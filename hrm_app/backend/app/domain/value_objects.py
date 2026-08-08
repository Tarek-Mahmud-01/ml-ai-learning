"""
Domain value objects — pure Python, immutable, no framework/DB/ML imports.

A "value object" has no identity; it is defined only by its values (two Money
of $5 are equal). These encode the *vocabulary* of the payroll domain.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class DayType(str, Enum):
    """The kind of day an attendance record represents."""
    PRESENT = "present"
    LATE = "late"
    HALF_DAY = "half_day"
    OVERTIME = "overtime"
    ABSENT = "absent"          # no punch, unpaid
    LEAVE = "leave"            # approved, paid, no punch
    WEEKEND = "weekend"        # no work expected
    HOLIDAY = "holiday"        # no work expected
    MISSING_PUNCH = "missing_punch"  # checked in but no check-out


# Day types where the worker is not expected to physically attend.
NO_WORK_DAYS = {DayType.ABSENT, DayType.LEAVE, DayType.WEEKEND, DayType.HOLIDAY}


def parse_hour(value: str | None) -> float | None:
    """
    Read a clock string as a number of hours.

    Accepts 'HH:MM' and 'HH:MM:SS' (real biometric punches carry seconds, e.g.
    '07:01:27'). Supports values past midnight (e.g. '29:00' -> 29.0) so an
    impossible 20-hour shift is representable rather than crashing. Returns None
    when there is no punch (absent/leave/missing).
    """
    if value is None:
        return None
    text = str(value).strip()
    if text == "" or text.lower() in {"nan", "none", "-"}:
        return None
    parts = text.split(":")
    hh = int(parts[0])
    mm = int(parts[1]) if len(parts) > 1 and parts[1] != "" else 0
    ss = int(parts[2]) if len(parts) > 2 and parts[2] != "" else 0
    return hh + mm / 60.0 + ss / 3600.0


@dataclass(frozen=True)
class EmployeeRules:
    """
    The pay policy for ONE employee (the "careful" per-employee requirement).

    A global default exists; each employee may override any field via their
    own contract. All money/time math in the domain reads these values — never
    hard-coded constants.
    """
    base_rate: float = 20.0          # $ per worked hour (capped at work_goal)
    ot_rate: float = 30.0            # $ per overtime hour (presence beyond shift_hours)
    shift_hours: float = 9.0         # full shift = work_goal + lunch
    work_goal: float = 8.0           # max paid work hours at base rate
    lunch: float = 1.0               # unpaid lunch hours
    tolerance: float = 0.01          # pay diff allowed before "wrong"
    shift_start: str = "09:00"       # expected check-in time
    late_after: str = "09:15"        # check-in later than this = late
    # weekday numbers that are the weekend (Mon=0 .. Sun=6). Default Sat/Sun.
    weekend_days: frozenset[int] = field(default_factory=lambda: frozenset({5, 6}))

    @classmethod
    def default(cls) -> "EmployeeRules":
        return cls()


@dataclass(frozen=True)
class DayFeatures:
    """
    The neutral, framework-free inputs an anomaly detector needs for one day.

    The domain speaks in these terms; the infrastructure ML adapter is
    responsible for turning them into the model's exact feature vector.
    """
    presence_hours: float
    reported_pay: float

    @property
    def pay_per_hour(self) -> float:
        return self.reported_pay / self.presence_hours if self.presence_hours else 0.0
