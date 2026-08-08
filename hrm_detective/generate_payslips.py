r"""
=====================================================================
HRM DETECTIVE — Milestone 1: Generate realistic payslip data
=====================================================================
Makes 200 payslips. MOST are correct. A FEW are secretly wrong
(fraud or mistakes) so we can test if our detective catches them.

Rules used to make "correct" pay:
  - 9h shift = 8 work + 1 lunch
  - base pay = $20/hour (max 8 hours)
  - overtime = $30/hour after 9 hours of presence

Run with:
  python hrm_detective/generate_payslips.py
=====================================================================
"""
import sys, os
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import numpy as np
import pandas as pd

rng = np.random.default_rng(7)

BASE_RATE = 20.0
OT_RATE = 30.0
SHIFT = 9.0
LUNCH = 1.0
WORK_GOAL = 8.0

names = ["Ayesha", "Rahim", "Karim", "Fatima", "Hasan", "Nadia",
         "Imran", "Sadia", "Tariq", "Mona", "Bilal", "Zara"]


def correct_pay(check_in_h, check_out_h):
    presence = check_out_h - check_in_h
    ot = max(0, presence - SHIFT)
    work = min(WORK_GOAL, max(0, presence - LUNCH))
    return round(work * BASE_RATE + ot * OT_RATE, 2), round(presence, 2)


rows = []
n = 200
for i in range(n):
    emp_id = f"E{100 + (i % 12):03d}"
    name = names[i % 12]
    check_in = 9  # 09:00
    # most people work a normal 8-11 hour presence (whole hours only)
    presence = int(rng.choice([9, 9, 9, 10, 11, 8], p=[.4, .2, .1, .1, .1, .1]))
    check_out = check_in + presence
    pay, hours = correct_pay(check_in, check_out)

    label = "normal"
    # --- Secretly inject a few WRONG payslips (about 8%) ---
    r = rng.random()
    if r < 0.04:                       # underpaid fraud
        pay = round(pay * rng.uniform(0.4, 0.7), 2)
        label = "underpaid"
    elif r < 0.07:                     # overpaid fraud
        pay = round(pay * rng.uniform(1.4, 2.0), 2)
        label = "overpaid"
    elif r < 0.08:                     # impossible hours
        check_out = check_in + 20      # "worked" 20 hours!
        pay, hours = correct_pay(check_in, check_out)
        label = "impossible_hours"

    rows.append({
        "Employee_ID": emp_id,
        "Name": name,
        "Date": f"2024-06-{(i % 28) + 1:02d}",
        "Check_In": f"{check_in:02d}:00",
        "Check_Out": f"{int(check_out):02d}:00",
        "Reported_Pay": pay,
        "_secret_label": label,        # only for checking later; detective ignores it
    })

df = pd.DataFrame(rows)
out = os.path.join("hrm_detective", "payslips.csv")
df.to_csv(out, index=False)

n_bad = (df["_secret_label"] != "normal").sum()
print(f"Created {len(df)} payslips -> {out}")
print(f"Secretly hid {n_bad} bad payslips inside:")
print(df["_secret_label"].value_counts().to_string())
print("\nNow run:  python hrm_detective/detective.py")
