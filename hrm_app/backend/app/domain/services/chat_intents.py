"""
Chat intent parser — pure domain, no framework. Turns a free-text message into
ONE safe, whitelisted Intent. It never executes anything; it only classifies.
This is the single source of "what the assistant understands".
"""
from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date

_WORDNUM = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
}


def _wordnum(token: str) -> int:
    token = token.strip().lower()
    return int(token) if token.isdigit() else _WORDNUM.get(token, 2)


# Every action the assistant can take. The LLM must choose from THIS set only
# (its safety boundary). Shared with the LLM prompt so both stay in sync.
KNOWN_KINDS = {
    "help", "tutor", "train", "retrain", "label",
    "add_employee", "edit_employee", "delete_employee", "show_employee",
    "list_employees", "insert_attendance", "edit_attendance",
    "delete_attendance", "check_month", "check_range", "show_day",
    "import_data",
    # Phase 4 — agent tools (aggregate queries, generate, payslip, config)
    "check_all", "list_unpaid", "list_absent", "list_issues", "list_paid",
    "payslip", "generate_employees", "generate_salary", "configure",
    # Phase 5 — employee search
    "find_employee",
    # Phase 6 — attendance listing
    "list_attendance",
}

# ---- recognisers -----------------------------------------------------------
_EMP = re.compile(r"\bE\d{3,}\b", re.IGNORECASE)
_DATE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
_TIME = re.compile(r"\b(\d{1,2}:\d{2})\b")
_NUM = re.compile(r"(-?\d+(?:\.\d+)?)")

_MONTHS = {
    "january": 1, "jan": 1, "february": 2, "feb": 2, "march": 3, "mar": 3,
    "april": 4, "apr": 4, "may": 5, "june": 6, "jun": 6, "july": 7, "jul": 7,
    "august": 8, "aug": 8, "september": 9, "sep": 9, "sept": 9, "october": 10,
    "oct": 10, "november": 11, "nov": 11, "december": 12, "dec": 12,
}

# keyword -> canonical DayType value
_DAYTYPES = {
    "present": "present", "late": "late", "half_day": "half_day",
    "half day": "half_day", "halfday": "half_day", "overtime": "overtime",
    "ot": "overtime", "absent": "absent", "leave": "leave",
    "weekend": "weekend", "holiday": "holiday",
    "missing_punch": "missing_punch", "missing punch": "missing_punch",
}

_TUTOR_KEYS = (
    "how does", "what is", "explain", "why ", "supervised", "unsupervised",
    "overfit", "feature", "isolation forest", "random forest", "anomaly",
    "how do you train", "teach the model",
)


@dataclass
class Intent:
    kind: str
    params: dict = field(default_factory=dict)
    confirm: bool = False


# ---- small extractors ------------------------------------------------------
def _emp(text: str) -> str | None:
    m = _EMP.search(text)
    if m:
        return m.group(0).upper()
    # also accept "employee 100" / "emp 100" / "staff 100" -> E100
    m2 = re.search(r"\b(?:employee|emp|staff|worker|id)\s+#?(\d{3,})\b", text, re.IGNORECASE)
    return f"E{m2.group(1)}" if m2 else None


# slots the deterministic enricher can backfill when the LLM omits them
_NEEDS_EMP = {
    "edit_employee", "delete_employee", "show_employee", "insert_attendance",
    "edit_attendance", "delete_attendance", "check_month", "check_range",
    "show_day", "label",
}
_NEEDS_DAY = {
    "insert_attendance", "edit_attendance", "delete_attendance", "show_day", "label",
}


