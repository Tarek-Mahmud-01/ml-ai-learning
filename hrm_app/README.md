# 🕵️ HRM Detective — Full-Stack (Next.js + FastAPI)

An attendance & payroll auditor. Pick an employee, check their whole month, and
see which days are wrong — using **two brains**:
- **Rules brain** — your pay policy (per-employee rates, shift, overtime, weekend).
- **AI brain** — a scikit-learn anomaly model that catches unusual days the
  rules miss (e.g. an impossible 20-hour shift paid "correctly").

Built with **Domain-Driven Design + clean architecture**. Black & white UI.
100% free & local — no paid API.

---

## Architecture (clean layers)
```
backend/app/
  domain/          PURE business logic (rules, entities) — no framework/DB/ML imports
  application/     use cases (seed, train, list, check month) — orchestration only
  infrastructure/  adapters: PostgreSQL (SQLAlchemy) + ML (scikit-learn) + config
  presentation/    thin FastAPI routers + schemas + DI (no business logic)

frontend/
  app/             Next.js pages (dashboard, employee report) — black & white
  lib/api.ts       the ONLY file that talks to the backend
  components/       presentation-only building blocks
```
Dependencies point **inward**: presentation → application → domain. The domain
depends on nothing (verified: no `fastapi`/`sqlalchemy`/`sklearn` imports in it).

---

## Prerequisites (already set up on this machine)
- **Node.js** 18+ and **npm** (has v22 / v10).
- **PostgreSQL** running on `localhost:5432` with a database named `hrm`
  (user `postgres`, password `postgres`). Change via `backend/.env`.
- Python **venv** at `H:\ml&ai_learning\venv` with `psycopg`, FastAPI, uvicorn,
  scikit-learn installed.

> ⚠️ **The `&` in the folder name** (`ml&ai_learning`) breaks Windows `cmd`
> shims. Two fixes are already baked in:
> - Frontend `package.json` calls Next via `node ./node_modules/...` (relative),
>   so `npm run dev` works.
> - Always start the backend with the **venv activated** (commands below), not
>   by passing the full `&` path.

---

## Run it (two terminals)

### 1) Backend — FastAPI on port 8010
```powershell
cd H:\ml&ai_learning\hrm_app\backend
& "H:\ml&ai_learning\venv\Scripts\Activate.ps1"
python -m uvicorn app.presentation.main:app --port 8010 --reload
```
API docs: http://localhost:8010/docs

### 2) Frontend — Next.js on port 3000
```powershell
cd H:\ml&ai_learning\hrm_app\frontend
npm run dev
```
Open: **http://localhost:3000**

*(Or just run `hrm_app\start-backend.ps1` and `hrm_app\start-frontend.ps1`.)*

---

## How to use
1. Open http://localhost:3000
2. Click **Generate data** (seeds 12 employees + a full month of attendance with
   edge cases + hidden fraud).
3. Click **Train detector** (fits the anomaly model on the worked days).
4. Click **View report →** on any employee to see their monthly audit:
   KPIs, day-by-day table, flagged days with the reason **and which rule applied**.

Status badges: `OK` · `RULE-FLAG` (rules say wrong) · `ML-FLAG` (AI says unusual)
· `BOTH`.

---

## API (core)
| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | liveness |
| POST | `/admin/seed` | generate employees + monthly attendance |
| POST | `/admin/train` | (re)train the anomaly detector |
| GET | `/employees` | list employees |
| GET | `/employees/{id}` | one employee + effective rules |
| GET | `/employees/{id}/report?month=YYYY-MM` | monthly rules+ML audit |

---

## Tests
```powershell
cd H:\ml&ai_learning\hrm_app\backend
python -m pytest tests/ -q
```
- `test_domain_rules.py` — pure rules (per-employee rules, edge cases, 29:00).
- `test_api_e2e.py` — seed → train → report through the API (needs Postgres).

---

## Config (`backend/.env`)
```
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/hrm
ARTIFACT_PATH=var/hrm_model.joblib
CORS_ORIGINS=http://localhost:3000
API_PORT=8010
```

