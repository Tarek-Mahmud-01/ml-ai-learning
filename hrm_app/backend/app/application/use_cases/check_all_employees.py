"""
Use case: check EVERY employee for one month and build a roster — one line per
employee (paid, expected, present/absent/late, flagged, status). The agent's
list_* queries (unpaid / absent / issues / paid) are filtered views of this.
Reuses CheckEmployeeMonth so the rules + ML logic is identical to a single check.
"""
from __future__ import annotations

from ...domain.repositories import AttendanceRepository, EmployeeRepository
from ...domain.services.anomaly import AnomalyDetector
from ...domain.services.payroll_rules import PayrollRulesService
from ...domain.services.report import RosterReport, build_roster
from .check_employee_month import CheckEmployeeMonth


class CheckAllEmployees:
    def __init__(self, employees: EmployeeRepository,
                 attendance: AttendanceRepository, rules: PayrollRulesService,
                 detector: AnomalyDetector) -> None:
        self._e = employees
        self._a = attendance
        self._rules = rules
        self._detector = detector

    def execute(self, year: int, month: int) -> RosterReport:
        checker = CheckEmployeeMonth(self._e, self._a, self._rules, self._detector)
        reports = []
        for emp in self._e.list_all():
            rep = checker.execute(emp.id, year, month)
            if rep.total_days > 0:          # only staff who have data that month
                reports.append(rep)
        return build_roster(f"{year:04d}-{month:02d}", reports)
