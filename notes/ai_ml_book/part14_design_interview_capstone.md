# PART XIV — System Design, Interview and Capstone

[📖 Table of contents](README.md) · [← previous part](part13_software_engineering_mlops.md) · [next part →](part15_advanced_shelf.md) · [Appendices](appendix.md)


> **Days 126–134 · Category: putting everything together · Levels: 1 → 3**
> **You will be able to:** design an ML / LLM system on a whiteboard, write a design doc, build and deploy a capstone (the **Intelligent HRM Assistant**: anomaly model + RAG + agent + API + UI), pass a full mock interview, and prove nothing is missing with the gap audit.

---

## Chapter 62 — ML and LLM system design

> **The framework:** requirements & metric → data → features → model → training → serving (batch / online) → monitoring → iteration.
> ⚠️ **Common mistakes:** jumping to the model · no metric · no failure modes · no monitoring plan.

### Level 1–2: classic ML systems
<a id="day-126"></a>
#### ☐ Day 126 — ML system design, part 1
- 🧮 **New math today (just-in-time):** back-of-envelope estimates (QPS, storage, cost).
- 🧠 **Idea · L1:** a repeatable framework: **requirements & metric → data → features → model → training → serving (batch / online) → monitoring → iteration**.
- ➗ **Equation · L1:** back-of-envelope: `QPS = users × requests/day / 86 400` · storage `= rows × bytes` · cost.
- ⌨️ **Build · L2:** design on paper: spam filter, fraud detection, recommender. Draw the boxes and data flow.
- 📊 **Measure · L2:** self-score each design with a checklist (metric? baseline? failure modes? monitoring?).
- 📈 **Improve · L3:** V1 sketch → V2 with numbers → V3 with trade-offs.
- 🎤 **Interview · L3:** "Design a fraud detection system." (record yourself, 30 min)
- ✅ **Done when:** you can walk through the framework without notes.


### Level 3: LLM systems and the design doc
<a id="day-127"></a>
#### ☐ Day 127 — ML / LLM system design, part 2 + the design doc
- 🧠 **Idea · L1:** LLM systems: RAG at scale, agent platform, search ranking. Trade-offs: quality ↔ latency ↔ cost ↔ safety.
- ➗ **Equation · L1:** cost per request `= tokens_in·p_in + tokens_out·p_out + retrieval cost` · caching / batching savings.
- ⌨️ **Build · L2:** a 2-page **design doc** (context, goals, non-goals, design, alternatives, risks, metrics, rollout).
- 📊 **Measure · L2:** have a peer (or an LLM) review the doc against a checklist.
- 📈 **Improve · L3:** V1 → reviewed V2.
- 🎤 **Interview · L3:** "Design an enterprise HR assistant used by 5 000 employees."
- ✅ **Done when:** you have a design-doc template you reuse.


## Chapter 63 — Capstone: Intelligent HRM Assistant

> **Product:** upload payslips → anomaly model flags rows → RAG explains the broken policy with citations → agent answers questions with tools → API + UI → deployed with Docker, CI, monitoring.

### Level 1: design
<a id="day-128"></a>
#### ☐ Day 128 — Capstone design: **Intelligent HRM Assistant**
- 🧠 **Idea · L1:** one product: upload payslips → **anomaly model** flags rows → **RAG** explains which policy was broken (with citations) → **agent** answers questions with tools → **API + UI** → deployed.
- ➗ **Equation · L1:** define success metrics now: anomaly precision@k, RAG citation accuracy, agent task success, p95 latency, cost / query.
- ⌨️ **Build · L2:** architecture diagram, data flow, API contract (OpenAPI), eval plan, risk list (privacy, wrong flags, injection), milestones.
- 📊 **Measure · L2:** review against the Day-127 doc checklist.
- 📈 **Improve · L3:** cut scope to what fits in 3 build days.
- 🎤 **Interview · L3:** present the design in 5 minutes.
- ✅ **Done when:** the design doc is committed.


### Level 2: build
<a id="day-129"></a>
#### ☐ Day 129 — Capstone build 1: model + RAG
- 🧠 **Idea · L1:** the intelligence layer.
- ➗ **Equation · L1:** use your Day-128 metrics.
- ⌨️ **Build · L2:** wrap the anomaly model (Day 39, `hrm_detective/`) as a service; reuse the Day-93 RAG for policy explanations.
- 📊 **Measure · L2:** anomaly precision@k; citation accuracy.
- 📈 **Improve · L3:** V1 → V3 on the worst error slice.
- 🎤 **Interview · L3:** explain one trade-off you made.
- ✅ **Done when:** both services pass their tests.

