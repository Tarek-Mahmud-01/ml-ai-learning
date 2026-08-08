# 🕵️ HRM Detective — Full A-to-Z Architecture (Plan Only)

> This is the **plan / design** for the complete system. **No code yet.**
> When you say "implement", we build it step by step in this order.

---

## 🎯 The goal (admin scenario)
An admin picks ONE employee, the system checks that employee's **whole month**
of attendance (with real edge cases), and reports the problems.

```
Admin: check E101 for June
System: "E101 worked 20 days, absent 2, late 3.
         Paid $3040 vs expected $3160.
         1 underpaid day flagged. Money at risk: $120."
        + opens a browser report
```

100% **free & local** (scikit-learn) — no paid API, no server, no port.

---

## 🧩 The A-to-Z Pipeline (7 stages)

```
[A] Config (rules)          hrm_config.py     GLOBAL "law" + PER-EMPLOYEE rules
        │
[B] Monthly data generator  generate_month.py 30 days × N employees + edge cases + hidden fraud
        │
[C] Feature engineering      features.py       turn each day into numbers
        │
[D] Train the AI brain       train_model.py    model LEARNS "wrong vs correct" → hrm_model.joblib
        │
[E] Detective (checker)      detective.py      rules brain + ML brain vote per day
        │
[F] Monthly report builder   report.py         per-employee KPIs + day table + text summary
        │
[G] Admin query entry        admin.py          "check E101 june" → runs D/E/F for that employee
        │
[H] Chat + data-update layer chat.py           client asks queries / fixes wrong data (SECURE)
```

Each stage = **one file, one job** (easy to learn, easy to test).

---

## ⚠️ IMPORTANT: Per-employee rules (each employee is different)

**Careful:** not every employee has the same rules! One person may earn $20/h,
another $25/h. One starts at 09:00, another at 10:00. Some have Fri/Sat weekend,
others Sat/Sun. If we check an employee with the WRONG rules, we flag good
payslips as bad (false alarm) — a serious mistake.

**Solution: two layers of rules.**

```
GLOBAL default rules  (hrm_config.py)      ← used when an employee has no custom rule
        +
PER-EMPLOYEE rules    (employees.csv)      ← overrides the default for that person
        =
effective rules for THIS employee  →  used by the checker
```

### New file: `employees.csv` (the contract table)
One row per employee = their personal contract:
| Employee_ID | Name | Base_Rate | OT_Rate | Shift_Start | Work_Hours | Weekend_Days | Contract |
|---|---|---|---|---|---|---|---|
| E101 | Ayesha | 20 | 30 | 09:00 | 8 | Sat,Sun | full-time |
| E102 | Rahim | 25 | 35 | 10:00 | 8 | Fri,Sat | full-time |
| E103 | Karim | 15 | 20 | 09:00 | 4 | Sat,Sun | part-time |

### How it is used (careful matching)
1. `hrm_config.py` holds the **global default** rule (fallback).
2. `get_rules(employee_id)` = look up that employee's row in `employees.csv`.
   - Found → use THEIR rates/shift/weekend.
   - Not found → use the global default (and WARN in the report).
3. `[B] generate_month.py` builds each employee's "correct" pay using THEIR OWN
   rules, so the test data is realistic per person.
4. `[E] detective.py` checks each day with THAT employee's effective rules —
   never the global one by accident.
5. `[F] report.py` shows which rule set was applied (e.g. "Rules: E102 contract,
   $25/h, 10:00 start, Fri/Sat weekend") so the admin can trust the result.

> This is the "careful" part: **the checker must always use the employee's own
> contract rules.** A mismatch = false fraud alerts. The report always prints
> which rules it used, so mistakes are visible.

---

## 📄 Stage-by-stage

### [A] `hrm_config.py` — the rules in one place
All HR law in one file so rules never disagree between files.
- **Global default rules:** base rate $20/h, OT $30/h, 9h shift (8 work + 1
  lunch), tolerance $0.01, weekend Sat/Sun, holiday list, late after 09:15,
  half-day = 4h, leave = paid, absent = unpaid.
- **Per-employee override:** a `get_rules(employee_id)` function that reads
  `employees.csv` and returns THAT employee's rules (rate, shift start, work
  hours, weekend days), falling back to the global default if not listed.
