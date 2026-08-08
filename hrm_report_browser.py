r"""
=====================================================================
HRM PAYSLIP CHECKER  ->  BROWSER REPORT (no server, no port)
=====================================================================
What it does:
  1. Reads a payslip CSV (your dataset).
  2. Runs your HR rules on every row (the "method").
  3. Writes a real HTML report to reports/hrm_report.html
  4. You open that file in ANY browser (double-click it).

No FastAPI. No Gradio. No localhost. No port. Zero conflict with
your WAMP / ERP projects. It just writes a file.

Usage:
  venv\Scripts\python.exe hrm_report_browser.py data/payslips_sample.csv
  (if no path given, it uses data/payslips_sample.csv)
=====================================================================
"""
import sys
import os
import webbrowser
import pandas as pd

# --- GLOBAL SETTINGS (your HR "law") ---
SHIFT_TOTAL_HOURS = 9.0    # 8 work + 1 lunch
WORK_HOURS_GOAL = 8.0
LUNCH_BREAK_HOURS = 1.0
BASE_RATE_PER_HOUR = 20.0
OT_RATE_PER_HOUR = 30.0
TOLERANCE = 0.01           # pay difference allowed before we call it "wrong"


def check_one_payslip(check_in, check_out, reported_pay):
    """Apply the HR rules to a single payslip. Returns a dict of results."""
    in_time = pd.to_datetime(check_in)
    out_time = pd.to_datetime(check_out)
    total_presence = (out_time - in_time).total_seconds() / 3600

    overtime_hours = max(0, total_presence - SHIFT_TOTAL_HOURS)
    actual_work_hours = min(WORK_HOURS_GOAL, max(0, total_presence - LUNCH_BREAK_HOURS))

    expected_pay = actual_work_hours * BASE_RATE_PER_HOUR + overtime_hours * OT_RATE_PER_HOUR
    difference = reported_pay - expected_pay
    is_wrong = abs(difference) > TOLERANCE

    return {
        "total_hours": round(total_presence, 2),
        "ot_hours": round(overtime_hours, 2),
        "expected_pay": round(expected_pay, 2),
        "difference": round(difference, 2),
        "status": "WRONG" if is_wrong else "CORRECT",
    }


def run(csv_path):
    # --- 1. Load the dataset ---
    if not os.path.exists(csv_path):
        print(f"[ERROR] File not found: {csv_path}")
        sys.exit(1)

    df = pd.read_csv(csv_path)
    required = {"Check_In", "Check_Out", "Reported_Pay"}
    missing = required - set(df.columns)
    if missing:
        print(f"[ERROR] CSV is missing columns: {missing}")
        print(f"        Found columns: {list(df.columns)}")
        sys.exit(1)

    print(f"Loaded {len(df)} payslips from {csv_path}")

    # --- 2. Run the method on every row ---
    rows = []
    wrong_count = 0
    total_overpaid = 0.0
    total_underpaid = 0.0

    for _, r in df.iterrows():
        res = check_one_payslip(r["Check_In"], r["Check_Out"], r["Reported_Pay"])
        if res["status"] == "WRONG":
            wrong_count += 1
            if res["difference"] > 0:
                total_overpaid += res["difference"]
            else:
                total_underpaid += abs(res["difference"])
        rows.append({
            "id": r.get("Employee_ID", "-"),
            "name": r.get("Name", "-"),
            "date": r.get("Date", "-"),
            "in": r["Check_In"],
            "out": r["Check_Out"],
            "paid": float(r["Reported_Pay"]),
            **res,
        })

    correct_count = len(rows) - wrong_count

    # --- 3. Print a quick console summary too ---
    print(f"  CORRECT: {correct_count}   WRONG: {wrong_count}")

    # --- 4. Build the HTML report ---
    html = build_html(rows, correct_count, wrong_count, total_overpaid, total_underpaid, csv_path)

    out_dir = "reports"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.abspath(os.path.join(out_dir, "hrm_report.html"))
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\nReport written to: {out_path}")

    # --- 5. Open it in the real browser (file://, no server) ---
    webbrowser.open("file:///" + out_path.replace("\\", "/"))
    print("Opened in your default browser.")


