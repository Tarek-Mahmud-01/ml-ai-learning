"""
LLM intent resolver backed by a LOCAL Ollama model (free, offline). It reads a
free-text message and returns a structured Intent chosen from the SAFE whitelist
— the model understands language but never runs code/SQL. On any problem
(Ollama down, bad output) it falls back to the deterministic regex resolver, so
the chat always works.
"""
from __future__ import annotations

import json

import httpx

from ...domain.services.chat_intents import (
    KNOWN_KINDS,
    Intent,
    IntentResolver,
    enrich,
)

_SYSTEM = """You convert an HR admin's message into ONE JSON action.
Output ONLY JSON: {"kind": <action>, "params": {...}, "confirm": <bool>}.
Pick kind from EXACTLY this list:
- help {}                         (anything you don't understand)
- tutor {message}                 (questions like "how does training work")
- train {}                        (retrain the anomaly model, unsupervised)
- retrain {}                      ("retrain from my labels", supervised)
- label {employee_id, day, is_wrong}   (day=YYYY-MM-DD; "wrong"->true,"correct"->false)
- add_employee {name, base_rate?, ot_rate?, shift_start?}
- edit_employee {employee_id, field, value}   field in base_rate|ot_rate|work_goal|shift_start|name|weekend_days
- delete_employee {employee_id}
- show_employee {employee_id}
- list_employees {}
- insert_attendance {employee_id, day, day_type, check_in, check_out, reported_pay}
      day_type in present|late|half_day|overtime|absent|leave|weekend|holiday|missing_punch
- edit_attendance {employee_id, day, field, value}   field in check_in|check_out|day_type|reported_pay
- delete_attendance {employee_id, day}
- check_month {employee_id, year, month}
- check_range {employee_id, months}    (e.g. "last two months" -> months:2)
- show_day {employee_id, day}
- import_data {merge_seconds?, replace?}   (load the real biometric SQL file; "keep the demo" -> replace:false)
Rules:
- Employee ids look like E100. Normalize "employee 100" or "100" to "E100".
- "pay"/"payroll" changes are edit_attendance with field="reported_pay".
- confirm=true ONLY if the user says confirm/yes; else false.
- If unsure, use kind "help".
Examples:
"check employee 100 for the last two months and tell me good or bad" -> {"kind":"check_range","params":{"employee_id":"E100","months":2},"confirm":false}
"make Karim's pay rate 30" -> {"kind":"edit_employee","params":{"employee_id":"","field":"base_rate","value":"30"},"confirm":false}
"set E101 june 12 pay to 190" -> {"kind":"edit_attendance","params":{"employee_id":"E101","day":"2024-06-12","field":"reported_pay","value":"190"},"confirm":false}
"how do you train the model" -> {"kind":"tutor","params":{"message":"how do you train the model"},"confirm":false}
"import the real biometric data" -> {"kind":"import_data","params":{},"confirm":false}
"load the real attendance file but keep the demo" -> {"kind":"import_data","params":{"replace":false},"confirm":false}
"""


class OllamaIntentResolver(IntentResolver):
    def __init__(self, fallback: IntentResolver, host: str, model: str,
                 timeout: float = 30.0) -> None:
        self._fallback = fallback
        self._url = host.rstrip("/") + "/api/chat"
        self._model = model
        self._timeout = timeout

    def resolve(self, message: str) -> Intent:
        try:
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
                           timeout=httpx.Timeout(self._timeout, connect=2.0))
            r.raise_for_status()
            content = r.json()["message"]["content"]
            data = json.loads(content)
            kind = str(data.get("kind", "")).strip()
            # LLM unsure or gave a bad kind -> trust the deterministic parser
            if kind not in KNOWN_KINDS or kind == "help":
                return self._fallback.resolve(message)
            params = data.get("params") or {}
            if not isinstance(params, dict):
                params = {}
            # LLM chose the action; regex fills any slots it dropped (id/date/value)
            return enrich(Intent(kind, params, bool(data.get("confirm", False))), message)
        except Exception:
            # Ollama down / timeout / bad JSON -> deterministic parser
            return self._fallback.resolve(message)
