"""
Domain entities — the nouns of the payroll world, plus the result objects the
checker produces. Pure Python; no framework/DB/ML imports.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from .value_objects import DayType, EmployeeRules


@dataclass
class Employee:
    """A person on payroll, with their own pay rules."""
    id: str
    name: str
    rules: EmployeeRules = field(default_factory=EmployeeRules.default)


@dataclass
class AttendanceDay:
    """One employee's record for one calendar day (raw input to the checker)."""
    employee_id: str
    day: date
    day_type: DayType
    check_in: str | None      # 'HH:MM' or None for no-punch days
    check_out: str | None
    reported_pay: float


@dataclass
class Label:
    """A user's teaching signal: this day is wrong (1) or correct (0)."""
    employee_id: str
    day: date
    is_wrong: bool


@dataclass
class AuditEntry:
    """A record of one change made through the assistant (who did what)."""
    action: str               # e.g. "edit_employee", "delete_attendance"
    target: str               # e.g. "E101", "E101 2024-06-12"
    detail: str               # human-readable change description


# Combined verdict status for a single day.
STATUS_OK = "OK"
STATUS_RULE = "RULE-FLAG"     # rules math says wrong
STATUS_ML = "ML-FLAG"         # model says unusual (rules missed it)
STATUS_BOTH = "BOTH"          # both agree it's wrong


@dataclass
class DayVerdict:
    """The checker's decision for one day — everything the UI needs, no gaps."""
    day: date
    day_type: DayType
    check_in: str | None
    check_out: str | None
    presence_hours: float
    ot_hours: float
    expected_pay: float
    reported_pay: float
    diff: float               # reported - expected (negative = underpaid)
    rule_flag: bool
    ml_flag: bool
    status: str
    reason: str               # plain words: why flagged (or "OK")
    rule_note: str            # which rule/policy was applied (closes info gap)


@dataclass
class MonthReport:
    """A full month for one employee: the days plus rolled-up KPIs + summary."""
    employee_id: str
    employee_name: str
    month: str                # 'YYYY-MM'
    rules_note: str           # which contract/rules were used
    days: list[DayVerdict]

    # KPIs (filled by the checker service)
    total_days: int = 0
    present_days: int = 0
    absent_days: int = 0
    late_days: int = 0
    leave_days: int = 0
    total_hours: float = 0.0
    ot_hours: float = 0.0
    total_paid: float = 0.0
    total_expected: float = 0.0
    money_at_risk: float = 0.0
    flagged_days: int = 0
    summary: str = ""
