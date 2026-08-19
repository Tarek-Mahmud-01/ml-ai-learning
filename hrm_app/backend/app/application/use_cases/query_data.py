"""
query_data — a SAFE, structured query over a month roster so the agent can answer
open-ended questions ("top 5 by overtime", "who worked > 25 days", "flagged and
unpaid") without a hand-coded intent. Operates on a RosterReport (built by
CheckAllEmployees); no raw SQL/code — only a whitelisted field set + operators.
"""
from __future__ import annotations

import json

from ...domain.services.report import RosterReport

FIELDS = {
    "paid": lambda r: r.total_paid,
    "expected": lambda r: r.total_expected,
    "present_days": lambda r: r.present_days,
    "absent_days": lambda r: r.absent_days,
    "late_days": lambda r: r.late_days,
    "flagged_days": lambda r: r.flagged_days,
    "money_at_risk": lambda r: r.money_at_risk,
    "ot_hours": lambda r: r.ot_hours,
    "total_hours": lambda r: r.total_hours,
}
_OPS = {
    ">": lambda a, b: a > b, ">=": lambda a, b: a >= b,
    "<": lambda a, b: a < b, "<=": lambda a, b: a <= b,
    "==": lambda a, b: a == b, "!=": lambda a, b: a != b,
}


class QueryData:
    def execute(self, roster: RosterReport, params: dict) -> str:
        rows = list(roster.rows)

        filters = params.get("filters") or []
        if isinstance(filters, str):                 # model sent JSON-as-string
            try:
                filters = json.loads(filters)
            except json.JSONDecodeError:
                filters = []
        if not isinstance(filters, list):
            filters = []

        for f in filters:
            if not isinstance(f, dict):              # skip malformed filter items
                continue
            field = str(f.get("field", "")).lower()
            op = str(f.get("op", "")).strip()
            val = f.get("value")
            if field == "status":                       # "OK" / "ISSUES"
                want = str(val).lower()
                same = [r for r in rows if str(r.status).lower() == want]
                rows = [r for r in rows if r not in same] if op == "!=" else same
                continue
            if field == "is_paid":                      # true/false / paid/unpaid
                want = str(val).lower() in ("true", "1", "yes", "paid")
                rows = [r for r in rows if r.is_paid == want]
                continue
            getter, cmp = FIELDS.get(field), _OPS.get(op)
            if getter is None or cmp is None:
                continue
            try:
                num = float(val)
            except (TypeError, ValueError):
                continue
            rows = [r for r in rows if cmp(getter(r), num)]

        sort_by = str(params.get("sort_by", "")).lower()
        if sort_by in FIELDS:
            desc = params.get("descending", True)
            if isinstance(desc, str):
                desc = desc.strip().lower() not in ("false", "0", "no", "asc")
            rows.sort(key=FIELDS[sort_by], reverse=bool(desc))

        try:
            limit = int(params.get("limit"))
        except (TypeError, ValueError):
            limit = 0
        if limit > 0:
            rows = rows[:limit]

        if not rows:
            return f"No employees match that query for {roster.month}."
        out = [f"{len(rows)} result(s) for {roster.month}:"]
        for r in rows[:60]:
            out.append(
                f"• {r.employee_id} {r.employee_name}: paid ${r.total_paid:,.0f}, "
                f"{r.present_days}d, OT {r.ot_hours:.0f}h, {r.flagged_days} flagged [{r.status}]")
        if len(rows) > 60:
            out.append(f"…and {len(rows) - 60} more")
        return "\n".join(out)
