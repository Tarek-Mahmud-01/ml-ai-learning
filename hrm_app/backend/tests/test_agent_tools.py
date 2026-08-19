"""
Tests for the Phase-4 agent tools: relative-date resolver, roster filters,
payslip breakdown, configure, bulk generate, and the new intent parses.
Pure + fake-repo (no DB / no LLM).
"""
from datetime import date

import pytest

from app.application.use_cases.configure import Configure
from app.application.use_cases.generate_staff import GenerateStaff
from app.domain.entities import Employee, MonthReport
from app.domain.services.chat_intents import parse, resolve_month
from app.domain.services.payroll_rules import PayrollRulesService
from app.domain.services.report import build_payslip, build_roster
from app.domain.value_objects import EmployeeRules


# ---- relative dates --------------------------------------------------------
def test_resolve_month_relative():
    assert resolve_month(date(2026, 8, 17), "last month") == (2026, 7)
    assert resolve_month(date(2026, 1, 10), "last month") == (2025, 12)
    assert resolve_month(date(2026, 8, 17), "this month") == (2026, 8)
    assert resolve_month(date(2026, 8, 17), "2 months ago") == (2026, 6)
    assert resolve_month(date(2026, 8, 17), "the 2026-07 report") == (2026, 7)
    assert resolve_month(date(2026, 8, 17), "no date at all") == (2026, 8)


# ---- roster filters --------------------------------------------------------
def _mr(eid, paid, expected, present, absent, flagged, risk, ot=10.0):
    r = MonthReport(eid, "Name" + eid, "2026-07", "", [])
    r.present_days, r.absent_days = present, absent
    r.total_paid, r.total_expected = paid, expected
    r.flagged_days, r.money_at_risk = flagged, risk
    r.ot_hours, r.total_hours = ot, 180.0
    return r


def test_roster_filters_bucket_correctly():
    reps = [
        _mr("E1", 0, 160, 20, 0, 1, 50),      # worked but unpaid + flagged
        _mr("E2", 4000, 4000, 22, 0, 0, 0),   # clean paid
        _mr("E3", 100, 160, 5, 3, 2, 60),     # paid, absences, issues
    ]
    roster = build_roster("2026-07", reps)
    assert {r.employee_id for r in roster.unpaid()} == {"E1"}
    assert {r.employee_id for r in roster.paid()} == {"E2", "E3"}
    assert {r.employee_id for r in roster.with_absences()} == {"E3"}
    assert {r.employee_id for r in roster.with_issues()} == {"E1", "E3"}


def test_payslip_breakdown():
    r = _mr("E1", 4188, 4188, 22, 0, 0, 0, ot=40.0)
    stmt = build_payslip(r, ot_rate=30)
    assert stmt.ot_pay == 1200.0                 # 40h * $30
    assert stmt.gross_pay == 4188
    assert stmt.base_pay == round(4188 - 1200, 2)
    assert stmt.status == "OK" and "PAYSLIP" in stmt.text


# ---- configure -------------------------------------------------------------
class FakeConfig:
    def __init__(self):
        self.d = {}

    def get(self, k):
        return self.d.get(k)

    def set(self, k, v):
        self.d[k] = v

    def all(self):
        return dict(self.d)


def test_configure_sets_and_validates():
    c = FakeConfig()
    key, val, _ = Configure(c).execute("merge window", "90")
    assert key == "merge_seconds" and val == "90" and c.d["merge_seconds"] == "90"
    key, val, _ = Configure(c).execute("default rate", "25")
    assert key == "default_base_rate" and val == "25.0"
    with pytest.raises(ValueError):
        Configure(c).execute("unknown thing", "5")


# ---- bulk generate ---------------------------------------------------------
class FakeEmployees:
    def __init__(self):
        self.items = {}

    def add(self, e):
        self.items[e.id] = e

    def list_all(self):
        return list(self.items.values())

    def clear(self):
        self.items.clear()


class FakeAttendance:
    def __init__(self):
        self.days = []

    def add_many(self, days):
        self.days.extend(days)

    def clear(self):
        self.days.clear()


def test_generate_staff_is_additive_with_salary():
    emps, att = FakeEmployees(), FakeAttendance()
    emps.add(Employee("E100017", "Real Person", EmployeeRules.default()))
    res = GenerateStaff(emps, att, PayrollRulesService()).execute(3, 2026, 7)
    assert res["employees"] == 3
    assert "E100017" in emps.items                       # real data untouched
    assert all(i.startswith("E9") for i in res["ids"])   # distinct id range
    assert res["attendance_days"] > 0 and len(att.days) == res["attendance_days"]


# ---- new intent parses (regex fallback) ------------------------------------
def test_new_intents_parse():
    assert parse("last month unpaid list").kind == "list_unpaid"
    assert parse("show me the absent list for june").kind == "list_absent"
    assert parse("who has issues this month").kind == "list_issues"
    assert parse("check everyone last month").kind == "check_all"
    assert parse("make 10 employees").kind == "generate_employees"
    assert parse("generate salary for 5 employees last month").kind == "generate_salary"
    assert parse("payslip for E100017 last month").kind == "payslip"
    i = parse("set merge window to 90 seconds")
    assert i.kind == "configure"
    assert i.params == {"key": "merge_seconds", "value": "90"}
