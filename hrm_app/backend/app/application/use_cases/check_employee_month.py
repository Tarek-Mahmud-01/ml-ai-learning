"""
Use case: check ONE employee's month = rules brain + ML brain per day, then
roll up into a MonthReport. Pure orchestration — the logic lives in the domain
services it calls.
"""
from __future__ import annotations

from ...domain.entities import DayVerdict, MonthReport
from ...domain.repositories import AttendanceRepository, EmployeeRepository
from ...domain.services.anomaly import AnomalyDetector, build_status
from ...domain.services.payroll_rules import PayrollRulesService
from ...domain.services.report import summarize_month
from ...domain.value_objects import DayFeatures

_WD = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


class EmployeeNotFound(Exception):
    pass


class CheckEmployeeMonth:
    def __init__(
        self,
        employees: EmployeeRepository,
        attendance: AttendanceRepository,
        rules: PayrollRulesService,
        detector: AnomalyDetector,
    ) -> None:
        self._employees = employees
        self._attendance = attendance
        self._rules = rules
        self._detector = detector

    def execute(self, employee_id: str, year: int, month: int) -> MonthReport:
        emp = self._employees.get(employee_id)
        if emp is None:
            raise EmployeeNotFound(employee_id)

        days = sorted(
            self._attendance.list_for_month(employee_id, year, month),
            key=lambda d: d.day,
        )

        verdicts: list[DayVerdict] = []
        for day in days:
            outcome = self._rules.check_day(day, emp.rules)

            # ML complements rules ONLY on worked days (there's presence to judge).
            ml_flag = False
            if outcome.presence_hours > 0:
                ml_flag = self._detector.is_wrong(
                    DayFeatures(outcome.presence_hours, day.reported_pay))

            verdicts.append(DayVerdict(
                day=day.day,
                day_type=day.day_type,
                check_in=day.check_in,
                check_out=day.check_out,
                presence_hours=outcome.presence_hours,
                ot_hours=outcome.ot_hours,
                expected_pay=outcome.expected_pay,
                reported_pay=day.reported_pay,
                diff=outcome.diff,
                rule_flag=outcome.rule_flag,
                ml_flag=ml_flag,
                status=build_status(outcome.rule_flag, ml_flag),
                reason=outcome.reason,
                rule_note=outcome.rule_note,
            ))

        return summarize_month(
            emp.id, emp.name, f"{year:04d}-{month:02d}",
            self._rules_note(emp), verdicts)

    @staticmethod
    def _rules_note(emp) -> str:
        r = emp.rules
        weekend = "/".join(_WD[d] for d in sorted(r.weekend_days))
        return (f"{emp.name} contract: ${r.base_rate:.0f}/h base, "
                f"${r.ot_rate:.0f}/h OT, start {r.shift_start}, weekend {weekend}")
