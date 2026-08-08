"""Attendance insert / edit / delete / show use cases. 'pay' == payroll field."""
from __future__ import annotations

from datetime import date

from ...domain.entities import AttendanceDay
from ...domain.repositories import AttendanceRepository, EmployeeRepository
from ...domain.value_objects import DayType

_ATT_FIELDS = {"check_in", "check_out", "day_type", "reported_pay"}


def _to_date(day_str: str | None) -> date:
    if not day_str:
        raise ValueError("please give a date like 2024-06-15")
    try:
        return date.fromisoformat(day_str)
    except ValueError:
        raise ValueError(f"'{day_str}' is not a valid date (use YYYY-MM-DD)")


def _to_day_type(value) -> DayType:
    try:
        return DayType(str(value).strip().lower().replace(" ", "_"))
    except ValueError:
        raise ValueError(
            "day type must be one of: present, late, half_day, overtime, "
            "absent, leave, weekend, holiday, missing_punch")


class InsertAttendance:
    def __init__(self, employees: EmployeeRepository,
                 attendance: AttendanceRepository) -> None:
        self._e = employees
        self._a = attendance

    def execute(self, employee_id, day, day_type, check_in, check_out,
                reported_pay) -> AttendanceDay:
        if self._e.get(employee_id) is None:
            raise ValueError(f"{employee_id} not found — add the employee first")
        rec = AttendanceDay(
            employee_id=employee_id,
            day=_to_date(day),
            day_type=_to_day_type(day_type or "present"),
            check_in=check_in,
            check_out=check_out,
            reported_pay=float(reported_pay) if reported_pay is not None else 0.0,
        )
        self._a.upsert_day(rec)
        return rec


class EditAttendance:
    def __init__(self, attendance: AttendanceRepository) -> None:
        self._a = attendance

    def execute(self, employee_id, day, field, value) -> tuple[AttendanceDay, str]:
        if field not in _ATT_FIELDS:
            raise ValueError("I can change: check_in, check_out, day_type, pay")
        if value in (None, ""):
            raise ValueError("please give a value")
        d = _to_date(day)
        rec = self._a.get_day(employee_id, d)
        if rec is None:
            raise ValueError(
                f"no attendance for {employee_id} on {day} — add it first")

        if field == "reported_pay":
            before = f"${rec.reported_pay:.2f}"
            rec.reported_pay = float(value)
            after = f"${rec.reported_pay:.2f}"
        elif field == "day_type":
            before = rec.day_type.value
            rec.day_type = _to_day_type(value)
            after = rec.day_type.value
        else:  # check_in / check_out
            before = getattr(rec, field) or "—"
            setattr(rec, field, str(value).strip())
            after = getattr(rec, field)

        self._a.upsert_day(rec)
        label = "pay" if field == "reported_pay" else field
        return rec, f"{label}: {before} -> {after}"


class DeleteAttendance:
    def __init__(self, attendance: AttendanceRepository) -> None:
        self._a = attendance

    def execute(self, employee_id, day) -> bool:
        d = _to_date(day)
        if not self._a.delete_day(employee_id, d):
            raise ValueError(f"no attendance for {employee_id} on {day}")
        return True


class ShowDay:
    def __init__(self, attendance: AttendanceRepository) -> None:
        self._a = attendance

    def execute(self, employee_id, day) -> AttendanceDay:
        d = _to_date(day)
        rec = self._a.get_day(employee_id, d)
        if rec is None:
            raise ValueError(f"no attendance for {employee_id} on {day}")
        return rec
