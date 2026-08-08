"""
Use-case test for ImportBioTime with in-memory fakes (no DB). Proves: bursts
merge, days get first-in/last-out + inferred type, pay = expected_pay at the
default rate, single punches become missing-punch, and replace clears the demo.
"""
from datetime import date, datetime

from app.application.use_cases.import_bio_time import ImportBioTime
from app.domain.entities import AttendanceDay, Employee
from app.domain.services.payroll_rules import PayrollRulesService
from app.domain.value_objects import DayType, EmployeeRules, parse_hour
from app.infrastructure.io.biotime_reader import Punch

svc = PayrollRulesService()


class FakeEmployees:
    def __init__(self):
        self.items: dict[str, Employee] = {}

    def add(self, e):
        self.items[e.id] = e

    def clear(self):
        self.items.clear()


class FakeAttendance:
    def __init__(self):
        self.days: list[AttendanceDay] = []

    def add_many(self, days):
        self.days.extend(days)

    def upsert_day(self, day):
        self.days.append(day)

    def clear(self):
        self.days.clear()


class FakeReader:
    def __init__(self, punches):
        self._p = punches

    def read_punches(self, path):
        return list(self._p)


def test_import_reduces_prices_and_replaces_demo():
    punches = [
        # 100017: morning double-tap (burst) + an evening punch -> one worked day
        Punch("100017", "MD JASHIM UDDIN", datetime(2026, 7, 27, 8, 44, 18)),
        Punch("100017", "MD JASHIM UDDIN", datetime(2026, 7, 27, 8, 44, 20)),
        Punch("100017", "MD JASHIM UDDIN", datetime(2026, 7, 27, 19, 1, 15)),
        # 12: a device-test burst, all within 60 s -> a single punch (missing out)
        Punch("12", "MDMILON", datetime(2024, 8, 22, 6, 57, 58)),
        Punch("12", "MDMILON", datetime(2024, 8, 22, 6, 58, 0)),
    ]
    emps, att = FakeEmployees(), FakeAttendance()
    emps.add(Employee("E100", "DemoPerson", EmployeeRules.default()))   # demo to clear
    att.add_many([AttendanceDay("E100", date(2024, 6, 1), DayType.PRESENT,
                                "09:00", "17:00", 140)])

    uc = ImportBioTime(emps, att, svc, FakeReader(punches),
                       merge_seconds=60, default_base_rate=20, default_ot_rate=30)
    report = uc.execute("dummy.sql", replace=True)

    assert report["employees"] == 2
    assert report["punches_read"] == 5
    assert report["punches_kept"] == 3           # 2 kept for 100017 + 1 for 12
    assert report["punches_merged_away"] == 2
    assert report["missing_punch_days"] == 1

    # Demo replaced by the two real staff (ids carry the E prefix).
    assert set(emps.items) == {"E100017", "E12"}

    default_rules = EmployeeRules(base_rate=20, ot_rate=30)
    worked = [d for d in att.days if d.check_out is not None]
    assert len(worked) == 1
    d = worked[0]
    presence = parse_hour(d.check_out) - parse_hour(d.check_in)
    assert d.reported_pay == svc.expected_pay(presence, default_rules)
    assert d.day_type == DayType.OVERTIME        # ~10.3h > 9h shift

    miss = [d for d in att.days if d.check_out is None]
    assert len(miss) == 1
    assert miss[0].day_type == DayType.MISSING_PUNCH
    assert miss[0].reported_pay == 0.0