def enrich(intent: "Intent", message: str) -> "Intent":
    """
    Deterministically fill missing slots from the message. A small LLM often
    picks the right action but drops the employee id / date / value — regex is
    reliable for those, so we repair the LLM's params here.
    """
    kind = intent.kind
    p = dict(intent.params or {})
    low = message.lower()

    if kind in _NEEDS_EMP and not p.get("employee_id"):
        e = _emp(message)
        if e:
            p["employee_id"] = e
    if kind in _NEEDS_DAY and not p.get("day"):
        d = _date(message)
        if d:
            p["day"] = d

    rng = re.search(
        r"(?:last|past)\s+(\d+|one|two|three|four|five|six|seven|eight|nine|"
        r"ten|eleven|twelve)\s+month", low)
    if kind == "check_month" and rng:          # "last N months" beats single month
        return Intent("check_range",
                      {"employee_id": p.get("employee_id"), "months": _wordnum(rng.group(1))},
                      intent.confirm)
    if kind == "check_range" and not p.get("months"):
        p["months"] = _wordnum(rng.group(1)) if rng else 2
    if kind == "check_month":
        mo = _month(low)
        p.setdefault("year", mo[0] if mo else 2024)
        p.setdefault("month", mo[1] if mo else 6)
    if kind == "import_data":
        for key, val in _import_slots(low).items():
            p.setdefault(key, val)
    return Intent(kind, p, intent.confirm)


def _date(text: str) -> str | None:
    m = _DATE.search(text)
    return m.group(1) if m else None


def _month(low: str) -> tuple[int, int] | None:
    m = re.search(r"\b(\d{4})-(\d{2})\b", low)
    if m:
        return int(m.group(1)), int(m.group(2))
    for name, num in _MONTHS.items():
        if re.search(rf"\b{name}\b", low):
            y = re.search(r"\b(20\d{2})\b", low)
            return (int(y.group(1)) if y else 2024), num
    return None


def _shift_month(year: int, month: int, back: int) -> tuple[int, int]:
    total = year * 12 + (month - 1) - back
    return total // 12, total % 12 + 1


def resolve_month(today: date, phrase: str) -> tuple[int, int]:
    """
    Turn a (possibly messy) phrase into (year, month), relative to `today`.
    "last month" -> previous month; "N months ago" -> back N; an explicit
    month name / YYYY-MM wins when present; otherwise the current month.
    The clock is passed in so the domain stays free of wall-clock calls.
    """
    low = (phrase or "").lower()
    if any(k in low for k in ("last month", "previous month", "past month")):
        return _shift_month(today.year, today.month, 1)
    ago = re.search(r"(\d+)\s+months?\s+ago", low)
    if ago:
        return _shift_month(today.year, today.month, int(ago.group(1)))
    if "this month" in low or "current month" in low:
        return today.year, today.month
    explicit = _month(low)
    if explicit:
        return explicit
    return today.year, today.month


def _value_after_to(text: str) -> str | None:
    parts = re.split(r"\bto\b", text, flags=re.IGNORECASE)
    if len(parts) >= 2:
        return parts[-1].strip()
    return None


def _last_number(text: str) -> float | None:
    nums = _NUM.findall(text)
    return float(nums[-1]) if nums else None


def _day_type(low: str) -> str | None:
    for kw, val in _DAYTYPES.items():
        if re.search(rf"\b{re.escape(kw)}\b", low):
            return val
    return None


def _emp_field(low: str) -> str | None:
    if "ot rate" in low or "overtime rate" in low or "ot_rate" in low:
        return "ot_rate"
    if "base rate" in low or "rate" in low:
        return "base_rate"
    if "name" in low:
        return "name"
    if "shift start" in low or "start" in low:
        return "shift_start"
    if "weekend" in low:
        return "weekend_days"
    if "work goal" in low or "goal" in low:
        return "work_goal"
    return None


def _att_field(low: str) -> str | None:
    if "checkout" in low or "check out" in low or "check-out" in low:
        return "check_out"
    if "checkin" in low or "check in" in low or "check-in" in low:
        return "check_in"
    if "type" in low:
        return "day_type"
    if "pay" in low or "payroll" in low:
        return "reported_pay"
    return None


def _parse_configure(low: str) -> "Intent":
    """Map a 'set merge window to 90' style message to a configure intent."""
    m = re.search(r"(-?\d+(?:\.\d+)?)", low)
    value = m.group(1) if m else None
    if "merge" in low:
        key = "merge_seconds"
    elif "ot" in low or "overtime" in low:
        key = "default_ot_rate"
    elif "tolerance" in low:
        key = "tolerance"
    else:
        key = "default_base_rate"
    return Intent("configure", {"key": key, "value": value})