<a id="day-130"></a>
#### ☐ Day 130 — Capstone build 2: agent + API + UI
- 🧠 **Idea · L1:** the product layer.
- ➗ **Equation · L1:** use your Day-128 metrics.
- ⌨️ **Build · L2:** the Day-110 agent behind a FastAPI app (`hrm_app/`), JWT auth, rate limiting, a simple front-end (upload data, see flags, chat).
- 📊 **Measure · L2:** agent task success; p95 latency.
- 📈 **Improve · L3:** V1 → V3.
- 🎤 **Interview · L3:** how do you keep the agent safe?
- ✅ **Done when:** an end-to-end demo works locally.


### Level 3: ship and polish
<a id="day-131"></a>
#### ☐ Day 131 — Capstone build 3: ship it
- 🧠 **Idea · L1:** production readiness.
- ➗ **Equation · L1:** use your Day-128 metrics + cost per query.
- ⌨️ **Build · L2:** Docker + compose, CI (lint + tests + eval gate), monitoring + drift alert, deploy to a public URL.
- 📊 **Measure · L2:** smoke test on the live URL; cost per day.
- 📈 **Improve · L3:** fix what the smoke test finds.
- 🎤 **Interview · L3:** how would you roll this out in a company?
- ✅ **Done when:** the live URL works.

<a id="day-132"></a>
#### ☐ Day 132 — Polish & document
- 🧠 **Idea · L1:** a project is only as good as its README.
- ➗ **Equation · L1:** none.
- ⌨️ **Build · L2:** README (problem, architecture diagram, how to run, results table V1 → V4, limits), model card, 3-minute demo video, screenshots.
- 📊 **Measure · L2:** ask someone to run it from the README alone.
- 📈 **Improve · L3:** fix every place they got stuck.
- 🎤 **Interview · L3:** give the 2-minute project pitch (record it).
- ✅ **Done when:** a stranger can run your project.


## Chapter 64 — Interview and portfolio

### Level 3: mock interview
<a id="day-133"></a>
#### ☐ Day 133 — Full mock interview
- 🧠 **Idea · L1:** rehearse the real thing.
- ➗ **Equation · L1:** derive on a whiteboard (no notes): linear regression normal equation · logistic gradient · softmax + CE gradient · backprop for 2 layers · attention · Adam · PCA · Bayes.
- ⌨️ **Build · L2:** code from memory: K-means, logistic regression with GD, a simple decision split, cosine search.
- 📊 **Measure · L2:** 50 ML-theory questions (random from your 20-question sets) + 1 system design; self-score and list weak spots.
- 📈 **Improve · L3:** re-study the 5 weakest topics for 90 minutes each, then re-test.
- 🎤 **Interview · L3:** a full 60-minute mock (record it).
- ✅ **Done when:** ≥ 80 % on the theory set.


### Level 3: portfolio and gap audit
<a id="day-134"></a>
#### ☐ Day 134 — Portfolio & **gap audit**
- 🧠 **Idea · L1:** make your work visible and check nothing is missing.
- ➗ **Equation · L1:** none.
- ⌨️ **Build · L2:** pin 4–6 GitHub repos; CV + LinkedIn headline; fill the **gap-audit table** in [Appendix D](appendix.md) (tick every row); write a 30-day follow-up list (Kaggle, open source, papers, one deeper area).
- 📊 **Measure · L2:** every roadmap topic has a ✅ or a written reason.
- 📈 **Improve · L3:** schedule the 30-day list.
- 🎤 **Interview · L3:** tell the story: "what I built, what failed, what I improved, what I learned".
- ✅ **Done when:** gap-audit is fully ticked. **You finished.** 🎓


---

### ✅ Part XIV cheat card — design checklist
| Question | Have I answered it? |
|---|---|
| What is the business goal and the one metric (offline + online)? | ☐ |
| What is the baseline? | ☐ |
| Where does the data come from, and how fresh? | ☐ |
| What are the features and how are they computed at serve time (no skew)? | ☐ |
| Which model, and why not something simpler? | ☐ |
| Batch or online? Latency budget per stage? | ☐ |
| Cost per request / per day? | ☐ |
| How will it fail? Fallback? Human in the loop? | ☐ |
| How do I monitor drift, quality, cost? | ☐ |
| How do I roll out (shadow → canary → A/B) and roll back? | ☐ |

[📖 Table of contents](README.md) · [← previous part](part13_software_engineering_mlops.md) · [next part →](part15_advanced_shelf.md) · [Appendices](appendix.md)
