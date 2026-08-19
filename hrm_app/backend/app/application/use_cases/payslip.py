"""
Use case: build one employee's payslip for a month — a pay statement (base +
overtime + gross vs actually paid) plus the audit status. Reuses
CheckEmployeeMonth for the totals and audit flags.
"""
from __future__ import annotations

from ...domain.repositories import AttendanceRepository, EmployeeRepository
from ...domain.services.anomaly import AnomalyDetector
from ...domain.services.payroll_rules import PayrollRulesService
from ...domain.services.report import PayslipStatement, build_payslip
from .check_employee_month import CheckEmployeeMonth, EmployeeNotFound


class Payslip:
    def __init__(self, employees: EmployeeRepository,
                 attendance: AttendanceRepository, rules: PayrollRulesService,
                 detector: AnomalyDetector) -> None:
        self._e = employees
        self._a = attendance
        self._rules = rules
        self._detector = detector

    def execute(self, employee_id: str, year: int, month: int) -> PayslipStatement:
        emp = self._e.get(employee_id)
        if emp is None:
            raise EmployeeNotFound(employee_id)
        report = CheckEmployeeMonth(
            self._e, self._a, self._rules, self._detector
        ).execute(employee_id, year, month)
        return build_payslip(report, emp.rules.ot_rate)
