"""
Pydantic request/response models + mappers from domain objects.
Presentation detail: shapes the JSON the frontend receives. No logic here.
"""
from __future__ import annotations

from pydantic import BaseModel

from ..domain.entities import Employee, MonthReport

_WD = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


class EmployeeOut(BaseModel):
    id: str
    name: str
    base_rate: float
    ot_rate: float
    work_goal: float
    shift_start: str
    weekend_days: str


class DayVerdictOut(BaseModel):
    day: str
    day_type: str
    check_in: str | None
    check_out: str | None
    presence_hours: float
    ot_hours: float
    expected_pay: float
    reported_pay: float
    diff: float
    rule_flag: bool
    ml_flag: bool
    status: str
    reason: str
    rule_note: str


class MonthReportOut(BaseModel):
    employee_id: str
    employee_name: str
    month: str
    rules_note: str
    total_days: int
    present_days: int
    absent_days: int
    late_days: int
    leave_days: int
    total_hours: float
    ot_hours: float
    total_paid: float
    total_expected: float
    money_at_risk: float
    flagged_days: int
    summary: str
    days: list[DayVerdictOut]


class SeedRequest(BaseModel):
    month: str = "2024-06"   # YYYY-MM


class SeedResult(BaseModel):
    month: str
    employees: int
    attendance_days: int
    injected_fraud: int


class TrainResult(BaseModel):
    samples_trained: int


class ImportRequest(BaseModel):
    path: str | None = None       # defaults to settings.import_sql_path
    replace: bool = True          # clear demo data first
    merge_seconds: int | None = None  # override the punch-merge window


class ImportResult(BaseModel):
    employees: int
    attendance_days: int
    missing_punch_days: int
    punches_read: int
    punches_kept: int
    punches_merged_away: int
    date_from: str | None
    date_to: str | None
    merge_seconds: int
    default_base_rate: float
    replaced_demo: bool


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None      # agent conversation memory


class ChatReplyOut(BaseModel):
    reply: str
    kind: str | None = None
    changed: bool = False


def employee_out(e: Employee) -> EmployeeOut:
    weekend = "/".join(_WD[d] for d in sorted(e.rules.weekend_days))
    return EmployeeOut(
        id=e.id, name=e.name, base_rate=e.rules.base_rate,
        ot_rate=e.rules.ot_rate, work_goal=e.rules.work_goal,
        shift_start=e.rules.shift_start, weekend_days=weekend)


def month_report_out(r: MonthReport) -> MonthReportOut:
    return MonthReportOut(
        employee_id=r.employee_id, employee_name=r.employee_name, month=r.month,
        rules_note=r.rules_note, total_days=r.total_days,
        present_days=r.present_days, absent_days=r.absent_days,
        late_days=r.late_days, leave_days=r.leave_days, total_hours=r.total_hours,
        ot_hours=r.ot_hours, total_paid=r.total_paid,
        total_expected=r.total_expected, money_at_risk=r.money_at_risk,
        flagged_days=r.flagged_days, summary=r.summary,
        days=[DayVerdictOut(
            day=v.day.isoformat(), day_type=v.day_type.value, check_in=v.check_in,
            check_out=v.check_out, presence_hours=v.presence_hours,
            ot_hours=v.ot_hours, expected_pay=v.expected_pay,
            reported_pay=v.reported_pay, diff=v.diff, rule_flag=v.rule_flag,
            ml_flag=v.ml_flag, status=v.status, reason=v.reason,
            rule_note=v.rule_note) for v in r.days])
