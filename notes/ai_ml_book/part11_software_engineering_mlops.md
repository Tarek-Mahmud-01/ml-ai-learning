# PART XI — Software Engineering with AI/ML (MLOps)

[📖 Table of contents](README.md) · [← previous part](part10_agentic_ai.md) · [next part →](part12_design_interview_capstone.md) · [Appendices](appendix.md)

> **Days 100–111 · Category: building, shipping and running AI systems · Levels: 1 → 3 in every chapter**
> **You will be able to:** serve a model with FastAPI, secure the API, connect PostgreSQL / pgvector, containerize with Docker, run CI/CD, test ML and LLM code, run background jobs, track experiments, monitor drift, process big data with PySpark, and deploy to the cloud.
> **You already know SQL (5 years) and FastAPI** — these days focus on what is *different* for AI services: model loading, latency, validation, drift, cost, and testing fuzzy output.
> **Math you meet here (just-in-time):** p50 / p95 latency (Day 100) · token bucket (101) · PSI / KS drift (108) · Amdahl's law (109).
> **More depth:** Advanced shelf Days 167–170 (Kafka / Airflow, vLLM / Kubernetes, Python performance, privacy).

---

## Chapter 51 — Serving a model and securing the API

> ⚠️ **Common mistakes:** loading the model on every request · no input validation · no rate limit on an LLM endpoint (cost!) · secrets in code.

### Level 1–2: FastAPI model serving
<a id="day-100"></a>
#### ☐ Day 100 — Serve a model with FastAPI
- 🧮 **New math today (just-in-time):** latency percentiles (p50 / p95) and throughput.
- 🧠 **Idea · L1:** a model is useful only when other software can call it. Load the model **once at start-up**, validate every input, return clear errors.
- ➗ **Equation · L1:** latency `p50 / p95` · throughput `= requests/second` · `workers × (1/latency)` ≈ capacity
- ⌨️ **Build · L2:** `pydantic` request/response models; `lifespan` loads `joblib` / PyTorch model; `/health`, `/predict`, `/predict_batch`; async vs sync; OpenAPI docs; load test with `locust` or `hey`.
- 📊 **Measure · L2:** p50 / p95 latency, error rate, memory.
- 📈 **Improve · L3:** load model per request → once → batch endpoint → quantized / ONNX model (awareness: TorchServe, TF Serving).
- 🎤 **Interview · L3:** Why load the model at start-up? · How do you handle bad input? · Sync vs async for ML endpoints?
- ✅ **Done when:** p95 latency is measured and written in the README.


### Level 3: authentication, rate limits, secrets
<a id="day-101"></a>
#### ☐ Day 101 — API security: auth, rate limits, secrets
- 🧮 **New math today (just-in-time):** token-bucket rate limiting and JWT signatures.
- 🧠 **Idea · L1:** an AI endpoint costs money and can leak data. Protect it.
- ➗ **Equation · L1:** JWT = `header.payload.signature` · token bucket `tokens += rate·Δt (max burst)`
- ⌨️ **Build · L2:** password hashing, JWT login, API keys, role checks, rate limiting (Redis / `slowapi`), CORS, `.env` secrets, request-size limits.
- 📊 **Measure · L2:** attack tests: no token, expired token, 1 000 req/min, oversized body.
- 📈 **Improve · L3:** open → API key → JWT + roles + rate limit.
- 🎤 **Interview · L3:** JWT vs session? · How do you rate-limit? · Where do secrets live?
- ✅ **Done when:** all 4 attack tests are blocked.


## Chapter 52 — Data and storage for AI apps

### Levels 1 → 3 (inside the day)
<a id="day-102"></a>
#### ☐ Day 102 — Databases inside AI apps (PostgreSQL, pgvector)
- 🧠 **Idea · L1:** you know SQL — focus on **app integration**: ORM, async, migrations, vector columns, indexes.
- ➗ **Equation · L1:** HNSW index = approximate nearest neighbours (recall ↔ speed trade-off)
- ⌨️ **Build · L2:** SQLAlchemy async + Alembic; a `documents` table with a `vector` column (pgvector); store predictions + feedback; (optional MongoDB for logs).
- 📊 **Measure · L2:** query time with and without an index; N+1 query check.
- 📈 **Improve · L3:** sequential scan → HNSW index → connection pool tuned.
- 🎤 **Interview · L3:** pgvector vs a vector DB? · How do you store predictions for audit? · Migrations in production?
- ✅ **Done when:** RAG runs on pgvector with an index.