- ⚠️ Everything downstream (generator, detective, report) must call
  `get_rules(employee_id)` — never hard-code the global rule.

### [A2] `employees.csv` — per-employee contract table
One row per employee with their personal rules (see the "Per-employee rules"
section above). This is what makes each individual employee checked correctly.

### [B] `generate_month.py` — realistic monthly attendance
Creates `attendance.csv` — one row **per employee per day** for a month.
Edge cases baked in: `present, late, half_day, absent, leave, weekend,
holiday, missing_punch, overtime`.
Hidden fraud to catch: underpaid, overpaid, paid-on-weekend, impossible-hours,
pay-on-absent-day.

### [C] `features.py` — shared feature engineering
One function used by BOTH training and the checker (so they always match).
Per-day numbers: presence_hours, reported_pay, pay_per_hour, expected_pay,
pay_diff, is_weekend, is_zero_hours, day_type.

### [D] `train_model.py` — the AI brain
RandomForest learns "wrong vs correct" from examples (not hard-coded rules).
Saves `hrm_model.joblib`. Shows accuracy + which features matter most.

### [E] `detective.py` — rules brain + ML brain
For each day: a **rule verdict** (math check) AND a **model verdict** (pattern
check). Combined status: `OK / RULE-FLAG / ML-FLAG / BOTH`.
The AI catches what rules miss (e.g. impossible 20-hour day).

### [F] `report.py` — monthly report
Two outputs:
1. **Browser report** — KPIs (days present/absent/late/leave, hours, OT, paid vs
   expected, money at risk) + day-by-day table, worst days first.
2. **Plain-English summary** (template, no LLM) — printed + shown on the report.

### [G] `admin.py` — the admin entry point
Two ways to ask (both free, no API):
- `python hrm_detective/admin.py E101 2024-06`
- `python hrm_detective/admin.py "check E101 june"` (keyword parsing)
Also `all` = report for every employee.

### [H] `chat.py` — client chat + data update (SECURE)
The client "talks" to the system: asks questions AND fixes wrong data, then
re-checks. Everything is safe — **no arbitrary code/SQL runs.**

**Two things the client can do:**

**1) Ask a query (read):**
```
> how many days was E101 absent in june?
> who was overpaid last month?
> total money at risk for E102
> show late days for E103
```
The chat maps the sentence to a **safe, pre-approved query type** (intent), never
to raw code. See the security model below.

**2) Update / fix wrong data (write):**
```
> fix E101 2024-06-12 checkout to 18:00
> mark E104 2024-06-09 as leave
> set E101 2024-06-12 pay to 160
```
→ the change is validated, written to `attendance.csv`, logged in `audit_log.csv`,
and the day is **re-checked automatically** so the report updates.

---

## 🔐 Security model (careful — payroll is sensitive)

Payroll data is private and money is involved, so the chat is built **safe by
design**:

| Risk | How we stop it |
|---|---|
| Arbitrary code / SQL injection | Chat maps to a **whitelist of intents** only. Raw input is NEVER run as code. No `eval`, no SQL string building. |
| Bad data writes | Every update is **validated** (valid employee, valid date, sane values) before saving. Invalid → rejected with a clear message. |
| Silent tampering | Every write goes to `audit_log.csv` (who, what, when, old → new). Nothing changes invisibly. |
| Sensitive info leak | Fields are tagged **public / sensitive**. Sensitive fields (exact pay, rate) are **masked** unless the user is an authorized role. |
| Wrong person editing | Simple **role/PIN gate**: `admin` can write; `viewer` can only read. (Free, local — a config list, not a paid auth service.) |
| Accidental data loss | Writes make a **timestamped backup** of `attendance.csv` first. |

