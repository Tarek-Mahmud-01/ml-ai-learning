"""
Month report assembly — domain logic that rolls per-day verdicts into KPIs and
a plain-English summary (template-based, no LLM). Pure Python.
"""
from __future__ import annotations

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
