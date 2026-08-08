"""
Use case: import a REAL biometric export (ZKTeco BioTime SQL dump) into the app.

Pipeline (orchestration only — the maths live in the domain):
  read raw punches  ->  group by (employee, calendar day)  ->  apply the
  punch-merge rule (collapse bursts, first-in/last-out, infer day type)  ->
  set reported_pay = expected_pay(presence) at a transparent DEFAULT rate
  (the dump has no pay data)  ->  write employees + attendance days.

Because the source has no salary data, pay is an assume-correct baseline the
admin tunes per employee later (chat: "set E100017 base rate to 25"); once real
pay is entered the rules brain flags over/under-payment.
"""
from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime
from typing import Iterable, Protocol

from ...domain.entities import AttendanceDay, Employee
from ...domain.repositories import AttendanceRepository, EmployeeRepository
from ...domain.services.payroll_rules import PayrollRulesService
from ...domain.services.punch_merge import reduce_day
from ...domain.value_objects import EmployeeRules, parse_hour


class PunchRecord(Protocol):
    emp_code: str
    name: str
    ts: datetime


class PunchSource(Protocol):
    """What the importer needs from a punch reader (infra supplies it)."""
    def read_punches(self, path: str) -> Iterable[PunchRecord]: ...


class ImportBioTime:
    def __init__(
        self,
        employees: EmployeeRepository,
        attendance: AttendanceRepository,
        rules: PayrollRulesService,
        reader: PunchSource,
        merge_seconds: int = 60,
        default_base_rate: float = 20.0,
        default_ot_rate: float = 30.0,
    ) -> None:
        self._employees = employees
        self._attendance = attendance
        self._rules = rules
        self._reader = reader
        self._merge_seconds = merge_seconds
        self._base = default_base_rate
        self._ot = default_ot_rate

    def execute(self, path: str, replace: bool = True,
                merge_seconds: int | None = None) -> dict:
        ms = self._merge_seconds if merge_seconds is None else int(merge_seconds)
        if replace:
            self._attendance.clear()
            self._employees.clear()

        default_rules = EmployeeRules(base_rate=self._base, ot_rate=self._ot)

        # Group punches: emp_code -> {day -> [punch datetimes]}; remember names.
        names: dict[str, str] = {}
        by_emp: dict[str, dict[date, list[datetime]]] = defaultdict(
            lambda: defaultdict(list))
        punches_read = 0
        for p in self._reader.read_punches(path):
            punches_read += 1
            names.setdefault(p.emp_code, p.name)
            by_emp[p.emp_code][p.ts.date()].append(p.ts)

        all_days: list[AttendanceDay] = []
        punches_kept = 0
        missing_days = 0
        min_date: date | None = None
        max_date: date | None = None

        for code in sorted(by_emp):
            eid = f"E{code}"
            self._employees.add(Employee(eid, names.get(code, eid), default_rules))

            for d, times in by_emp[code].items():
                merged = reduce_day(times, default_rules, ms)
                if merged is None:
                    continue
                punches_kept += merged.punches_kept
                ci = parse_hour(merged.check_in) or 0.0
                co = parse_hour(merged.check_out)
                if co is None:                    # single punch -> missing punch
                    missing_days += 1
                    presence = 0.0
                else:
                    presence = co - ci
                # No pay in the source: assume-correct pay at the default rate,
                # computed from the SAME HH:MM the rules brain re-reads later, so the
                # baseline shows diff = 0 (not a rounding-cent false mismatch).
                pay = self._rules.expected_pay(presence, default_rules)
                all_days.append(AttendanceDay(
                    eid, d, merged.day_type, merged.check_in, merged.check_out, pay))
                min_date = d if min_date is None or d < min_date else min_date
                max_date = d if max_date is None or d > max_date else max_date

        # After a clear there are no conflicts -> fast bulk insert; otherwise upsert.
        if replace:
            self._attendance.add_many(all_days)
        else:
            for day in all_days:
                self._attendance.upsert_day(day)

        return {
            "employees": len(by_emp),
            "attendance_days": len(all_days),
            "missing_punch_days": missing_days,
            "punches_read": punches_read,
            "punches_kept": punches_kept,
            "punches_merged_away": punches_read - punches_kept,
            "date_from": min_date.isoformat() if min_date else None,
            "date_to": max_date.isoformat() if max_date else None,
            "merge_seconds": ms,
            "default_base_rate": self._base,
            "replaced_demo": replace,
        }