## Chapter 53 — Packaging and delivery: Docker, Git, CI/CD, testing

> ⚠️ **Common mistakes:** fat images · tests that need the real LLM · merging with a red pipeline.

### Level 1: Docker
<a id="day-103"></a>
#### ☐ Day 103 — Docker & docker-compose
- 🧠 **Idea · L1:** package code + dependencies so "it works on my machine" is the same everywhere.
- ➗ **Equation · L1:** image size `= Σ layers` — smaller is faster to deploy.
- ⌨️ **Build · L2:** `Dockerfile` (multi-stage, slim, non-root user, cached layers); `docker-compose` with api + postgres + redis; health-checks; `.dockerignore`.
- 📊 **Measure · L2:** image size, build time, start-up time.
- 📈 **Improve · L3:** fat image → slim base → multi-stage → layer caching.
- 🎤 **Interview · L3:** Image vs container? · Why multi-stage? · How do containers talk to each other?
- ✅ **Done when:** `docker compose up` starts the whole service.


### Level 2: Git workflow and CI
<a id="day-104"></a>
#### ☐ Day 104 — Git workflow & CI/CD
- 🧠 **Idea · L1:** every change goes through branch → pull request → review → automatic checks → merge.
- ➗ **Equation · L1:** none — pipeline = lint → test → build → (deploy).
- ⌨️ **Build · L2:** feature branch + PR; small commits (`feat:`, `fix:`); GitHub Actions: `ruff` + `pytest` + Docker build; a PR template; branch protection.
- 📊 **Measure · L2:** pipeline time; a failing test blocks the merge (prove it).
- 📈 **Improve · L3:** manual checks → CI → cached CI.
- 🎤 **Interview · L3:** Merge vs rebase? · What does CI do? · How do you review a PR?
- ✅ **Done when:** a red test blocks a PR in your own repo.


### Level 3: testing ML and LLM code
<a id="day-105"></a>
#### ☐ Day 105 — Testing ML & LLM code
- 🧠 **Idea · L1:** ML code is hard to test because outputs are fuzzy. Test the **parts**: data checks, pure functions, API contracts, and **score thresholds**.
- ➗ **Equation · L1:** model regression test `score ≥ baseline − tolerance`
- ⌨️ **Build · L2:** `pytest` fixtures; unit tests for preprocessing; data validation (`pandera`); API tests with `TestClient`; mock the LLM; golden-set test for prompts.
- 📊 **Measure · L2:** coverage; flaky-test count.
- 📈 **Improve · L3:** no tests → unit tests → data tests → model-score gate in CI.
- 🎤 **Interview · L3:** How do you test a model? · How do you test non-deterministic LLM output? · What is a golden set?
- ✅ **Done when:** CI fails if the model score drops.


## Chapter 54 — Async work, MLOps and monitoring

### Level 1–2: queues and caching
<a id="day-106"></a>
#### ☐ Day 106 — Async work: Redis, Celery, caching
- 🧠 **Idea · L1:** slow jobs (training, big LLM batches) must not block the API. Use a queue + workers. Cache repeated answers.
- ➗ **Equation · L1:** cache hit rate `= hits/requests` · retry with exponential back-off `delay = base·2ⁿ`
- ⌨️ **Build · L2:** Celery worker + Redis broker; job status endpoint; cache LLM / prediction results; idempotent retries.
- 📊 **Measure · L2:** latency before/after cache; queue depth.
- 📈 **Improve · L3:** inline → background job → + cache → + retries.
- 🎤 **Interview · L3:** When use a queue? · Idempotency? · Cache invalidation?
- ✅ **Done when:** a long job runs in the background and reports progress.


### Level 2: experiment tracking and reproducibility
<a id="day-107"></a>
#### ☐ Day 107 — MLflow, DVC & reproducibility
- 🧠 **Idea · L1:** you must reproduce any result: code + data + params + environment.
- ➗ **Equation · L1:** none — run = (git commit, data hash, params, metrics, artifacts).
- ⌨️ **Build · L2:** MLflow tracking + model registry; DVC for data; fixed seeds; pinned `requirements.txt`; a model card.
- 📊 **Measure · L2:** re-run an old experiment and get the same number.
- 📈 **Improve · L3:** notebook only → script + MLflow → + DVC + registry.
- 🎤 **Interview · L3:** What do you log for every run? · Model registry stages? · Data versioning?
- ✅ **Done when:** you reproduce a result from 2 weeks ago.


