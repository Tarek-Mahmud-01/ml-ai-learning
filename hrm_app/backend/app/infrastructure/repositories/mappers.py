"""Translate between ORM rows (infrastructure) and domain entities."""
from __future__ import annotations

from ...domain.entities import AttendanceDay, Employee
from ...domain.value_objects import DayType, EmployeeRules
from ..db.models import AttendanceModel, EmployeeModel


def employee_to_domain(m: EmployeeModel) -> Employee:
    weekend = frozenset(
        int(x) for x in str(m.weekend_days).split(",") if x.strip() != "")
    rules = EmployeeRules(
        base_rate=m.base_rate, ot_rate=m.ot_rate, shift_hours=m.shift_hours,
        work_goal=m.work_goal, lunch=m.lunch, tolerance=m.tolerance,
        shift_start=m.shift_start, late_after=m.late_after,
        weekend_days=weekend,
    )
    return Employee(id=m.id, name=m.name, rules=rules)


def employee_to_orm(e: Employee) -> EmployeeModel:
    r = e.rules
    return EmployeeModel(
        id=e.id, name=e.name, base_rate=r.base_rate, ot_rate=r.ot_rate,
        shift_hours=r.shift_hours, work_goal=r.work_goal, lunch=r.lunch,
        tolerance=r.tolerance, shift_start=r.shift_start, late_after=r.late_after,
        weekend_days=",".join(str(d) for d in sorted(r.weekend_days)),
    )


def attendance_to_domain(m: AttendanceModel) -> AttendanceDay:
    return AttendanceDay(
        employee_id=m.employee_id, day=m.day, day_type=DayType(m.day_type),
        check_in=m.check_in, check_out=m.check_out, reported_pay=m.reported_pay,
    )


def attendance_to_orm(a: AttendanceDay) -> AttendanceModel:
    return AttendanceModel(
        employee_id=a.employee_id, day=a.day, day_type=a.day_type.value,
        check_in=a.check_in, check_out=a.check_out, reported_pay=a.reported_pay,
    )