def _import_slots(low: str) -> dict:
    """Optional slots on an import message: merge window + keep-demo flag."""
    p: dict = {}
    m = (re.search(r"merge\s+(?:window\s+)?(?:to\s+)?(\d+)", low)
         or re.search(r"(\d+)\s*(?:s\b|sec|second)", low))
    if m:
        p["merge_seconds"] = int(m.group(1))
    if any(w in low for w in ("keep", "both", "beside", "alongside")):
        p["replace"] = False
    return p


# ---- the parser ------------------------------------------------------------
def parse(message: str) -> Intent:
    text = message.strip()
    low = text.lower()
    emp = _emp(text)
    dt = _date(text)
    confirm = bool(re.search(r"\bconfirm\b|\byes\b", low))

    if not low or low in ("help", "?", "hi", "hello", "commands"):
        return Intent("help")

    # ----- configuration (global settings, no employee id) -----
    if emp is None and any(
        w in low for w in ("merge window", "merge second", "merge to", "punch merge",
                           "default rate", "default base", "default ot", "tolerance")
    ) and any(v in low for v in ("set", "change", "configure", "update", "make")):
        return _parse_configure(low)

    # ----- deletes (need confirm) -----
    if "delete" in low and "employee" in low and emp:
        return Intent("delete_employee", {"employee_id": emp}, confirm)
    if "delete" in low and emp and (dt or "attendance" in low):
        return Intent("delete_attendance", {"employee_id": emp, "day": dt}, confirm)

    # ----- adds -----
    if ("add" in low or "create" in low) and "employee" in low:
        return _parse_add_employee(text, low, emp)
    if (("add" in low or "insert" in low) and ("attendance" in low)) or (
        low.startswith("add") and emp and dt
    ):
        return _parse_insert_attendance(text, low, emp, dt)

    # ----- payroll (pay on a day) -----
    if ("payroll" in low or "pay" in low) and emp and dt and _last_number(text) is not None:
        return Intent("edit_attendance", {
            "employee_id": emp, "day": dt,
            "field": "reported_pay", "value": _last_number(text)})

    # ----- edits (set ...) -----
    if low.startswith("set") and emp and dt:
        fld = _att_field(low) or "reported_pay"
        val = _value_after_to(text) or (str(_last_number(text)) if _last_number(text) is not None else None)
        return Intent("edit_attendance", {
            "employee_id": emp, "day": dt, "field": fld, "value": val})
    if low.startswith("set") and emp:
        fld = _emp_field(low)
        val = _value_after_to(text)
        return Intent("edit_employee", {"employee_id": emp, "field": fld, "value": val})

    # ----- labeling (teach) -----
    if emp and dt and ("wrong" in low or "correct" in low or "right" in low or "mark" in low):
        return Intent("label", {
            "employee_id": emp, "day": dt, "is_wrong": "wrong" in low})

    # ----- training -----
    if "retrain" in low or ("train" in low and "label" in low):
        return Intent("retrain")
    if low == "train" or "train the model" in low or "train model" in low or low.startswith("train"):
        return Intent("train")

    # ----- check / show -----
    if low.startswith("check") and emp:
        rng = re.search(
            r"(?:last|past)\s+(\d+|one|two|three|four|five|six|seven|eight|"
            r"nine|ten|eleven|twelve)\s+month", low)
        if rng:
            return Intent("check_range", {
                "employee_id": emp, "months": _wordnum(rng.group(1))})
        mo = _month(low)
        return Intent("check_month", {
            "employee_id": emp,
            "year": mo[0] if mo else 2024,
            "month": mo[1] if mo else 6})
    if low.startswith("show") and emp and dt:
        return Intent("show_day", {"employee_id": emp, "day": dt})
    if low.startswith("show") and emp:
        return Intent("show_employee", {"employee_id": emp})
    if "list" in low and ("employee" in low or "staff" in low):
        return Intent("list_employees")

    # ----- list an employee's attendance -----
    if ("attendance" in low or "attendce" in low or "attehnd" in low or "attend" in low) \
            and any(w in low for w in ("show", "list", "view", "last", "recent")) \
            and not any(w in low for w in ("add", "insert", "delete", "set ")):
        return Intent("list_attendance", {"employee_id": emp, "query": low})

    # ----- find / search an employee -----
    if any(w in low for w in ("find", "search", "lookup", "look up", "who is")) \
            and any(w in low for w in ("employee", "emp", "staff", "worker", "name")):
        return Intent("find_employee", {"query": low})

    # ----- roster queries across ALL employees + generate + payslip -----
    if re.search(r"\bunpaid\b", low) or "not paid" in low:
        return Intent("list_unpaid", {"month_phrase": low})
    if re.search(r"\babsent", low) and any(w in low for w in ("list", "show", "who", "how many")):
        return Intent("list_absent", {"month_phrase": low})
    if any(w in low for w in ("issue", "problem", "fine", "rule break", "broke", "flag")) \
            and any(w in low for w in ("list", "show", "who", "report", "find")):
        return Intent("list_issues", {"month_phrase": low})
    if re.search(r"\bpaid\b", low) and "list" in low:
        return Intent("list_paid", {"month_phrase": low})
    if any(w in low for w in ("check all", "check everyone", "everyone", "all employee",
                             "every employee", "all staff", "whole team", "all payslip")):
        return Intent("check_all", {"month_phrase": low})
    if "payslip" in low or "pay slip" in low or "pay-slip" in low:
        return Intent("payslip", {"employee_id": emp, "month_phrase": low})
    if any(w in low for w in ("generate", "make", "create")) \
            and any(w in low for w in ("salary", "salery", "payroll")):
        n = _last_number(low)
        return Intent("generate_salary", {"count": int(n) if n else 5, "month_phrase": low})
    if any(w in low for w in ("make", "create", "generate")) \
            and re.search(r"employe", low) and _last_number(low) is not None:
        return Intent("generate_employees", {"count": int(_last_number(low))})

    # ----- import real biometric data -----
    if "import" in low and any(
        w in low for w in ("real", "bio", "biometric", "punch",
                           "sql", "data", "attendance", "file")):
        return Intent("import_data", _import_slots(low))

    # ----- tutor -----
    if any(k in low for k in _TUTOR_KEYS):
        return Intent("tutor", {"message": low})

    return Intent("help")


