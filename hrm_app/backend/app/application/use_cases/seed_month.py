"""
Use case: generate demo data — employees with per-employee rules + a full month
of attendance covering real edge cases (present/late/half/absent/leave/weekend/
overtime/missing-punch) with a slice of hidden fraud for the detective to catch.

`synth_attendance` (module function) generates ONE employee's month and is reused
by GenerateStaff so demo generation stays in one place.
"""
from __future__ import annotations

import calendar
from datetime import date

import numpy as np

from ...domain.entities import AttendanceDay, Employee
from ...domain.repositories import AttendanceRepository, EmployeeRepository
from ...domain.services.payroll_rules import PayrollRulesService
from ...domain.value_objects import DayType, EmployeeRules

NAMES = ["Ayesha", "Rahim", "Karim", "Fatima", "Hasan", "Nadia",
         "Imran", "Sadia", "Tariq", "Mona", "Bilal", "Zara"]


def _fmt(hour: float) -> str:
    h = int(hour)
    m = int(round((hour - h) * 60))
    return f"{h:02d}:{m:02d}"


def synth_attendance(
    emp: Employee, year: int, month: int, rng, rules: PayrollRulesService,
) -> tuple[list[AttendanceDay], int]:
    """Generate one employee's month of attendance. Returns (days, fraud_count)."""
    days_in_month = calendar.monthrange(year, month)[1]
    start_hour = int(emp.rules.shift_start.split(":")[0])
    leave_pay = round(emp.rules.work_goal * emp.rules.base_rate, 2)
    out: list[AttendanceDay] = []
    fraud = 0

    for dnum in range(1, days_in_month + 1):
        d = date(year, month, dnum)

        # Weekend for THIS employee's contract
        if d.weekday() in emp.rules.weekend_days:
            pay = 0.0
            if rng.random() < 0.02:      # rare weekend-pay fraud
                pay = leave_pay
                fraud += 1
            out.append(AttendanceDay(emp.id, d, DayType.WEEKEND, None, None, pay))
            continue

        roll = rng.random()
        if roll < 0.05:                  # absent (unpaid)
            pay = 0.0
            if rng.random() < 0.15:      # sometimes paid while absent (fraud)
                pay = leave_pay
                fraud += 1
            out.append(AttendanceDay(emp.id, d, DayType.ABSENT, None, None, pay))
            continue
        if roll < 0.08:                  # approved paid leave
            out.append(AttendanceDay(emp.id, d, DayType.LEAVE, None, None, leave_pay))
            continue
        if roll < 0.10:                  # forgot to check out
            out.append(AttendanceDay(
                emp.id, d, DayType.MISSING_PUNCH, _fmt(start_hour), None, 0.0))
            continue

        # A worked day — pick a subtype
        sub = rng.random()
        if sub < 0.12:
            dtype, ci_hour, presence = DayType.HALF_DAY, start_hour, 4
        elif sub < 0.30:
            dtype, ci_hour, presence = DayType.OVERTIME, start_hour, int(rng.choice([10, 11]))
        elif sub < 0.45:
            dtype, ci_hour, presence = DayType.LATE, start_hour + 1, 8
        else:
            dtype, ci_hour, presence = DayType.PRESENT, start_hour, int(rng.choice([9, 9, 9, 8]))

        check_in = _fmt(ci_hour)
        check_out = _fmt(ci_hour + presence)
        expected = rules.expected_pay(presence, emp.rules)
        pay = expected

        # Hidden fraud on worked days (~7%)
        fr = rng.random()
        if fr < 0.03:                    # underpaid
            pay = round(expected * rng.uniform(0.4, 0.7), 2)
            fraud += 1
        elif fr < 0.06:                  # overpaid
            pay = round(expected * rng.uniform(1.4, 2.0), 2)
            fraud += 1
        elif fr < 0.07:                  # impossible hours (rules pass, ML must catch)
            presence = 20
            check_out = _fmt(ci_hour + 20)
            pay = rules.expected_pay(20, emp.rules)
            dtype = DayType.OVERTIME
            fraud += 1

        out.append(AttendanceDay(emp.id, d, dtype, check_in, check_out, round(pay, 2)))

    return out, fraud


class SeedMonth:
    def __init__(
        self,
        employees: EmployeeRepository,
        attendance: AttendanceRepository,
        rules: PayrollRulesService,
    ) -> None:
        self._employees = employees
        self._attendance = attendance
        self._rules = rules

    def execute(self, year: int, month: int) -> dict:
        self._attendance.clear()
        self._employees.clear()

        rng = np.random.default_rng(42)
        employees = self._make_employees()
        for e in employees:
            self._employees.add(e)

        all_days: list[AttendanceDay] = []
        fraud = 0
        for e in employees:
            days, f = synth_attendance(e, year, month, rng, self._rules)
            all_days.extend(days)
            fraud += f

        self._attendance.add_many(all_days)
        return {
            "month": f"{year:04d}-{month:02d}",
            "employees": len(employees),
            "attendance_days": len(all_days),
            "injected_fraud": fraud,
        }

    @staticmethod
    def _make_employees() -> list[Employee]:
        emps: list[Employee] = []
        for i, name in enumerate(NAMES):
            eid = f"E{100 + i:03d}"
            if i == 1:      # higher-paid, later start
                rules = EmployeeRules(base_rate=25, ot_rate=35, shift_start="10:00")
            elif i == 2:    # part-time (4h day)
                rules = EmployeeRules(work_goal=4, base_rate=15, ot_rate=20)
            elif i == 3:    # Fri/Sat weekend
                rules = EmployeeRules(weekend_days=frozenset({4, 5}))
            else:
                rules = EmployeeRules.default()
            emps.append(Employee(eid, name, rules))
        return emps
