r"""
=====================================================================
HRM DETECTIVE — Milestone 2: The Rules Brain + Browser Report
=====================================================================
Reads payslips.csv, applies HR rules to catch WRONG payslips,
and writes a browser report (report.html) that opens automatically.
No server, no port -> safe next to WAMP/ERP.

Run with (from the MAIN folder):
  python hrm_detective/detective.py

Milestone 3 (YOUR practice): add the ML brain (Isolation Forest).
Look for the "TODO (Milestone 3)" spot below.
=====================================================================
"""
import sys, os, webbrowser
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import pandas as pd

# --- HR rules (the "law") ---
BASE_RATE, OT_RATE = 20.0, 30.0
SHIFT, LUNCH, WORK_GOAL = 9.0, 1.0, 8.0
TOLERANCE = 0.01

HERE = os.path.dirname(__file__)
CSV = os.path.join(HERE, "payslips.csv")
REPORT = os.path.join(HERE, "report.html")


def hour_of(t):
    """Read 'HH:MM' as a number of hours. Handles 29:00 (past midnight)."""
    h, m = str(t).split(":")
    return int(h) + int(m) / 60.0


def rules_check(check_in, check_out, reported_pay):
    """Return expected pay + whether the payslip breaks the rules."""
    presence = hour_of(check_out) - hour_of(check_in)
    ot = max(0, presence - SHIFT)
    work = min(WORK_GOAL, max(0, presence - LUNCH))
    expected = round(work * BASE_RATE + ot * OT_RATE, 2)
    diff = round(reported_pay - expected, 2)
    return presence, round(ot, 2), expected, diff, abs(diff) > TOLERANCE


def main():
    if not os.path.exists(CSV):
        print("payslips.csv not found. Run generate_payslips.py first.")
        return

    df = pd.read_csv(CSV)
    rows, wrong, money_at_risk = [], 0, 0.0

    for _, r in df.iterrows():
        presence, ot, expected, diff, is_wrong = rules_check(
            r["Check_In"], r["Check_Out"], r["Reported_Pay"])
        if is_wrong:
            wrong += 1
            money_at_risk += abs(diff)
        rows.append({
            "id": r["Employee_ID"], "name": r["Name"], "date": r["Date"],
            "in": r["Check_In"], "out": r["Check_Out"],
            "paid": r["Reported_Pay"], "hours": round(presence, 1),
            "ot": ot, "expected": expected, "diff": diff,
            "rule_flag": is_wrong,
        })

    # =============================================================
    # TODO (Milestone 3) — ADD THE ML BRAIN HERE
    # -------------------------------------------------------------
    # from sklearn.ensemble import IsolationForest
    # feats = pd.DataFrame({
    #     "hours":    [x["hours"] for x in rows],
    #     "paid":     [x["paid"]  for x in rows],
    #     "expected": [x["expected"] for x in rows],
    # })
    # iso = IsolationForest(contamination=0.08, random_state=42)
    # preds = iso.fit_predict(feats)          # -1 = anomaly, 1 = normal
    # for x, p in zip(rows, preds):
    #     x["ml_flag"] = (p == -1)
    # Then show x["ml_flag"] as a column in the report + compare to rules.
    # =============================================================
    for x in rows:
        x.setdefault("ml_flag", False)   # placeholder until you add ML

    correct = len(rows) - wrong
    html = build_html(rows, correct, wrong, money_at_risk)
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Checked {len(rows)} payslips.")
    print(f"  CORRECT: {correct}   WRONG (rules): {wrong}")
    print(f"  Money at risk: ${money_at_risk:,.2f}")
    path = os.path.abspath(REPORT)
    print(f"Report: {path}")
    webbrowser.open("file:///" + path.replace("\\", "/"))