def _parse_add_employee(text: str, low: str, emp: str | None) -> Intent:
    # name = words after 'employee'/'named' up to a keyword
    m = re.search(r"(?:employee|named)\s+([A-Za-z][A-Za-z .]*?)(?=\s+(?:rate|ot|start|weekend|id|E\d|$))",
                  text, re.IGNORECASE)
    name = m.group(1).strip() if m else None
    rate = _after_kw(low, "rate")
    ot = _after_kw(low, "ot")
    start = _TIME.search(text)
    return Intent("add_employee", {
        "employee_id": emp,
        "name": name,
        "base_rate": rate,
        "ot_rate": ot,
        "shift_start": start.group(1) if start else None,
    })


def _parse_insert_attendance(text: str, low: str, emp: str | None, dt: str | None) -> Intent:
    times = _TIME.findall(text)
    pay = None
    mpay = re.search(r"pay\s+(-?\d+(?:\.\d+)?)", low)
    if mpay:
        pay = float(mpay.group(1))
    return Intent("insert_attendance", {
        "employee_id": emp,
        "day": dt,
        "day_type": _day_type(low) or "present",
        "check_in": times[0] if len(times) >= 1 else None,
        "check_out": times[1] if len(times) >= 2 else None,
        "reported_pay": pay,
    })


def _after_kw(low: str, kw: str) -> float | None:
    m = re.search(rf"\b{kw}\s+(-?\d+(?:\.\d+)?)", low)
    return float(m.group(1)) if m else None


class IntentResolver(ABC):
    """Port: turn a message into a safe Intent. Regex or LLM implement this."""

    @abstractmethod
    def resolve(self, message: str) -> Intent:
        ...


class RegexResolver(IntentResolver):
    """Deterministic keyword/regex resolver (pure, always available)."""

    def resolve(self, message: str) -> Intent:
        return parse(message)
