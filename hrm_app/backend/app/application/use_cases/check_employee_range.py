"""
Use case: check an employee across the LAST N months that have data, and give
one combined good/bad verdict. Reuses CheckEmployeeMonth per month.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from ...domain.entities import MonthReport
from ...domain.repositories import AttendanceRepository, EmployeeRepository
from ...domain.services.anomaly import AnomalyDetector
from ...domain.services.payroll_rules import PayrollRulesService
from .check_employee_month import CheckEmployeeMonth, EmployeeNotFound


@dataclass
class RangeReport:
    employee_id: str
    employee_name: str
    months: list[MonthReport] = field(default_factory=list)
    summary: str = ""
    flagged_days: int = 0
    money_at_risk: float = 0.0


class CheckEmployeeRange:
    def __init__(self, employees: EmployeeRepository,
                 attendance: AttendanceRepository, rules: PayrollRulesService,
                 detector: AnomalyDetector) -> None:
        self._e = employees
        self._a = attendance
        self._rules = rules
        self._detector = detector

    def execute(self, employee_id: str, months: int = 2) -> RangeReport:
        emp = self._e.get(employee_id)
        if emp is None:
            raise EmployeeNotFound(employee_id)

        available = self._a.list_months(employee_id)     # sorted ascending
        if not available:
            return RangeReport(emp.id, emp.name,
                               summary=f"{emp.name} ({emp.id}) has no attendance data yet.")

        chosen = available[-max(1, months):]
        checker = CheckEmployeeMonth(self._e, self._a, self._rules, self._detector)
        reports = [checker.execute(emp.id, y, m) for (y, m) in chosen]

        flagged = sum(r.flagged_days for r in reports)
        risk = round(sum(r.money_at_risk for r in reports), 2)
        paid = round(sum(r.total_paid for r in reports), 2)
        expected = round(sum(r.total_expected for r in reports), 2)
        span = ", ".join(r.month for r in reports)

        lines = [
            f"{emp.name} ({emp.id}) — {len(reports)} month(s) checked ({span}):",
            f"paid ${paid:,.2f} vs expected ${expected:,.2f}.",
        ]
        if flagged == 0:
            lines.append("Everything looks GOOD ✅ — no problem days found.")
        else:
            lines.append(
                f"Found {flagged} problem day(s), ${risk:,.2f} at risk. Details below.")
        for r in reports:
            tag = "OK" if r.flagged_days == 0 else f"{r.flagged_days} flagged, ${r.money_at_risk:,.2f}"
            lines.append(f"• {r.month}: {r.present_days} present, "
                         f"{r.absent_days} absent, {r.late_days} late — {tag}")

        if months > len(available):
            lines.append(f"(only {len(available)} month(s) of data exist for {emp.id})")

        return RangeReport(emp.id, emp.name, reports, "\n".join(lines), flagged, risk)
