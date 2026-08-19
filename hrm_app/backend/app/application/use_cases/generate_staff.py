"""
Use case: bulk-create N demo employees (additive — never clears real data), and
optionally give them a full month of generated salary/attendance. Reuses
seed_month.synth_attendance so demo generation lives in one place.

IDs use an E9xxx range (E9001, E9002, ...) so they never collide with the demo
staff (E100-E111) or the real imported staff (E100017), and still match the
chat's employee-id pattern.
"""
from __future__ import annotations

import numpy as np

from ...domain.entities import Employee
from ...domain.repositories import AttendanceRepository, EmployeeRepository
from ...domain.services.payroll_rules import PayrollRulesService
from ...domain.value_objects import EmployeeRules
from .seed_month import synth_attendance

_DEMO_NAMES = ["Arjun", "Priya", "Sanjay", "Meera", "Rohit", "Divya", "Kabir",
               "Anaya", "Vikram", "Isha", "Aditya", "Neha", "Farhan", "Zoya",
               "Omar", "Lila", "Bilal", "Sara", "Nabil", "Ruma"]


class GenerateStaff:
    def __init__(self, employees: EmployeeRepository,
                 attendance: AttendanceRepository,
                 rules: PayrollRulesService) -> None:
        self._e = employees
        self._a = attendance
        self._rules = rules

    def execute(self, count: int, year: int | None = None, month: int | None = None,
                base_rate: float = 20.0, ot_rate: float = 30.0) -> dict:
        count = max(1, min(int(count), 100))
        existing = {e.id for e in self._e.list_all()}
        rng = np.random.default_rng()

        made: list[Employee] = []
        n = 9000
        while len(made) < count:
            n += 1
            eid = f"E{n}"
            if eid in existing:
                continue
            name = _DEMO_NAMES[(n - 9001) % len(_DEMO_NAMES)]
            emp = Employee(eid, name, EmployeeRules(base_rate=base_rate, ot_rate=ot_rate))
            self._e.add(emp)
            existing.add(eid)
            made.append(emp)

        days = 0
        if year and month:
            all_days = []
            for e in made:
                d, _ = synth_attendance(e, year, month, rng, self._rules)
                all_days.extend(d)
            if all_days:
                self._a.add_many(all_days)
            days = len(all_days)

        return {
            "employees": len(made),
            "ids": [e.id for e in made],
            "attendance_days": days,
            "month": f"{year:04d}-{month:02d}" if year and month else None,
        }