def build_html(rows, correct, wrong, overpaid, underpaid, source):
    trs = ""
    for r in rows:
        wrong = r["status"] == "WRONG"
        badge = ("<span class='b bad'>WRONG</span>" if wrong
                 else "<span class='b ok'>CORRECT</span>")
        diff = r["difference"]
        diff_txt = f"+{diff:.2f}" if diff > 0 else f"{diff:.2f}"
        diff_cls = "pos" if diff > 0 else ("neg" if diff < 0 else "zero")
        trs += f"""<tr class="{'row-bad' if wrong else ''}">
          <td class="mono">{r['id']}</td>
          <td>{r['name']}</td>
          <td class="mono dim">{r['in']}–{r['out']}</td>
          <td class="mono num">{r['total_hours']}</td>
          <td class="mono num">{r['ot_hours']}</td>
          <td class="mono num">${r['paid']:.2f}</td>
          <td class="mono num">${r['expected_pay']:.2f}</td>
          <td class="mono num {diff_cls}">{diff_txt}</td>
          <td>{badge}</td>
        </tr>"""

    total = correct + wrong
    accuracy = (correct / total * 100) if total else 0

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>HRM Payslip Check — Report</title>
<style>
  :root {{
    --bg:#f5f6fb; --card:#fff; --ink:#181a2b; --soft:#5a5d78; --faint:#8b8ea8;
    --line:#e5e7f2; --accent:#4f46e5; --ok:#0f9d6b; --ok-bg:#e4f6ef;
    --bad:#d6336c; --bad-bg:#fdeaf1; --mono:ui-monospace,"Cascadia Code",Consolas,monospace;
    --sans:-apple-system,"Segoe UI",Roboto,sans-serif;
  }}
  @media (prefers-color-scheme:dark){{
    :root{{--bg:#0e0f1a;--card:#16182a;--ink:#eceefb;--soft:#aab;--faint:#777c9e;
    --line:#282b45;--accent:#8b85f5;--ok:#34d399;--ok-bg:#10261f;--bad:#f472a6;--bad-bg:#2a1220;}}
  }}
  *{{box-sizing:border-box;}}
  body{{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.5;}}
  .wrap{{max-width:1000px;margin:0 auto;padding:2.5rem 1.25rem 4rem;}}
  .eyebrow{{font-family:var(--mono);font-size:.78rem;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);margin:0 0 .4rem;}}
  h1{{font-size:1.9rem;margin:0 0 .4rem;letter-spacing:-.02em;}}
  .src{{color:var(--faint);font-family:var(--mono);font-size:.82rem;margin-bottom:1.75rem;}}
  .cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1rem;margin-bottom:2rem;}}
  .kpi{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:1.1rem 1.25rem;}}
  .kpi .lbl{{font-family:var(--mono);font-size:.75rem;color:var(--faint);text-transform:uppercase;letter-spacing:.05em;}}
  .kpi .val{{font-size:2rem;font-weight:700;margin-top:.25rem;font-variant-numeric:tabular-nums;}}
  .kpi.good .val{{color:var(--ok);}} .kpi.bad .val{{color:var(--bad);}}
  .kpi .unit{{font-size:.9rem;color:var(--faint);font-weight:500;}}
  table{{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;}}
  .tablewrap{{overflow-x:auto;}}
  th{{text-align:left;font-family:var(--mono);font-size:.72rem;text-transform:uppercase;letter-spacing:.05em;color:var(--faint);padding:.85rem .9rem;border-bottom:1px solid var(--line);white-space:nowrap;}}
  td{{padding:.8rem .9rem;border-bottom:1px solid var(--line);font-size:.92rem;}}
  tr:last-child td{{border-bottom:none;}}
  .row-bad{{background:var(--bad-bg);}}
  .mono{{font-family:var(--mono);}} .num{{text-align:right;font-variant-numeric:tabular-nums;}}
  .dim{{color:var(--soft);}} .pos{{color:var(--bad);}} .neg{{color:var(--accent);}} .zero{{color:var(--faint);}}
  .b{{font-family:var(--mono);font-size:.72rem;font-weight:700;padding:.25rem .55rem;border-radius:6px;white-space:nowrap;}}
  .b.ok{{color:var(--ok);background:var(--ok-bg);}} .b.bad{{color:var(--bad);background:var(--bad-bg);}}
  footer{{margin-top:2rem;color:var(--faint);font-family:var(--mono);font-size:.78rem;}}
  .rules{{margin-top:1.5rem;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:1rem 1.25rem;font-size:.85rem;color:var(--soft);}}
  .rules code{{font-family:var(--mono);color:var(--accent);}}
</style></head><body>
<div class="wrap">
  <p class="eyebrow">HRM Anomaly Check · Live Report</p>
  <h1>Payslip verification results</h1>
  <p class="src">source: {source} &nbsp;·&nbsp; {total} payslips analyzed</p>

  <div class="cards">
    <div class="kpi"><div class="lbl">Total checked</div><div class="val">{total}</div></div>
    <div class="kpi good"><div class="lbl">Correct</div><div class="val">{correct}</div></div>
    <div class="kpi bad"><div class="lbl">Errors found</div><div class="val">{wrong}</div></div>
    <div class="kpi"><div class="lbl">Accuracy</div><div class="val">{accuracy:.0f}<span class="unit">%</span></div></div>
    <div class="kpi bad"><div class="lbl">Overpaid</div><div class="val">${overpaid:.0f}</div></div>
    <div class="kpi"><div class="lbl">Underpaid</div><div class="val">${underpaid:.0f}</div></div>
  </div>

  <div class="tablewrap"><table>
    <thead><tr>
      <th>ID</th><th>Name</th><th>Shift</th><th>Hours</th><th>OT</th>
      <th>Paid</th><th>Expected</th><th>Diff</th><th>Status</th>
    </tr></thead>
    <tbody>{trs}</tbody>
  </table></div>

  <div class="rules">
    <strong>Rules applied:</strong>
    9h shift (8 work + 1 lunch) · base <code>${BASE_RATE_PER_HOUR:.0f}/h</code> ·
    overtime after 9h at <code>${OT_RATE_PER_HOUR:.0f}/h</code> ·
    a payslip is <code>WRONG</code> if reported pay differs from expected by more than ${TOLERANCE}.
  </div>

  <footer>Generated locally by hrm_report_browser.py · no server, opened via file://</footer>
</div></body></html>"""


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "data/payslips_sample.csv"
    run(path)
