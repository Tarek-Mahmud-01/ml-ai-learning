"""
PayrollRulesService — the RULES BRAIN. Pure domain logic.

This is where the old `rules_check` lives now, generalised to per-employee
rules and real attendance edge cases (absent / leave / weekend / missing punch).
No framework, DB, or ML imports — just the payroll "law".
"""
from __future__ import annotations

from dataclasses import dataclass

from ..entities import AttendanceDay
from ..value_objects import DayType, EmployeeRules, parse_hour


@dataclass
class RuleOutcome:
    """The rules-only result for one day (before ML is considered)."""
    presence_hours: float
    ot_hours: float
    expected_pay: float
    diff: float                # reported - expected (negative = underpaid)
    rule_flag: bool
    reason: str
    rule_note: str             # which policy was applied (for the UI, no info gap)


class PayrollRulesService:
    """Applies one employee's rules to one day and decides if pay is correct."""

    def expected_pay(self, presence: float, rules: EmployeeRules) -> float:
        """Expected pay for a worked day from presence hours."""
        ot = max(0.0, presence - rules.shift_hours)
        work = min(rules.work_goal, max(0.0, presence - rules.lunch))
        return round(work * rules.base_rate + ot * rules.ot_rate, 2)

    def check_day(self, day: AttendanceDay, rules: EmployeeRules) -> RuleOutcome:
        dt = day.day_type
        paid = float(day.reported_pay or 0.0)
        tol = rules.tolerance

        # --- No-work days -------------------------------------------------
        if dt == DayType.ABSENT:
            diff = round(paid - 0.0, 2)
            flag = abs(diff) > tol            # any pay on an unpaid day is wrong
            reason = ("Paid on an absent (unpaid) day"
                      if flag else "Absent — no pay (correct)")
            return RuleOutcome(0.0, 0.0, 0.0, diff, flag, reason, "Absent: unpaid day")

        if dt == DayType.LEAVE:
            expected = round(rules.work_goal * rules.base_rate, 2)  # paid leave = base day
            diff = round(paid - expected, 2)
            flag = abs(diff) > tol
            reason = (f"Leave pay mismatch (expected ${expected:.2f})"
                      if flag else "Approved paid leave (correct)")
            note = f"Leave: paid {rules.work_goal:.0f}h @ ${rules.base_rate:.0f}"
            return RuleOutcome(0.0, 0.0, expected, diff, flag, reason, note)

        if dt in (DayType.WEEKEND, DayType.HOLIDAY):
            diff = round(paid - 0.0, 2)
            flag = paid > tol                 # no work expected → no pay expected
            reason = ("Pay on a no-work day (weekend/holiday)"
                      if flag else f"{dt.value.capitalize()} — no pay (correct)")
            note = f"{dt.value.capitalize()}: no work expected"
            return RuleOutcome(0.0, 0.0, 0.0, diff, flag, reason, note)

        # --- Punch-based days ---------------------------------------------
        ci = parse_hour(day.check_in)
        co = parse_hour(day.check_out)
        if dt == DayType.MISSING_PUNCH or ci is None or co is None:
            return RuleOutcome(
                0.0, 0.0, 0.0, 0.0, True,
                "Missing check-in/out — cannot verify, needs review",
                "Missing punch: manual review")

        presence = co - ci
        ot = max(0.0, presence - rules.shift_hours)
        expected = self.expected_pay(presence, rules)
        diff = round(paid - expected, 2)
        flag = abs(diff) > tol
        if flag:
            reason = f"{'Underpaid' if diff < 0 else 'Overpaid'} by ${abs(diff):.2f}"
        else:
            reason = "Pay matches hours (correct)"
        work = min(rules.work_goal, max(0.0, presence - rules.lunch))
        note = (f"{work:.1f}h @ ${rules.base_rate:.0f}"
                f" + {ot:.1f}h OT @ ${rules.ot_rate:.0f}")
        return RuleOutcome(round(presence, 2), round(ot, 2), expected, diff,
                           flag, reason, note)