### Level 3: monitoring, drift and LLM tracing
<a id="day-108"></a>
#### ☐ Day 108 — Monitoring, drift & LLM tracing
- 🧮 **New math today (just-in-time):** Population Stability Index (PSI) and the KS test.
- 🧠 **Idea · L1:** a model decays when the world changes. Watch inputs, outputs, errors, cost.
- ➗ **Equation · L1:** PSI `= Σ (aᵢ − eᵢ)·ln(aᵢ/eᵢ)` (< 0.1 ok, > 0.25 big shift) · KS test for drift
- ⌨️ **Build · L2:** structured logging; Prometheus-style metrics (latency, errors); drift report with Evidently; alert rule; Langfuse traces for LLM calls.
- 📊 **Measure · L2:** simulate drift (shift a feature) and detect it.
- 📈 **Improve · L3:** no monitoring → logs → metrics → drift alert → retraining trigger.
- 🎤 **Interview · L3:** Data drift vs concept drift? · What do you monitor for an LLM app? · When retrain?
- ✅ **Done when:** a drift alert fires on your simulated shift.


## Chapter 55 — Big data and cloud

### Level 2: PySpark
<a id="day-109"></a>
#### ☐ Day 109 — PySpark, part 1
- 🧮 **New math today (just-in-time):** Amdahl's law.
- 🧠 **Idea · L1:** data too big for one machine. Spark splits it into **partitions** and runs on many cores. Lazy: nothing runs until an **action**.
- ➗ **Equation · L1:** speed-up ≈ `1/((1−p) + p/N)` (Amdahl's law)
- ⌨️ **Build · L2:** local Spark; DataFrame API; transformations vs actions; `groupBy`, `join`, window functions; read / write **Parquet**.
- 📊 **Measure · L2:** pandas vs Spark time on a 1–5 GB file.
- 📈 **Improve · L3:** CSV → Parquet → partition by a key → cache.
- 🎤 **Interview · L3:** Transformation vs action? · What is a shuffle? · When NOT to use Spark?
- ✅ **Done when:** you processed a file larger than your RAM.

<a id="day-110"></a>
#### ☐ Day 110 — PySpark, part 2
- 🧠 **Idea · L1:** ETL + features + models at scale. Know Spark MLlib and Dask as options.
- ➗ **Equation · L1:** none new.
- ⌨️ **Build · L2:** ETL pipeline: read → clean → features → write; a Spark MLlib `Pipeline` (or pandas-on-Spark); compare with your sklearn pipeline.
- 📊 **Measure · L2:** score + time vs sklearn on the same data.
- 📈 **Improve · L3:** skewed partitions → repartition / salting; fewer shuffles.
- 🎤 **Interview · L3:** What is data skew? · Batch vs streaming? · Spark vs Dask?
- ✅ **Done when:** one reproducible Spark job with a README.


### Level 3: cloud deployment (checkpoint)
<a id="day-111"></a>
#### ☐ Day 111 — Cloud deploy
- 🧠 **Idea · L1:** put the service on the internet. Options: Render / Railway / Hugging Face Spaces (easy), AWS (ECR + ECS / Lambda), plus awareness of Kubernetes (pod, deployment, service) and managed ML (SageMaker, Vertex AI, Azure ML).
- ➗ **Equation · L1:** monthly cost `≈ (instance price × hours) + (egress) + (LLM tokens)`
- ⌨️ **Build · L2:** deploy your **FastAPI + Docker** service publicly with secrets set in the platform; health-check; logs; rollback.
- 📊 **Measure · L2:** cold-start, p95, cost per day.
- 📈 **Improve · L3:** manual deploy → CI deploy on merge.
- 🎤 **Interview · L3:** answer **20 questions** (Days 100–111). Blue-green vs canary?
- ✅ **Checkpoint:** a **live URL** for your HR policy assistant.


---

### ✅ Part XI cheat card — where to deploy?
| Option | Effort | Cost | Good for | Limit |
|---|---|---|---|---|
| Hugging Face Spaces | lowest | free tier | demos, Gradio / Streamlit | not for private production |
| Render / Railway | low | low | FastAPI + Docker apps | scaling limits |
| AWS (ECS / Lambda / SageMaker), GCP Vertex AI, Azure ML | medium–high | pay per use | production, GPUs, compliance | complexity |
| Kubernetes | high | infra cost | many services, autoscaling | needs a platform team |
| Edge / on-device (ONNX) | medium | low | privacy, offline | small models only |

[📖 Table of contents](README.md) · [← previous part](part10_agentic_ai.md) · [next part →](part12_design_interview_capstone.md) · [Appendices](appendix.md)
