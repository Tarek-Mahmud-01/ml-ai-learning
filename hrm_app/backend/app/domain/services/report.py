"""
Month report assembly — domain logic that rolls per-day verdicts into KPIs and
a plain-English summary (template-based, no LLM). Pure Python.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from ..entities import DayVerdict, MonthReport
from ..value_objects import DayType


def summarize_month(
    employee_id: str,
    employee_name: str,
    month: str,
    rules_note: str,
    verdicts: list[DayVerdict],
) -> MonthReport:
    """Fold the day verdicts into a MonthReport with KPIs + summary."""
    report = MonthReport(
        employee_id=employee_id,
        employee_name=employee_name,
        month=month,
        rules_note=rules_note,
        days=verdicts,
    )

    report.total_days = len(verdicts)
    report.present_days = sum(
        1 for v in verdicts
        if v.day_type in (DayType.PRESENT, DayType.LATE,
                          DayType.HALF_DAY, DayType.OVERTIME))
    report.absent_days = sum(1 for v in verdicts if v.day_type == DayType.ABSENT)
    report.late_days = sum(1 for v in verdicts if v.day_type == DayType.LATE)
    report.leave_days = sum(1 for v in verdicts if v.day_type == DayType.LEAVE)
    report.total_hours = round(sum(v.presence_hours for v in verdicts), 2)
    report.ot_hours = round(sum(v.ot_hours for v in verdicts), 2)
    report.total_paid = round(sum(v.reported_pay for v in verdicts), 2)
    report.total_expected = round(sum(v.expected_pay for v in verdicts), 2)
    flagged = [v for v in verdicts if v.rule_flag or v.ml_flag]
    report.flagged_days = len(flagged)
    report.money_at_risk = round(sum(abs(v.diff) for v in flagged), 2)

    report.summary = _write_summary(report, flagged)
    return report


def _write_summary(r: MonthReport, flagged: list[DayVerdict]) -> str:
    """One plain-English paragraph an admin can read at a glance."""
    parts = [
        f"{r.employee_name} ({r.employee_id}) — {r.month}:",
        f"worked {r.present_days} days, absent {r.absent_days},",
        f"late {r.late_days}, leave {r.leave_days}.",
        f"Paid ${r.total_paid:,.2f} vs expected ${r.total_expected:,.2f}.",
    ]
    if flagged:
        parts.append(
            f"{r.flagged_days} day(s) flagged — money at risk ${r.money_at_risk:,.2f}.")
    else:
        parts.append("No problems found.")
    return " ".join(parts)


# --- Roster: a one-line-per-employee view of a whole month (agent queries) ---
@dataclass
class RosterRow:
    employee_id: str
    employee_name: str
    present_days: int
    absent_days: int
    late_days: int
    total_paid: float
    total_expected: float
    flagged_days: int
    money_at_risk: float
    status: str          # "OK" or "ISSUES"
    is_paid: bool
    ot_hours: float = 0.0
    total_hours: float = 0.0


@dataclass
class RosterReport:
    month: str
    rows: list[RosterRow] = field(default_factory=list)

    def unpaid(self) -> list["RosterRow"]:      # worked but received no pay
        return [r for r in self.rows if not r.is_paid and r.present_days > 0]

    def paid(self) -> list["RosterRow"]:
        return [r for r in self.rows if r.is_paid]

    def with_absences(self) -> list["RosterRow"]:
        return [r for r in self.rows if r.absent_days > 0]

    def with_issues(self) -> list["RosterRow"]:  # rule breaks / ML flags / fines
        return [r for r in self.rows if r.flagged_days > 0]


def build_roster(month: str, reports: list[MonthReport]) -> RosterReport:
    rows = [
        RosterRow(
            employee_id=r.employee_id, employee_name=r.employee_name,
            present_days=r.present_days, absent_days=r.absent_days,
            late_days=r.late_days, total_paid=r.total_paid,
            total_expected=r.total_expected, flagged_days=r.flagged_days,
            money_at_risk=r.money_at_risk,
            status="ISSUES" if r.flagged_days else "OK",
            is_paid=r.total_paid > 0,
            ot_hours=r.ot_hours,
            total_hours=r.total_hours,
        )
        for r in reports
    ]
    return RosterReport(month=month, rows=rows)


# --- Payslip: a printable pay statement (base + OT + net) plus audit status ---
@dataclass
class PayslipStatement:
    employee_id: str
    employee_name: str
    month: str
    worked_days: int
    total_hours: float
    ot_hours: float
    base_pay: float
    ot_pay: float
    gross_pay: float
    paid: float
    flagged_days: int
    status: str
    text: str


def build_payslip(report: MonthReport, ot_rate: float) -> PayslipStatement:
    ot_pay = round(report.ot_hours * ot_rate, 2)
    gross = report.total_expected
    base_pay = round(gross - ot_pay, 2)
    status = "OK" if report.flagged_days == 0 else "NEEDS REVIEW"
    text = "\n".join([
        f"PAYSLIP — {report.employee_name} ({report.employee_id})",
        f"Month: {report.month}",
        f"Worked days: {report.present_days}   "
        f"Hours: {report.total_hours:.1f} (OT {report.ot_hours:.1f})",
        f"Base pay ....... ${base_pay:,.2f}",
        f"Overtime pay ... ${ot_pay:,.2f}",
        f"Gross pay ...... ${gross:,.2f}",
        f"Actually paid .. ${report.total_paid:,.2f}",
        f"Audit: {status}"
        + (f" ({report.flagged_days} day(s) flagged)" if report.flagged_days else ""),
    ])
    return PayslipStatement(
        employee_id=report.employee_id, employee_name=report.employee_name,
        month=report.month, worked_days=report.present_days,
        total_hours=report.total_hours, ot_hours=report.ot_hours,
        base_pay=base_pay, ot_pay=ot_pay, gross_pay=gross,
        paid=report.total_paid, flagged_days=report.flagged_days,
        status=status, text=text)
