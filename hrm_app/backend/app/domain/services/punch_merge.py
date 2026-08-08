"""
Punch-merge rule — pure domain (stdlib only, no framework/DB/ML imports).

Real biometric devices store EVERY read as its own row, so one finger-tap becomes
a burst of punches a few seconds apart (e.g. 11 punches in 36 s). This service is
the new HRM rule the user asked for:

  1. collapse a burst into ONE punch  ("count only one in / one out"), then
  2. reduce an employee's day to a single check-in (first punch) and check-out
     (last punch), and
  3. infer the day type from the result.

It works on a single employee-day's punch datetimes; grouping by employee/day is
the caller's job.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from ..value_objects import DayType, EmployeeRules, parse_hour

HALF_DAY_MAX_HOURS = 5.0   # a worked day shorter than this is treated as a half day


@dataclass(frozen=True)
class MergedDay:
    """One employee-day reduced from many raw punches."""
    check_in: str | None       # "HH:MM" of the first kept punch
    check_out: str | None      # "HH:MM" of the last kept punch (may exceed 24:00)
    day_type: DayType
    presence_hours: float
    punches_seen: int          # raw punches in the group (before merge)
    punches_kept: int          # punches left after collapsing bursts


def collapse_punches(punches: list[datetime], merge_seconds: float) -> list[datetime]:
    """
    Drop any punch within `merge_seconds` of the previous KEPT punch, so a rapid
    burst counts as a single punch event. Input need not be sorted.
    """
    kept: list[datetime] = []
    for ts in sorted(punches):
        if not kept or (ts - kept[-1]).total_seconds() > merge_seconds:
            kept.append(ts)
    return kept


def _fmt_hours(hf: float) -> str:
    """
    Float hours -> 'HH:MM' (allows >24:00 for a shift that ran past midnight).
    Seconds are truncated so the string shows the clock minute actually reached
    (07:01:59 -> '07:01'); the tiny epsilon absorbs float rounding error.
    """
    total_min = int(hf * 60 + 1e-9)
    hh, mm = divmod(total_min, 60)
    return f"{hh:02d}:{mm:02d}"


def reduce_day(punches: list[datetime], rules: EmployeeRules,
               merge_seconds: float) -> MergedDay | None:
    """
    Reduce one employee-day's raw punches to a single in/out + inferred day type.
    Returns None when there are no punches at all.

    - 0 punches            -> None (caller creates no row)
    - 1 punch (after merge) -> MISSING_PUNCH (checked in, never out; can't verify)
    - 2+ punches           -> first = check-in, last = check-out; day type inferred
    """
    seen = len(punches)
    kept = collapse_punches(punches, merge_seconds)
    if not kept:
        return None

    first = kept[0]
    first_hf = first.hour + first.minute / 60.0 + first.second / 3600.0
    check_in = _fmt_hours(first_hf)

    if len(kept) == 1:
        return MergedDay(check_in, None, DayType.MISSING_PUNCH, 0.0, seen, 1)

    last = kept[-1]
    presence = (last - first).total_seconds() / 3600.0
    # Rebuild check-out from first + presence so a shift past midnight keeps the
    # >24:00 convention (e.g. in 22:00, presence 9 -> "31:00").
    check_out = _fmt_hours(first_hf + presence)

    late_after = parse_hour(rules.late_after) or 0.0
    if presence < HALF_DAY_MAX_HOURS:
        day_type = DayType.HALF_DAY
    elif presence > rules.shift_hours:
        day_type = DayType.OVERTIME
    elif first_hf > late_after:
        day_type = DayType.LATE
    else:
        day_type = DayType.PRESENT

    return MergedDay(check_in, check_out, day_type, round(presence, 2), seen, len(kept))