**Secure vs insecure info on chat:**
- ✅ Safe to show: attendance counts, flags, "money at risk" totals, which rule was used.
- 🔒 Masked by default: an individual's exact salary/rate, personal notes — shown
  only to the `admin` role, hidden (e.g. `$***`) for `viewer`.
- ❌ Never allowed: running commands, reading files outside the project, deleting data.

**Intent whitelist (the only actions the chat can do):**
```
READ  : count_days, list_flags, money_at_risk, show_employee, compare_month
WRITE : fix_time, fix_pay, set_day_type   (admin role only, validated + logged)
```
Anything not matching an intent → polite "I can't do that" (fails safe).

---

## 🗂️ Files to build (in `hrm_detective/`)
| File | New/Change | Job |
|---|---|---|
| `hrm_config.py` | new | global rules + `get_rules(employee_id)` lookup |
| `employees.csv` | new | per-employee contract rules (rate, shift, weekend) |
| `generate_month.py` | new | monthly attendance + edge cases + fraud (uses each employee's rules) |
| `features.py` | new | shared feature engineering |
| `train_model.py` | change | train on monthly data |
| `detective.py` | change | rules + ML per day |
| `report.py` | new | per-employee report + summary |
| `admin.py` | new | admin query entry |
| `chat.py` | new | secure client chat: ask queries + fix data |
| `audit_log.csv` | new (auto) | record of every data change (who/what/when) |
| `roles.py` | new | simple role/PIN gate (admin can write, viewer read-only) |
| `GUIDE_A_to_Z.md` | new | step-by-step learning doc |

Old `generate_payslips.py` stays as the simple day-level intro version.

---

## 🔢 Build order (each step runnable on its own)
1. `hrm_config.py` + `employees.csv` (global rules + per-employee contracts)
2. `generate_month.py` → make `attendance.csv` (each employee uses own rules)
3. `features.py`
4. `train_model.py` → train + save model
5. `detective.py` → rules + ML per day
6. `report.py` → browser + text for one employee
7. `admin.py` → wire it all together
8. `chat.py` + `roles.py` → secure chat: ask queries + fix data (+ `audit_log.csv`)
9. Docs

---

## ✅ How we'll verify it works
- After [B]: print row count + edge-case counts + hidden-fraud counts.
- After [D]: accuracy + feature importance on unseen days.
- After [E]: known-fraud employee → confirm flags fire (ML catches impossible hours).
- After [G]: `admin.py E101 2024-06` → summary matches the browser report KPIs;
  keyword form works; `all` runs without crashing (absent/leave/weekend handled).

---

## 🔒 Constraints honored
- Free & local (scikit-learn), **no paid API**, no server/port.
- Beginner-friendly: one file = one job, heavy comments.
- Windows-safe paths + UTF-8 output guard.
- **Secure by design:** whitelist intents only, validated writes, audit log,
  role gate, sensitive-field masking, backup before write.
- Optional later upgrade: swap template summary/chat for a FREE local LLM
  (Ollama) — still no paid API. Even then, the LLM only picks an **intent**;
  it never runs raw code, so the security model stays intact.

---

## 🤖 Is this "real AI"?
Yes — two AI pieces, both free & local:
1. **The detective model** (`train_model.py`) — a trained classifier that LEARNS
   wrong-vs-correct payslips from examples (not hard-coded rules).
2. **The chat** — turns plain language into a **safe intent**. Starts as keyword
   parsing (free, safe); can later use a free local LLM for better understanding,
   while still only choosing from the safe intent whitelist.

The rules brain + the trained AI brain + the secure chat = a real AI-based HRM
payroll checker that finds problems AND lets the client fix them safely.

---

> **Status: PLAN ONLY.** Say **"implement"** (or "start building") and we begin
> at step 1 (`hrm_config.py`), one runnable file at a time.
