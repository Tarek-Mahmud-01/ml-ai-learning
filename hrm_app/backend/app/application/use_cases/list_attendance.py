"""
Use case: show an employee's recent attendance days (date, type, in/out, pay).
Defaults to their most recent month with data; a specific month can be given.
"""
from __future__ import annotations

from ...domain.repositories import AttendanceRepository, EmployeeRepository
from .check_employee_month import EmployeeNotFound


class ListAttendance:
    def __init__(self, employees: EmployeeRepository,
                 attendance: AttendanceRepository) -> None:
        self._e = employees
        self._a = attendance

    def execute(self, employee_id: str, year: int | None = None,
                month: int | None = None, limit: int = 20) -> str:
        emp = self._e.get(employee_id)
        if emp is None:
            raise EmployeeNotFound(employee_id)

        if year and month:
            days = self._a.list_for_month(employee_id, year, month)
            when = f"{year:04d}-{month:02d}"
        else:
            months = self._a.list_months(employee_id)
            if not months:
                return f"{emp.name} ({emp.id}) has no attendance records yet."
            y, m = months[-1]                      # most recent month with data
            days = self._a.list_for_month(employee_id, y, m)
            when = f"{y:04d}-{m:02d}"

        days = sorted(days, key=lambda d: d.day, reverse=True)[:limit]
        if not days:
            return f"No attendance found for {emp.name} ({emp.id}) in {when}."
        total = sum(d.reported_pay for d in days)
        lines = [f"{emp.name} ({emp.id}) — last {len(days)} day(s) of {when} "
                 f"(total ${total:,.2f}):"]
        for d in days:
            lines.append(
                f"• {d.day} {d.day_type.value}: "
                f"{d.check_in or '—'}–{d.check_out or '—'}, pay ${d.reported_pay:.2f}")
        return "\n".join(lines)