## Phase 2 — Admin Assistant Chat ✅ (built)
A **Chat page** (`/chat`) runs the whole system in plain language — safe by design
(keyword **intent whitelist**, no raw code/SQL), validated writes, **confirm-on-delete**,
and an **audit log**. Free & local (no LLM).

What you can type:
- **Employees:** `add employee Rakib rate 22 start 09:00` · `set E101 base rate to 30` · `delete employee E101` (→ repeat with `confirm`)
- **Attendance:** `add attendance E101 2024-06-15 present 09:00 18:00 pay 160` · `set E101 2024-06-12 checkout to 18:00`
- **Payroll (pay on a day):** `set E101 2024-06-12 pay to 190` · `insert payroll E101 2024-06-12 190`
- **Check:** `check E101 june` · `show E101 2024-06-12`
- **Train / teach:** `train` (unsupervised) · `E100 2024-06-11 is wrong` → `retrain from my labels` (supervised)
- **Learn:** `how does training work?` · `supervised vs unsupervised`

**Two model kinds, one artifact:** `train` fits an IsolationForest (`kind=iforest`,
unsupervised); `retrain from my labels` fits a RandomForest (`kind=rf`, supervised
— learns from your labels). Whichever you trained last is the active detector; the
chat tells you which.

New endpoint: `POST /chat {message}` → `{reply, kind?, changed?}`. New tables:
`labels`, `audit_log`. Still no auth/RBAC (a later phase).

### Natural-language chat via a LOCAL LLM (free) 🧠
The chat understands free-form English via a **local Ollama model** (`llama3.2:3b`)
— no paid API, runs offline. The LLM only **chooses a safe action** from the
whitelist (it never runs code/SQL); if Ollama is down it **falls back to the regex
parser**, so the chat always works.

Now you can type naturally, e.g.:
- *"check employee 100 for the last two months and tell me if anything looks bad"* → multi-month report
- *"make Karim's pay rate 30"* · *"add a day for E101 on june 20, present, 9 to 6, paid 160"*

Setup (one time): install Ollama, then `ollama pull llama3.2:3b`. Config in
`backend/.env` / settings: `USE_LLM=true`, `OLLAMA_URL`, `OLLAMA_MODEL`. Set
`USE_LLM=false` to use the fast keyword parser only. New multi-month endpoint
intent: `check_range` ("last N months").

## Phase 3 — Real biometric data + Punch-Merge rule ✅ (built)
Import a **real ZKTeco BioTime** SQL dump (raw fingerprint punches) and train on it.

**The Punch-Merge rule (new):** real devices store every read as its own row, so one
tap becomes a burst of punches seconds apart. `domain/services/punch_merge.py`
collapses any punches within a window (**default 60s**) into one, then reduces each
employee-day to **first-in / last-out** and infers the day type. A single punch all
day → `missing_punch`. Verified to reproduce the dump's own daily table exactly.

**No pay in the source:** the dump has punches only, so pay is set to an
**assume-correct baseline** (`reported_pay = expected_pay(presence)` at a default
rate). Tune per employee in chat (`set E100017 base rate to 25`); once real pay is
entered the rules brain flags over/under-payment. IDs become `E`+code (e.g.
`E100017`).

How to use:
- **Dashboard →** "Use your real data" → **Import real data**, then **Train detector**.
- **Chat →** "import real data" · "train" · "check E100017 last two months".
- **API →** `POST /admin/import {path?, replace?, merge_seconds?}`.

Config in `backend/.env` / settings: `PUNCH_MERGE_SECONDS` (60),
`IMPORT_DEFAULT_BASE_RATE` (20), `IMPORT_DEFAULT_OT_RATE` (30), `IMPORT_SQL_PATH`.
`parse_hour` now also accepts `HH:MM:SS`. Known v1 limit: night shifts that cross
midnight may split across two calendar dates.

> ⚠️ Running the demo-seeding tests re-seeds the DB and **wipes imported real data** —
> just re-import from the dashboard/chat to restore it.

### Still not built (future)
Login/roles (RBAC) + sensitive-field masking. Night-shift midnight pairing.

## Note
`next@14.2.15` prints a security-upgrade notice. For this local learning app it's
fine; run `npm install next@latest` when you want the patched release.
