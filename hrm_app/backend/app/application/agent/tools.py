"""
Tool registry — the agent's action catalog. Each Tool carries the JSON Schema the
LLM sees (via `schemas()`), plus `writes`/`destructive` flags the agent uses for
auditing and confirm-gating. Execution is delegated to the shared ChatAssistant
executor (`run_tool`), so there is ONE dispatch implementation — this is only
metadata + the tool contract the model is offered.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Tool:
    name: str
    description: str
    parameters: dict            # JSON Schema (object)
    writes: bool = False
    destructive: bool = False

    def schema(self) -> dict:
        return {"type": "function", "function": {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }}


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def schemas(self) -> list[dict]:
        return [t.schema() for t in self._tools.values()]

    def names(self) -> list[str]:
        return list(self._tools)


# ---- schema shorthands -----------------------------------------------------
def _obj(props: dict, required: list[str] | None = None) -> dict:
    return {"type": "object", "properties": props, "required": required or []}


_STR = {"type": "string"}
_INT = {"type": "integer"}
_NUM = {"type": "number"}
_BOOL = {"type": "boolean"}
_MONTH = {"type": "string",
          "description": "month words: 'last month', 'this month', 'june', or '2026-07'"}


def default_registry() -> ToolRegistry:
    r = ToolRegistry()
    add = r.register

    # --- read / query ---
    add(Tool("find_employee",
             "Search employees by name or id fragment (e.g. '17' -> E100017, 'jashim').",
             _obj({"query": _STR}, ["query"])))
    add(Tool("list_employees", "List all employees.", _obj({})))
    add(Tool("show_employee", "Show one employee's contract/pay rules.",
             _obj({"employee_id": _STR}, ["employee_id"])))
    add(Tool("check_month",
             "Audit ONE employee for a month (pay vs expected, flagged days).",
             _obj({"employee_id": _STR, "month_phrase": _MONTH}, ["employee_id"])))
    add(Tool("check_range", "Audit ONE employee across the last N months.",
             _obj({"employee_id": _STR, "months": _INT}, ["employee_id"])))
    add(Tool("check_all", "Roster of EVERY employee for a month (paid/expected/flags).",
             _obj({"month_phrase": _MONTH})))
    add(Tool("list_unpaid", "Employees who worked but were not paid, for a month.",
             _obj({"month_phrase": _MONTH})))
    add(Tool("list_absent", "Employees with absences for a month.",
             _obj({"month_phrase": _MONTH})))
    add(Tool("list_issues", "Employees with rule/ML flags (issues/fines) for a month.",
             _obj({"month_phrase": _MONTH})))
    add(Tool("list_paid", "Employees who were paid, for a month.",
             _obj({"month_phrase": _MONTH})))
    add(Tool("payslip", "One employee's payslip (base+OT+net) plus audit, for a month.",
             _obj({"employee_id": _STR, "month_phrase": _MONTH}, ["employee_id"])))
    add(Tool("list_attendance",
             "Show an employee's recent attendance days (date, type, in/out, pay). "
             "Defaults to their latest month; pass month_phrase for a specific month.",
             _obj({"employee_id": _STR, "month_phrase": _MONTH}, ["employee_id"])))
    add(Tool("query_data",
             "Flexible query over the month roster. Filter/sort/limit by these fields: "
             "paid, expected, present_days, absent_days, late_days, flagged_days, "
             "money_at_risk, ot_hours, total_hours, status ('OK'/'ISSUES'), is_paid. "
             "Use for 'top N by X', 'who has more than X', etc.",
             _obj({"month_phrase": _MONTH,
                   "filters": {"type": "array", "items":
                               _obj({"field": _STR, "op": _STR, "value": _STR})},
                   "sort_by": _STR, "descending": _BOOL, "limit": _INT})))
    add(Tool("tutor", "Explain an HRM/ML concept in plain words.",
             _obj({"message": _STR})))

    # --- write ---
    add(Tool("add_employee", "Add a new employee.",
             _obj({"name": _STR, "base_rate": _NUM, "ot_rate": _NUM, "shift_start": _STR},
                  ["name"]), writes=True))
    add(Tool("edit_employee",
             "Edit an employee field: base_rate|ot_rate|work_goal|shift_start|name|weekend_days.",
             _obj({"employee_id": _STR, "field": _STR, "value": _STR},
                  ["employee_id", "field", "value"]), writes=True))
    add(Tool("delete_employee", "Delete an employee. Destructive — needs confirm.",
             _obj({"employee_id": _STR}, ["employee_id"]), writes=True, destructive=True))
    add(Tool("insert_attendance", "Add an attendance day for an employee.",
             _obj({"employee_id": _STR, "day": _STR, "day_type": _STR,
                   "check_in": _STR, "check_out": _STR, "reported_pay": _NUM},
                  ["employee_id", "day"]), writes=True))
    add(Tool("edit_attendance",
             "Edit an attendance day field: check_in|check_out|day_type|reported_pay.",
             _obj({"employee_id": _STR, "day": _STR, "field": _STR, "value": _STR},
                  ["employee_id", "day", "field", "value"]), writes=True))
    add(Tool("delete_attendance", "Delete an attendance day. Destructive — needs confirm.",
             _obj({"employee_id": _STR, "day": _STR}, ["employee_id", "day"]),
             writes=True, destructive=True))
    add(Tool("generate_employees", "Create N demo employees (no salary).",
             _obj({"count": _INT}, ["count"]), writes=True))
    add(Tool("generate_salary", "Create N demo employees WITH a month of salary.",
             _obj({"count": _INT, "month_phrase": _MONTH}, ["count"]), writes=True))
    add(Tool("configure",
             "Change a setting: key = merge_seconds | default_base_rate | default_ot_rate.",
             _obj({"key": _STR, "value": _STR}, ["key", "value"]), writes=True))
    add(Tool("label", "Mark an employee's day wrong/correct to teach the model.",
             _obj({"employee_id": _STR, "day": _STR, "is_wrong": _BOOL},
                  ["employee_id", "day", "is_wrong"]), writes=True))
    add(Tool("train", "Train the anomaly model (unsupervised).", _obj({}), writes=True))
    add(Tool("retrain", "Retrain a supervised model from saved labels.", _obj({}), writes=True))
    add(Tool("import_data", "Import the real biometric SQL file (replaces demo data).",
             _obj({"replace": _BOOL}), writes=True))
    return r
