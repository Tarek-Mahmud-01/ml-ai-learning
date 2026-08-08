# 🕵️ HRM Payslip Detective — Real Project

A tool that reads payslip data and catches **wrong or fraudulent payslips**
using two brains working together:
1. **Rules brain** — your HR law (9h shift, overtime, base/OT rates).
2. **ML brain** — an Isolation Forest that spots weird/unusual payslips
   the rules might miss.

Then it shows a **browser report** flagging each bad payslip, the reason,
and how much money was lost — with **no server, no port** (safe with WAMP/ERP).

---

## 🎯 What "done" looks like
Run one command → get a browser report that says:
> "3 payslips look WRONG. Karim was underpaid $60. Employee X is a
>  statistical anomaly (unusual pattern). Total money at risk: $250."

---

## ✅ TO-DO CHECKLIST (build in order)

### 🟢 Milestone 1 — Data (DONE for you)
- [x] `generate_payslips.py` — makes 200 realistic payslips
- [x] Hide a few "fraud" payslips inside (wrong pay, impossible hours)
- [x] Save to `hrm_detective/payslips.csv`

### 🟢 Milestone 2 — Rules Brain (DONE for you)
- [x] `detective.py` — apply HR rules to every payslip
- [x] Calculate expected pay, find differences
- [x] Label each payslip CORRECT or WRONG (by rules)

### 🟡 Milestone 3 — ML Brain (YOUR practice)
- [ ] Add Isolation Forest to `detective.py`
- [ ] Train it on the numeric features (hours, pay, OT)
- [ ] Let it flag "anomaly" payslips (unusual patterns)
- [ ] Compare: did ML catch what the rules missed?

### 🟡 Milestone 4 — Browser Report (partly done)
- [x] Basic HTML report with KPIs + table
- [ ] Add a column showing the ML anomaly flag
- [ ] Add a "reason" for each flagged payslip
- [ ] Add a total "money at risk" number

### 🔵 Milestone 5 — Polish (stretch goals)
- [ ] Sort worst offenders to the top
- [ ] Add a simple bar chart of money lost per employee
- [ ] Let the user pass any CSV file as input
- [ ] Write a short README explaining how to use it

---

## 🗂️ Files in this project
| File | Job |
|---|---|
| `generate_payslips.py` | Make realistic test data (with hidden fraud) |
| `detective.py` | The brains: rules + ML, writes the report |
| `payslips.csv` | The data (created by the generator) |
| `report.html` | The final browser report (created by detective) |

## ▶️ How to run (from the MAIN folder, not inside hrm_detective)
```
cd H:\ml&ai_learning
python hrm_detective/generate_payslips.py
python hrm_detective/detective.py
```