def build_html(rows, correct, wrong, money):
    rows_sorted = sorted(rows, key=lambda x: -abs(x["diff"]))  # worst first
    trs = ""
    for r in rows_sorted:
        if not r["rule_flag"] and not r["ml_flag"]:
            continue  # report shows only flagged ones (keep it short)
        d = r["diff"]
        reason = ("Underpaid" if d < 0 else "Overpaid") if r["rule_flag"] else "ML anomaly"
        trs += f"""<tr>
          <td class=mono>{r['id']}</td><td>{r['name']}</td>
          <td class="mono dim">{r['in']}-{r['out']} ({r['hours']}h)</td>
          <td class="mono num">${r['paid']:.2f}</td>
          <td class="mono num">${r['expected']:.2f}</td>
          <td class="mono num {'neg' if d<0 else 'pos'}">{d:+.2f}</td>
          <td><span class="b bad">{reason}</span></td>
        </tr>"""
    if not trs:
        trs = "<tr><td colspan=7 style='text-align:center;padding:2rem'>No problems found 🎉</td></tr>"

    return f"""<!doctype html><html><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>HRM Detective Report</title><style>
:root{{--bg:#f5f6fb;--card:#fff;--ink:#181a2b;--soft:#5a5d78;--faint:#8b8ea8;
--line:#e5e7f2;--accent:#4f46e5;--ok:#0f9d6b;--bad:#d6336c;--bad-bg:#fdeaf1;
--mono:ui-monospace,Consolas,monospace;--sans:-apple-system,"Segoe UI",sans-serif;}}
@media(prefers-color-scheme:dark){{:root{{--bg:#0e0f1a;--card:#16182a;--ink:#eceefb;
--soft:#aab;--faint:#777c9e;--line:#282b45;--accent:#8b85f5;--ok:#34d399;--bad:#f472a6;--bad-bg:#2a1220;}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans)}}
.wrap{{max-width:920px;margin:0 auto;padding:2.5rem 1.25rem 4rem}}
.eyebrow{{font-family:var(--mono);font-size:.78rem;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);margin:0 0 .4rem}}
h1{{font-size:1.9rem;margin:0 0 1.5rem;letter-spacing:-.02em}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1rem;margin-bottom:2rem}}
.kpi{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:1.1rem 1.25rem}}
.kpi .lbl{{font-family:var(--mono);font-size:.72rem;color:var(--faint);text-transform:uppercase}}
.kpi .val{{font-size:1.9rem;font-weight:700;margin-top:.25rem;font-variant-numeric:tabular-nums}}
.kpi.bad .val{{color:var(--bad)}}.kpi.good .val{{color:var(--ok)}}
table{{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden}}
.tw{{overflow-x:auto}}th{{text-align:left;font-family:var(--mono);font-size:.7rem;text-transform:uppercase;color:var(--faint);padding:.8rem .9rem;border-bottom:1px solid var(--line);white-space:nowrap}}
td{{padding:.8rem .9rem;border-bottom:1px solid var(--line);font-size:.9rem}}tr:last-child td{{border:none}}
.mono{{font-family:var(--mono)}}.num{{text-align:right;font-variant-numeric:tabular-nums}}
.dim{{color:var(--soft)}}.neg{{color:var(--bad)}}.pos{{color:var(--accent)}}
.b{{font-family:var(--mono);font-size:.7rem;font-weight:700;padding:.25rem .55rem;border-radius:6px}}
.b.bad{{color:var(--bad);background:var(--bad-bg)}}
.note{{margin-top:1.5rem;color:var(--soft);font-size:.85rem}}
</style></head><body><div class=wrap>
<p class=eyebrow>HRM Detective · Payslip Audit</p>
<h1>Payslip investigation results</h1>
<div class=cards>
<div class=kpi><div class=lbl>Total checked</div><div class=val>{correct+wrong}</div></div>
<div class="kpi good"><div class=lbl>Correct</div><div class=val>{correct}</div></div>
<div class="kpi bad"><div class=lbl>Flagged wrong</div><div class=val>{wrong}</div></div>
<div class="kpi bad"><div class=lbl>Money at risk</div><div class=val>${money:,.0f}</div></div>
</div>
<div class=tw><table><thead><tr>
<th>ID</th><th>Name</th><th>Shift</th><th>Paid</th><th>Expected</th><th>Diff</th><th>Reason</th>
</tr></thead><tbody>{trs}</tbody></table></div>
<p class=note>Only flagged payslips are shown. Rules: 9h shift (8 work + 1 lunch),
$20/h base, $30/h overtime after 9h. <b>Milestone 3:</b> add Isolation Forest to also
catch unusual patterns the rules miss.</p>
</div></body></html>"""


if __name__ == "__main__":
    main()
