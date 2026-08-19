"""
ChatAssistant — the decision-making chat agent. It turns ONE (possibly messy)
message into an ordered PLAN of safe tool calls, runs them in order, and composes
one clean reply. It holds NO business math (that lives in the domain services /
use cases it calls). Every write is audited; deletes require an explicit confirm
and are never chained.

Flow: planner (local LLM) -> list of steps -> run each -> compose. If the planner
is unavailable, it falls back to the single-intent resolver (LLM+regex), so the
chat always works.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Callable, Protocol

from ...domain.entities import AuditEntry
from ...domain.repositories import (
    AttendanceRepository,
    AuditRepository,
    ConfigRepository,
    EmployeeRepository,
    LabelRepository,
)
from ...domain.services import tutor
from ...domain.services.anomaly import (
    AnomalyDetector,
    DetectorTrainer,
    SupervisedTrainer,
)
from ...domain.services.chat_intents import (
    IntentResolver,
    _date as extract_date,
    _emp as extract_emp,
    resolve_month,
)
from ...domain.services.payroll_rules import PayrollRulesService
from .attendance_crud import (
    DeleteAttendance,
    EditAttendance,
    InsertAttendance,
    ShowDay,
)
from .check_all_employees import CheckAllEmployees
from .check_employee_month import CheckEmployeeMonth
from .check_employee_range import CheckEmployeeRange
from .configure import Configure
from .employee_crud import AddEmployee, DeleteEmployee, EditEmployee, ShowEmployee
from .find_employee import FindEmployee
from .generate_staff import GenerateStaff
from .import_bio_time import ImportBioTime
from .label_feedback import SaveLabel, SupervisedTrain
from .list_attendance import ListAttendance
from .list_employees import ListEmployees
from .payslip import Payslip
from .query_data import QueryData
from .train_model import TrainModel

_WD = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# tools that need an employee — used to resolve a bare NAME to an id
_NEEDS_EMPLOYEE = {
    "show_employee", "check_month", "check_range", "payslip", "list_attendance",
    "edit_employee", "delete_employee", "insert_attendance", "edit_attendance",
    "delete_attendance", "label",
}


@dataclass
class ChatReply:
    reply: str
    kind: str | None = None      # active model kind after train/retrain
    changed: bool = False        # did this modify data?


class PlanStep(Protocol):
    kind: str
    params: dict
    confirm: bool


class AgentPlanner(Protocol):
    def plan(self, message: str) -> list[PlanStep]: ...


class ChatAssistant:
    def __init__(
        self,
        employees: EmployeeRepository,
        attendance: AttendanceRepository,
        labels: LabelRepository,
        audit: AuditRepository,
        config: ConfigRepository,
        rules: PayrollRulesService,
        detector: AnomalyDetector,
        unsup_trainer: DetectorTrainer,
        sup_trainer: SupervisedTrainer,
        resolver: IntentResolver,
        planner: AgentPlanner,
        importer: ImportBioTime,
        import_path: str,
        clock: Callable[[], date],
        default_merge_seconds: int = 60,
        default_base_rate: float = 20.0,
        default_ot_rate: float = 30.0,
    ) -> None:
        self._emp = employees
        self._att = attendance
        self._lab = labels
        self._audit_repo = audit
        self._config = config
        self._rules = rules
        self._detector = detector
        self._unsup = unsup_trainer
        self._sup = sup_trainer
        self._resolver = resolver
        self._planner = planner
        self._importer = importer
        self._import_path = import_path
        self._clock = clock
        self._def_merge = default_merge_seconds
        self._def_base = default_base_rate
        self._def_ot = default_ot_rate

    # ---- public entry -------------------------------------------------------
    def handle(self, message: str) -> ChatReply:
        today = self._clock()
        steps = self._make_plan(message)
        ctx: dict = {}
        replies: list[ChatReply] = []
        for st in steps:
            params = dict(getattr(st, "params", None) or {})
            confirm = bool(getattr(st, "confirm", False))
            try:
                replies.append(
                    self._run_tool(st.kind, params, confirm, message, today, ctx))
            except ValueError as e:
                replies.append(ChatReply(f"⚠ {e}"))
            except Exception as e:  # noqa: BLE001 — surface adapter errors safely
                replies.append(ChatReply(f"⚠ Step '{st.kind}' failed: {e}"))
        if not replies:
            return ChatReply(tutor.help_text())
        return self._compose(replies)

    def _make_plan(self, message: str) -> list:
        """Ask the agent planner; fall back to the single-intent resolver."""
        try:
            steps = self._planner.plan(message)
        except Exception:
            steps = None
        if steps:
            return steps
        return [self._resolver.resolve(message)]     # Intent ~ PlanStep

    def _compose(self, replies: list[ChatReply]) -> ChatReply:
        if len(replies) == 1:
            return replies[0]
        changed = any(r.changed for r in replies)
        kind = next((r.kind for r in reversed(replies) if r.kind), None)
        body = "\n\n".join(f"[{i}] {r.reply}" for i, r in enumerate(replies, 1))
        return ChatReply(body, kind=kind, changed=changed)

    # ---- helpers ------------------------------------------------------------
    def _audit(self, action: str, target: str, detail: str) -> None:
        self._audit_repo.add(AuditEntry(action, target, detail))

    def _ym(self, params: dict, message: str, today: date) -> tuple[int, int]:
        if params.get("year") and params.get("month"):
            try:
                return int(params["year"]), int(params["month"])
            except (TypeError, ValueError):
                pass
        return resolve_month(today, params.get("month_phrase") or message)

    def _cfg_int(self, key: str, default: int) -> int:
        v = self._config.get(key)
        return int(float(v)) if v is not None else default

    def _cfg_float(self, key: str, default: float) -> float:
        v = self._config.get(key)
        return float(v) if v is not None else default

    def _roster(self, year: int, month: int, ctx: dict):
        key = (year, month)
        if key not in ctx:
            ctx[key] = CheckAllEmployees(
                self._emp, self._att, self._rules, self._detector).execute(year, month)
        return ctx[key]

    @staticmethod
    def _fmt_rows(title: str, month: str, rows, describe) -> str:
        if not rows:
            return f"{title} for {month}: none. ✅"
        lines = [f"{title} for {month} ({len(rows)}):"]
        lines += [f"• {r.employee_id} {r.employee_name} — {describe(r)}" for r in rows[:60]]
        if len(rows) > 60:
            lines.append(f"…and {len(rows) - 60} more")
        return "\n".join(lines)

    def run_tool(self, name: str, params: dict, confirm: bool, message: str,
                 today: date, ctx: dict) -> ChatReply:
        """Public entry for the HrmAgent loop — reuses the full tool dispatch."""
        return self._run_tool(name, dict(params or {}), confirm, message, today, ctx)

    # ---- the tool executor (one plan step) ---------------------------------
    def _run_tool(self, k: str, p: dict, confirm: bool, message: str,
                  today: date, ctx: dict) -> ChatReply:
        # deterministic slot backfill from the raw message (ids/dates the LLM drops)
        if not p.get("employee_id"):
            e = extract_emp(message)
            if e:
                p["employee_id"] = e
        # name fallback: a tool needs an employee but none/a wrong id was given → search
        if k in _NEEDS_EMPLOYEE:
            eid = p.get("employee_id")
            if not eid or self._emp.get(eid) is None:
                hits = FindEmployee(self._emp).execute(p.get("query") or message)
                if len(hits) == 1:
                    p["employee_id"] = hits[0].id
        if not p.get("day"):
            d = extract_date(message)
            if d:
                p["day"] = d

        if k == "help":
            return ChatReply(tutor.help_text())
        if k == "tutor":
            return ChatReply(tutor.answer(p.get("message", message)))

        # ---- roster queries across all employees ----
        if k in ("check_all", "list_unpaid", "list_absent", "list_issues", "list_paid"):
            y, m = self._ym(p, message, today)
            roster = self._roster(y, m, ctx)
            if not roster.rows:
                return ChatReply(f"No attendance data for {roster.month}. "
                                 f"Try 'generate salary for 5 employees' or 'import real data'.")
            if k == "list_unpaid":
                return ChatReply(self._fmt_rows(
                    "UNPAID (worked but $0)", roster.month, roster.unpaid(),
                    lambda r: f"{r.present_days} day(s) worked, paid $0"))
            if k == "list_absent":
                return ChatReply(self._fmt_rows(
                    "ABSENCES", roster.month, roster.with_absences(),
                    lambda r: f"{r.absent_days} absent day(s)"))
            if k == "list_issues":
                return ChatReply(self._fmt_rows(
                    "ISSUES (rule/ML flags)", roster.month, roster.with_issues(),
                    lambda r: f"{r.flagged_days} flagged, ${r.money_at_risk:,.0f} at risk"))
            if k == "list_paid":
                return ChatReply(self._fmt_rows(
                    "PAID", roster.month, roster.paid(),
                    lambda r: f"${r.total_paid:,.2f} for {r.present_days} day(s)"))
            # check_all — full roster
            rows = roster.rows
            head = (f"All employees — {roster.month} ({len(rows)} with data): "
                    f"{len(roster.paid())} paid, {len(roster.unpaid())} unpaid, "
                    f"{len(roster.with_issues())} with issues.")
            body = [f"• {r.employee_id} {r.employee_name}: paid ${r.total_paid:,.0f}/"
                    f"exp ${r.total_expected:,.0f}, {r.present_days}d, "
                    f"{r.flagged_days} flag [{r.status}]" for r in rows[:60]]
            if len(rows) > 60:
                body.append(f"…and {len(rows) - 60} more")
            return ChatReply(head + "\n" + "\n".join(body))

        if k == "find_employee":
            q = p.get("query") or message
            matches = FindEmployee(self._emp).execute(q)
            if not matches:
                return ChatReply(f"No employee matches '{str(q).strip()}'.")
            if len(matches) == 1:
                e = matches[0]
                wd = "/".join(_WD[d] for d in sorted(e.rules.weekend_days))
                return ChatReply(
                    f"{e.id} — {e.name}: ${e.rules.base_rate:.0f}/h base, "
                    f"${e.rules.ot_rate:.0f}/h OT, work {e.rules.work_goal:.0f}h, "
                    f"start {e.rules.shift_start}, weekend {wd}.")
            lines = [f"Found {len(matches)} employees:"]
            lines += [f"• {e.id} {e.name}" for e in matches[:40]]
            return ChatReply("\n".join(lines))

        if k == "query_data":
            y, m = self._ym(p, message, today)
            roster = self._roster(y, m, ctx)
            return ChatReply(QueryData().execute(roster, p))

        if k == "list_attendance":
            if not p.get("employee_id"):
                raise ValueError("Which employee? e.g. 'attendance for E100017'")
            if p.get("month_phrase") or (p.get("year") and p.get("month")):
                y, m = self._ym(p, message, today)
                return ChatReply(ListAttendance(self._emp, self._att).execute(
                    p["employee_id"], y, m))
            return ChatReply(ListAttendance(self._emp, self._att).execute(p["employee_id"]))

        if k == "payslip":
            if not p.get("employee_id"):
                raise ValueError("Which employee? e.g. 'payslip E100017 last month'")
            y, m = self._ym(p, message, today)
            stmt = Payslip(self._emp, self._att, self._rules, self._detector).execute(
                p["employee_id"], y, m)
            return ChatReply(stmt.text)

        # ---- generate ----
        if k == "generate_employees":
            count = int(p.get("count") or 5)
            base = self._cfg_float("default_base_rate", self._def_base)
            ot = self._cfg_float("default_ot_rate", self._def_ot)
            res = GenerateStaff(self._emp, self._att, self._rules).execute(
                count, base_rate=base, ot_rate=ot)
            self._audit("generate_employees", "demo", f"{res['employees']} added")
            ids = ", ".join(res["ids"][:10]) + ("…" if len(res["ids"]) > 10 else "")
            return ChatReply(
                f"Created {res['employees']} employees ({ids}). "
                f"Add salary with 'generate salary for {res['employees']} employees this month'.",
                changed=True)

        if k == "generate_salary":
            y, m = self._ym(p, message, today)
            count = int(p.get("count") or 5)
            base = self._cfg_float("default_base_rate", self._def_base)
            ot = self._cfg_float("default_ot_rate", self._def_ot)
            res = GenerateStaff(self._emp, self._att, self._rules).execute(
                count, y, m, base, ot)
            self._audit("generate_salary", res["month"] or "",
                        f"{res['employees']} emp, {res['attendance_days']} days")
            ids = ", ".join(res["ids"][:10]) + ("…" if len(res["ids"]) > 10 else "")
            return ChatReply(
                f"Generated {res['month']} salary for {res['employees']} new employees "
                f"({ids}): {res['attendance_days']} attendance days. "
                f"Check them with 'check all {res['month']}'.",
                changed=True)

        if k == "configure":
            key, val, label = Configure(self._config).execute(
                p.get("key"), p.get("value"))
            self._audit("configure", key, val)
            return ChatReply(
                f"Saved: {label} = {val}. It applies to the next import / generate.",
                changed=True)

        # ---- training ----
        if k == "train":
            rep = TrainModel(self._att, self._unsup).execute()
            self._audit("train", "model", f"IsolationForest on {rep.samples} days")
            return ChatReply(
                f"Trained on {rep.samples} worked days.\n"
                f"• Features: {', '.join(rep.features)}\n"
                f"• Algorithm: {rep.algorithm}\n"
                f"It learned the 'normal' pattern; unusual days get flagged. "
                f"Active model: unsupervised.",
                kind="iforest", changed=True)

        if k == "retrain":
            res = SupervisedTrain(self._att, self._lab, self._sup).execute()
            if not res["trained"]:
                return ChatReply(
                    f"You have {res['labels']} labelled day(s) "
                    f"({res['wrong']} wrong, {res['correct']} correct). I need at "
                    f"least 4 labels with BOTH classes. Label more, e.g. "
                    f"'E100 2024-06-11 is wrong'.")
            self._audit("retrain", "model", f"RandomForest on {res['labels']} labels")
            return ChatReply(
                f"Retrained a SUPERVISED model on your {res['labels']} labels "
                f"({res['wrong']} wrong, {res['correct']} correct). "
                f"The report now uses what YOU taught it. Active model: supervised.",
                kind="rf", changed=True)

        if k == "label":
            lab = SaveLabel(self._emp, self._att, self._lab).execute(
                p["employee_id"], p["day"], p["is_wrong"])
            self._audit("label", f"{lab.employee_id} {lab.day}",
                        "wrong" if lab.is_wrong else "correct")
            return ChatReply(
                f"Noted {lab.employee_id} on {lab.day} as "
                f"{'WRONG' if lab.is_wrong else 'CORRECT'}. "
                f"Say 'retrain from my labels' when ready.", changed=True)

        # ---- employees ----
        if k == "add_employee":
            e = AddEmployee(self._emp).execute(
                p.get("name"), p.get("base_rate"), p.get("ot_rate"),
                p.get("shift_start"), p.get("employee_id"))
            self._audit("add_employee", e.id, f"{e.name} ${e.rules.base_rate:.0f}/h")
            return ChatReply(
                f"Added {e.id} — {e.name}: ${e.rules.base_rate:.0f}/h base, "
                f"start {e.rules.shift_start}.", changed=True)

        if k == "edit_employee":
            e, desc = EditEmployee(self._emp).execute(
                p["employee_id"], p.get("field"), p.get("value"))
            self._audit("edit_employee", e.id, desc)
            return ChatReply(f"Updated {e.id} — {desc}.", changed=True)

        if k == "delete_employee":
            if not confirm:
                return ChatReply(
                    f"This will DELETE employee {p['employee_id']}. "
                    f"Send: 'delete employee {p['employee_id']} confirm' to proceed.")
            e = DeleteEmployee(self._emp).execute(p["employee_id"])
            self._audit("delete_employee", e.id, e.name)
            return ChatReply(f"Deleted employee {e.id} ({e.name}).", changed=True)

        if k == "show_employee":
            e = ShowEmployee(self._emp).execute(p["employee_id"])
            wd = "/".join(_WD[d] for d in sorted(e.rules.weekend_days))
            return ChatReply(
                f"{e.id} {e.name}: ${e.rules.base_rate:.0f}/h base, "
                f"${e.rules.ot_rate:.0f}/h OT, work {e.rules.work_goal:.0f}h, "
                f"start {e.rules.shift_start}, weekend {wd}.")

        if k == "list_employees":
            emps = ListEmployees(self._emp).execute()
            if not emps:
                return ChatReply("No employees yet. Try 'add employee Rakib rate 22'.")
            shown = ", ".join(f"{e.id} {e.name}" for e in emps[:40])
            more = f" …and {len(emps) - 40} more" if len(emps) > 40 else ""
            return ChatReply(f"Employees ({len(emps)}): " + shown + more)

        # ---- attendance / payroll ----
        if k == "insert_attendance":
            r = InsertAttendance(self._emp, self._att).execute(
                p["employee_id"], p["day"], p.get("day_type"),
                p.get("check_in"), p.get("check_out"), p.get("reported_pay"))
            self._audit("insert_attendance", f"{r.employee_id} {r.day}",
                        f"{r.day_type.value} ${r.reported_pay:.2f}")
            return ChatReply(
                f"Added attendance for {r.employee_id} on {r.day}: "
                f"{r.day_type.value}, {r.check_in or '—'}–{r.check_out or '—'}, "
                f"pay ${r.reported_pay:.2f}.", changed=True)

        if k == "edit_attendance":
            r, desc = EditAttendance(self._att).execute(
                p["employee_id"], p["day"], p["field"], p["value"])
            self._audit("edit_attendance", f"{r.employee_id} {r.day}", desc)
            return ChatReply(f"Updated {r.employee_id} {r.day} — {desc}.", changed=True)

        if k == "delete_attendance":
            if not confirm:
                return ChatReply(
                    f"This will DELETE attendance for {p['employee_id']} on "
                    f"{p['day']}. Send the same command with 'confirm'.")
            DeleteAttendance(self._att).execute(p["employee_id"], p["day"])
            self._audit("delete_attendance", f"{p['employee_id']} {p['day']}", "deleted")
            return ChatReply(
                f"Deleted attendance for {p['employee_id']} on {p['day']}.",
                changed=True)

        # ---- single-employee checks ----
        if k == "check_month":
            if self._emp.get(p["employee_id"]) is None:
                raise ValueError(f"{p['employee_id']} not found")
            y, m = self._ym(p, message, today)
            rep = CheckEmployeeMonth(
                self._emp, self._att, self._rules, self._detector
            ).execute(p["employee_id"], y, m)
            return ChatReply(f"{rep.summary}\nRules: {rep.rules_note}")

        if k == "check_range":
            if self._emp.get(p["employee_id"]) is None:
                raise ValueError(f"{p['employee_id']} not found")
            rep = CheckEmployeeRange(
                self._emp, self._att, self._rules, self._detector
            ).execute(p["employee_id"], int(p.get("months", 2)))
            return ChatReply(rep.summary)

        if k == "show_day":
            r = ShowDay(self._att).execute(p["employee_id"], p["day"])
            return ChatReply(
                f"{r.employee_id} {r.day}: {r.day_type.value}, "
                f"{r.check_in or '—'}–{r.check_out or '—'}, pay ${r.reported_pay:.2f}.")

        # ---- import real biometric data ----
        if k == "import_data":
            merge = p.get("merge_seconds")
            if merge is None:
                merge = self._cfg_int("merge_seconds", self._def_merge)
            rep = self._importer.execute(
                self._import_path, replace=p.get("replace", True),
                merge_seconds=merge)
            self._audit("import_data", "biometric",
                        f"{rep['employees']} employees, {rep['attendance_days']} days")
            scope = ("replaced the demo data" if rep["replaced_demo"]
                     else "added alongside the demo data")
            return ChatReply(
                f"Imported real biometric data ({scope}):\n"
                f"• {rep['employees']} employees, {rep['attendance_days']} attendance days "
                f"({rep['date_from']} → {rep['date_to']})\n"
                f"• Merged {rep['punches_merged_away']} duplicate punches "
                f"(window {rep['merge_seconds']}s) from {rep['punches_read']} reads\n"
                f"• {rep['missing_punch_days']} missing-punch days (checked in, never out)\n"
                f"Pay is a ${rep['default_base_rate']:.0f}/h baseline — tune per employee, "
                f"e.g. 'set E100017 base rate to 25'. Now say 'train' to fit the model.",
                changed=True)

        return ChatReply(tutor.help_text())
