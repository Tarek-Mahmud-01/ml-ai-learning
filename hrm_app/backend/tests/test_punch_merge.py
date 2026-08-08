"""
Pure tests for the punch-merge rule + seconds-aware parse_hour. No DB/framework.
Run from the backend folder:  python -m pytest tests/ -q
"""
from datetime import datetime

from app.domain.services.punch_merge import (
    collapse_punches,
    reduce_day,
)
from app.domain.value_objects import DayType, EmployeeRules, parse_hour

rules = EmployeeRules.default()   # shift 9h, late_after 09:15


def _p(hh, mm, ss=0):
    return datetime(2025, 7, 31, hh, mm, ss)


def test_parse_hour_handles_seconds():
    # Real biometric times carry seconds and must not crash.
    assert abs(parse_hour("07:01:27") - (7 + 1 / 60 + 27 / 3600)) < 1e-6
    assert parse_hour("09:00:00") == 9.0
    assert parse_hour("29:00") == 29.0   # past-midnight still works


def test_burst_within_window_collapses_to_one():
    # The real '11 punches in 36 s' burst -> a single kept punch.
    burst = [_p(6, 57, 58), _p(6, 58, 0), _p(6, 58, 1), _p(6, 58, 4),
             _p(6, 58, 23), _p(6, 58, 34)]
    assert len(collapse_punches(burst, 60)) == 1
    # A single all-day burst = checked in but never out -> missing punch.
    day = reduce_day(burst, rules, 60)
    assert day.day_type == DayType.MISSING_PUNCH
    assert day.check_in == "06:57" and day.check_out is None
    assert day.punches_seen == 6 and day.punches_kept == 1


def test_normal_day_first_in_last_out_overtime():
    # Morning double-tap (burst) + an evening punch -> one in, one out.
    punches = [_p(7, 3, 25), _p(7, 3, 26), _p(19, 1, 15)]
    day = reduce_day(punches, rules, 60)
    assert day.check_in == "07:03"
    assert day.check_out == "19:01"
    assert 11.9 < day.presence_hours < 12.1
    assert day.day_type == DayType.OVERTIME   # 12h > 9h shift
    assert day.punches_kept == 2


def test_half_day_and_late_and_present_inference():
    half = reduce_day([_p(9, 0), _p(12, 0)], rules, 60)
    assert half.day_type == DayType.HALF_DAY          # 3h < 5h

    late = reduce_day([_p(9, 30), _p(17, 30)], rules, 60)
    assert late.day_type == DayType.LATE              # in after 09:15, 8h

    present = reduce_day([_p(9, 0), _p(17, 0)], rules, 60)
    assert present.day_type == DayType.PRESENT        # on time, 8h, no OT


def test_merge_window_is_configurable():
    two = [_p(9, 0, 0), _p(9, 1, 30)]   # 90 seconds apart
    assert len(collapse_punches(two, 60)) == 2    # 90s > 60s -> both kept
    assert len(collapse_punches(two, 120)) == 1   # 90s <= 120s -> merged


def test_no_punches_returns_none():
    assert reduce_day([], rules, 60) is None
