"""
Agent PLANNER backed by a local Ollama model (free, offline). It turns ONE message
into an ordered list of tool-calls chosen from the SAFE whitelist — the model
decides WHAT to do; it never runs code/SQL. Returns [] on any problem so the
ChatAssistant falls back to its single-intent resolver.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field

import httpx

from ...domain.services.chat_intents import KNOWN_KINDS

_SYSTEM = """You are an HR admin assistant. Turn the user's ONE message into an
ordered PLAN of tool calls. Output ONLY JSON: {"steps":[{"kind":..,"params":{..}}]}.

Use ONLY these tools:
- help {}                         (you don't understand)
- tutor {message}                 ("how does training work?")
- list_employees {}               (names of everyone)
- show_employee {employee_id}
- add_employee {name, base_rate?, ot_rate?, shift_start?}
- edit_employee {employee_id, field, value}   field: base_rate|ot_rate|work_goal|shift_start|name|weekend_days
- delete_employee {employee_id}
- insert_attendance {employee_id, day, day_type, check_in, check_out, reported_pay}
- edit_attendance {employee_id, day, field, value}   field: check_in|check_out|day_type|reported_pay
- delete_attendance {employee_id, day}
- check_month {employee_id, month_phrase}       (one employee, one month)
- check_range {employee_id, months}             ("last two months" -> months:2)
- show_day {employee_id, day}
- payslip {employee_id, month_phrase}           (pay statement + audit for one person)
- check_all {month_phrase}                      (every employee, a month roster)
- list_unpaid {month_phrase}                    (worked but not paid)
- list_absent {month_phrase}                    (who was absent)
- list_issues {month_phrase}                    (rule breaks / fines / flags)
- list_paid {month_phrase}                      (who was paid)
- generate_employees {count}                    ("make 10 employees")
- generate_salary {count, month_phrase}         (make N employees + a month of salary)
- configure {key, value}   key: merge_seconds|default_base_rate|default_ot_rate
- import_data {replace?}                        (load the real biometric SQL file)
- train {}                                      (unsupervised model)
- retrain {}                                    ("retrain from my labels")
- label {employee_id, day, is_wrong}

Rules:
- Break the request into MULTIPLE steps in the order they must run.
- Employee ids look like E100 or E100017. Normalize "employee 100" -> "E100".
- For any month, pass {"month_phrase":"<the words>"} (e.g. "last month","june",
  "2026-07"). Do NOT compute dates yourself.
- Never chain deletes; at most one delete, and set confirm only if the user
  said confirm/yes.
- If you don't understand, return {"steps":[{"kind":"help","params":{}}]}.

Examples:
"last month unpaid list" -> {"steps":[{"kind":"list_unpaid","params":{"month_phrase":"last month"}}]}
"make 10 employees" -> {"steps":[{"kind":"generate_employees","params":{"count":10}}]}
"last month make 5 employee salary and check payslip, show me the issue list and paid list" ->
{"steps":[{"kind":"generate_salary","params":{"count":5,"month_phrase":"last month"}},{"kind":"list_issues","params":{"month_phrase":"last month"}},{"kind":"list_paid","params":{"month_phrase":"last month"}}]}
"import real data then train" -> {"steps":[{"kind":"import_data","params":{}},{"kind":"train","params":{}}]}
"set merge window to 90 seconds" -> {"steps":[{"kind":"configure","params":{"key":"merge_seconds","value":"90"}}]}
"check employee 100017 last two months" -> {"steps":[{"kind":"check_range","params":{"employee_id":"E100017","months":2}}]}
"""


@dataclass
class ToolCall:
    kind: str
    params: dict = field(default_factory=dict)
    confirm: bool = False


class NullPlanner:
    """No-op planner (LLM disabled) — forces the single-intent regex fallback."""

    def plan(self, message: str) -> list[ToolCall]:
        return []


class OllamaAgentPlanner:
    def __init__(self, host: str, model: str, timeout: float = 90.0) -> None:
        self._url = host.rstrip("/") + "/api/chat"
        self._model = model
        self._timeout = timeout

    def plan(self, message: str) -> list[ToolCall]:
        payload = {
            "model": self._model,
            "messages": [
                {"role": "system", "content": _SYSTEM},
                {"role": "user", "content": message},
            ],
            "stream": False,
            "format": "json",
            "options": {"temperature": 0},
        }
        r = httpx.post(self._url, json=payload,
                       timeout=httpx.Timeout(self._timeout, connect=3.0))
        r.raise_for_status()
        data = json.loads(r.json()["message"]["content"])
        steps = data.get("steps") if isinstance(data, dict) else None
        if not isinstance(steps, list):
            return []
        out: list[ToolCall] = []
        for s in steps:
            if not isinstance(s, dict):
                continue
            kind = str(s.get("kind", "")).strip()
            if kind not in KNOWN_KINDS:
                continue
            params = s.get("params")
            if not isinstance(params, dict):
                params = {}
            out.append(ToolCall(kind, params, bool(s.get("confirm", False))))
        return out
