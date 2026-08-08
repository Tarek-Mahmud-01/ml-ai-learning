"""
Pure domain tests — no DB, no framework, no ML. Proves the rules brain.
Run from the backend folder:  python -m pytest tests/ -q
"""
from datetime import date

from app.domain.entities import AttendanceDay
from app.domain.services.anomaly import build_status
from app.domain.services.payroll_rules import PayrollRulesService
from app.domain.value_objects import DayType, EmployeeRules, parse_hour

svc = PayrollRulesService()
rules = EmployeeRules.default()


def _day(day_type, ci, co, pay):
    return AttendanceDay("E100", date(2024, 6, 3), day_type, ci, co, pay)


def test_parse_hour_supports_past_midnight():
    assert parse_hour("29:00") == 29.0
    assert parse_hour("09:30") == 9.5
    assert parse_hour(None) is None
    assert parse_hour("") is None


def test_known_correct_pay_cases():
    # 9h→160, 10h→190, 8h→140, 11h→220
    assert svc.check_day(_day(DayType.PRESENT, "09:00", "18:00", 160), rules).expected_pay == 160
    assert svc.check_day(_day(DayType.OVERTIME, "09:00", "19:00", 190), rules).expected_pay == 190
    assert svc.check_day(_day(DayType.PRESENT, "09:00", "17:00", 140), rules).expected_pay == 140
    assert svc.check_day(_day(DayType.OVERTIME, "09:00", "20:00", 220), rules).expected_pay == 220


def test_correct_pay_not_flagged():
    out = svc.check_day(_day(DayType.PRESENT, "09:00", "18:00", 160), rules)
    assert out.rule_flag is False


def test_underpaid_and_overpaid_flagged():
    under = svc.check_day(_day(DayType.PRESENT, "09:00", "18:00", 100), rules)
    assert under.rule_flag and under.diff < 0
    over = svc.check_day(_day(DayType.PRESENT, "09:00", "18:00", 250), rules)
    assert over.rule_flag and over.diff > 0


def test_absent_day_should_have_no_pay():
    ok = svc.check_day(_day(DayType.ABSENT, None, None, 0), rules)
    assert ok.rule_flag is False
    bad = svc.check_day(_day(DayType.ABSENT, None, None, 160), rules)
    assert bad.rule_flag is True  # paid on an unpaid day


def test_leave_is_paid_base_day():
    out = svc.check_day(_day(DayType.LEAVE, None, None, 160), rules)
    assert out.expected_pay == 160 and out.rule_flag is False


def test_weekend_pay_is_flagged():
    out = svc.check_day(_day(DayType.WEEKEND, None, None, 160), rules)
    assert out.rule_flag is True


def test_impossible_hours_passes_rules_but_ml_catches():
    # 20h presence paid "correctly" (490) → rules see no diff...
    out = svc.check_day(_day(DayType.OVERTIME, "09:00", "29:00", 490), rules)
    assert out.presence_hours == 20 and out.rule_flag is False
    # ...but the combined status must escalate when ML flags it.
    assert build_status(rule_flag=out.rule_flag, ml_flag=True) == "ML-FLAG"


def test_per_employee_rules_change_expected():
    rich = EmployeeRules(base_rate=25, ot_rate=35)
    out = svc.check_day(_day(DayType.PRESENT, "09:00", "18:00", 200), rich)
    assert out.expected_pay == 200  # 8h * 25 = 200 (different from default 160)
