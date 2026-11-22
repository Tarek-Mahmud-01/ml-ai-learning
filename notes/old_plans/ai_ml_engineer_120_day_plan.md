# 🗓️ AI & ML Engineer — 120-Day Plan (Low Level → High Level)

> **Goal:** become an advanced **AI/ML Engineer** who can also build **Generative AI, Agentic AI, NLP** and ship them as **real software**.
> **Pace:** 3–4 hrs/day · 120 days (~17 weeks) · **Style:** low level first, then high level. No gaps.
> **Old plans** are archived in [old_plans/](old_plans/). **Your class notes** are in [course_notes/](course_notes/).
> **Tools list** (what to install when): [tools_and_libraries.md](tools_and_libraries.md)
> **Source roadmaps** (AI Engineer, GenAI Engineer, AI Agent Developer, NLP Engineer, ML Engineer, Software Engineering with ML-AI):
> <https://github.com/rashakil-ds/Roadmap-Docs>

---

## 🧭 How every day works (same 6 blocks, ≈ 3.5 hrs)

| # | Block | Time | What you do |
|---|---|---|---|
| 1 | 🧠 **Idea + ➗ Equation** | 45 min | Explain it in simple words. Write the equation. Name every symbol. Derive it by hand on paper. |
| 2 | ⌨️ **Build it twice** | 90 min | First **from scratch** (NumPy / pure Python). Then with the **library** (scikit-learn / PyTorch / …). Both must give the same answer. |
| 3 | 📊 **Performance & error** | 30 min | Pick the right metric. Look at the **biggest errors**. Ask: *where* is it wrong and *why*? |
| 4 | 📈 **Improve ladder** | 30 min | V1 baseline → V2 fix → V3 tune → V4 best. Write every score in the results table. |
| 5 | 🎤 **Interview** | 15 min | Answer 3 questions **out loud, in your own words**. Add: "when should I NOT use it?" |
| 6 | ✅ **Done when…** | 5 min | Check the box. One git commit: `Day N: topic`. |

**Algorithm card** — for every algorithm, your note must answer these 10 lines:
`Idea · Equation · Assumptions · From-scratch code · Library code · Metric · Typical errors · How to improve (ladder) · Use / don't use · 3 interview Qs`

**Rules**
1. **Never skip block 3–5.** Knowing the equation is not enough; you must also know *how it fails* and *how to fix it*.
2. **Fit scalers/encoders/imputers on the train set only** — always. (Data leakage is the #1 interview trap.)
3. **Every number goes in the results table** (template at the bottom). "V1 → V4" is your proof of improvement.
4. **Last day of every phase = checkpoint:** mini-project + **20 interview questions** + wrap the model in a small **FastAPI function with a test** (this is the company habit).
5. Stuck > 30 min? Write down exactly what is unclear, move on, come back next day.
6. Keep code in `plan120/dayNNN_topic.py` and results in `plan120/results_log.md` (create the folder on Day 1).

**Datasets (all offline, built into scikit-learn):** `load_diabetes` (regression) · `load_breast_cancer` (binary) · `load_wine`, `load_digits` (multi-class) · `make_moons/blobs` (clusters) ·
**your own data:** `data/` sales data and the HRM payslip data in `hrm_detective/` and `hrm_app/`.

---

## 🗺️ Phase map

| Phase | Days | Topic | You finish with |
|---|---|---|---|
| 1 | 1–9 | Foundations: stats, linear algebra, calculus, probability, information theory | You can read any ML equation |
| 2 | 10–16 | Data & features: EDA, cleaning, encoding, scaling, selection, imbalance, pipelines | A clean, leak-free pipeline |
| 3 | 17–47 | Classical ML: regression → classification → trees → boosting → clustering → tuning → time series | Every classic algorithm, with equation + errors |
| 4 | 48–59 | Deep learning: neuron → backprop → PyTorch → TensorFlow/Keras | A network you can debug |
| 5 | 60–62 | Computer vision (short) | CNN + transfer learning + detection idea |
| 6 | 63–73 | NLP: text → embeddings → RNN/LSTM → Transformer → BERT | A fine-tuned NLP model |
| 7 | 74–76 | Reinforcement learning (short) | Q-learning, PPO idea, RLHF link |
| 8 | 77–90 | Generative AI & LLMs: tiny GPT, prompts, RAG, LoRA, diffusion | RAG assistant + LoRA model |
| 9 | 91–99 | Agentic AI: tools, ReAct, LangGraph, MCP, multi-agent, evals | A safe, evaluated agent |
| 10 | 100–111 | Software engineering with AI/ML: FastAPI, auth, Docker, CI, tests, MLOps, PySpark, cloud | A deployed, monitored service |
| 11 | 112–120 | System design, interviews, capstone (**Intelligent HRM Assistant**), gap audit | Portfolio + interview-ready |

**Your class notes → days:** Correlation (D3) · Distance Metrics (D4, D28) · Loss Functions / Partial Derivatives / Gradient Descent (D6–7, D50) ·
Feature Engineering, Transformation & Encoding (D12–13) · Pandas + Simple Linear Regression + Residuals + Cost (D17–18) ·
Linear Regression, Evaluation, Over/Underfitting, Bias–Variance (D20–22) · Decision Tree (D32–33) · Random Forest, Linear Model (D34).
**Already done earlier (re-use, don't redo):** old Day 1 (linear algebra practice), old Day 2 → [advanced_day2_calculus.md](advanced_day2_calculus.md) and [../advanced_day2_calculus.py](../advanced_day2_calculus.py).

---
---

# 🧮 PHASE 1 — Foundations (Days 1–9)

### ☐ Day 1 — Setup + the ML workflow (baseline, split, metric, error)
- 🧠 **Idea:** ML = learn a rule from examples. Workflow: question → data → **split** → **baseline** → model → **metric** → **error analysis** → improve. A *baseline* (always predict the mean) is the score every model must beat.
- ➗ **Equation:** `error eᵢ = yᵢ − ŷᵢ` · baseline `ŷ = ȳ` · `RMSE = √( (1/n) Σ eᵢ² )`
- ⌨️ **Build:** check `venv` + `requirements.txt`; create `plan120/`. Load `load_diabetes`; split 70/15/15 by hand; baseline mean predictor; RMSE by hand → check with `DummyRegressor`.
- 📊 **Measure:** baseline RMSE on validation. List the 10 biggest errors. Write: "this is the score to beat".
- 📈 **Improve:** V1 = mean baseline (log it). Preview V2 = a one-feature line (done properly on Day 17).
- 🎤 **Interview:** Train vs validation vs test? · Why a baseline? · What is data leakage (one example)?
- ✅ **Done when:** environment runs, baseline RMSE is in `results_log.md`.

### ☐ Day 2 — Statistics for ML
- 🧠 **Idea:** describe data by **centre**, **spread**, **shape**. Sample vs population. Central Limit Theorem. A p-value = "how surprising is this if nothing is going on?".
- ➗ **Equation:** `x̄ = Σx/n` · `s² = Σ(x−x̄)²/(n−1)` · `z = (x−x̄)/s` · standard error `= s/√n` · IQR `= Q3 − Q1`
- ⌨️ **Build:** mean / median / variance / std / IQR from scratch → compare with NumPy/pandas. Histogram + boxplot. z-score outlier finder. A t-test with `scipy.stats`.
- 📊 **Measure:** your values = NumPy values (diff < 1e-9). Why `n−1`? Show the bias with `n` on tiny samples (error analysis).
- 📈 **Improve:** mean → median → trimmed mean on data with outliers; see which centre stays stable.
- 🎤 **Interview:** Mean vs median — when? · Why divide by n−1? · What does a p-value mean (and NOT mean)?
- ✅ **Done when:** you can explain CLT with a simulation plot.

### ☐ Day 3 — Correlation & covariance (Pearson r) — *your notes: Correlation*
- 🧠 **Idea:** do two variables move together? Covariance has a sign; correlation rescales it to −1…1. Only **linear** relationships. Correlation ≠ causation.
- ➗ **Equation:** `cov(X,Y) = Σ(x−x̄)(y−ȳ)/(n−1)` · `r = cov(X,Y)/(sₓ·s_y)` = `[nΣxy − ΣxΣy] / √([nΣx² − (Σx)²][nΣy² − (Σy)²])`
- ⌨️ **Build:** r with **both** formulas → check `np.corrcoef`. Correlation heat-map on diabetes. Counter-example: `y = x²` gives r ≈ 0.
- 📊 **Measure:** Pearson vs Spearman (Pearson on ranks). Error analysis: one outlier can change r a lot (Anscombe's quartet).
- 📈 **Improve:** Pearson → Spearman for curved-but-monotone data → remove outlier. Use r to rank features.
- 🎤 **Interview:** What does r = 0 mean? · Pearson vs Spearman? · Give a correlation-not-causation example.
- ✅ **Done when:** both formulas give the same r to 1e-12.

### ☐ Day 4 — Vectors, matrices & distance metrics — *your notes: Distance Metrics*
- 🧠 **Idea:** one row = a **vector**; a dataset = a **matrix**. Dot product = similarity. Distance = how far two rows are.
- ➗ **Equation:** `a·b = Σaᵢbᵢ` · `‖a‖ = √Σaᵢ²` · Euclidean `√Σ(aᵢ−bᵢ)²` · Manhattan `Σ|aᵢ−bᵢ|` · Minkowski `(Σ|aᵢ−bᵢ|ᵖ)^(1/p)` · cosine `a·b/(‖a‖‖b‖)` · matrix product `Cᵢⱼ = Σₖ Aᵢₖ Bₖⱼ`
- ⌨️ **Build:** matrix multiply with 3 loops vs `@`. All distances from scratch vs `scipy.spatial.distance`. "Find the nearest row to a query row".
- 📊 **Measure:** timing loop vs NumPy; shape-mismatch errors and how to read them.
- 📈 **Improve:** raw features → **scaled** features → cosine; show the nearest neighbour changes.
- 🎤 **Interview:** Euclidean vs Manhattan vs cosine? · Why scale before distance? · What is the curse of dimensionality?
- ✅ **Done when:** you can say which distance to use for text, for maps, for money.

### ☐ Day 5 — Eigenvectors & SVD (the maths behind PCA)
- 🧠 **Idea:** a matrix stretches space. **Eigenvectors** = directions that are only stretched, not turned. **SVD** splits any matrix into rotate–scale–rotate and tells you the most important directions.
- ➗ **Equation:** `A v = λ v` · `A = U Σ Vᵀ` · covariance `C = XᵀX/(n−1)` (X centred)
- ⌨️ **Build:** `np.linalg.eig` on a 2×2 (check by hand). SVD of a small image. Rank-k approximation `A_k`.
- 📊 **Measure:** reconstruction error `‖A − A_k‖` vs k. Plot it.
- 📈 **Improve:** k=1 → k=5 → k=20 → choose k that keeps 95 % of the energy.
- 🎤 **Interview:** Eigenvector in plain words? · How is SVD related to PCA? · Why centre the data first?
- ✅ **Done when:** you can compress an image and report the error.

### ☐ Day 6 — Derivatives, chain rule, partial derivatives — *your notes: Loss Functions, Partial Derivatives & GD*
- 🧠 **Idea:** derivative = slope = "how much does the output change if I nudge the input?". Chain rule = functions inside functions. Partial derivative = slope along one input, others fixed. Re-use [advanced_day2_calculus.md](advanced_day2_calculus.md).
- ➗ **Equation:** `f′(x) = lim (f(x+h) − f(x))/h` · chain `d/dx f(g(x)) = f′(g(x))·g′(x)` · `∂L/∂w` for `L = (wx − y)²` is `2x(wx − y)`
- ⌨️ **Build:** numeric derivative (central difference) → test on `x²`, `sin x`, one-weight MSE → compare with PyTorch autograd (reuse [../advanced_day2_calculus.py](../advanced_day2_calculus.py)).
- 📊 **Measure:** numeric vs analytic error shrinks as h gets smaller, then grows again (float noise). Plot it.
- 📈 **Improve:** forward difference → central difference → analytic → autograd.
- 🎤 **Interview:** What is a gradient? · Chain rule in backprop in one sentence? · Why partial derivatives in ML?
- ✅ **Done when:** numeric and analytic gradients agree to 1e-6.

### ☐ Day 7 — Gradient descent by hand — *your notes: Gradient Descent*
- 🧠 **Idea:** to reduce the loss, step **downhill**: opposite to the gradient. Learning rate α = step size.
- ➗ **Equation:** `w ← w − α·∂L/∂w` · for `L = (1/n)Σ(wx−y)²`: `∂L/∂w = (2/n)Σ x(wx−y)` · momentum `v ← βv + ∇L ; w ← w − αv`
- ⌨️ **Build:** GD on `f(x) = (x−3)²`; then on a 1-weight MSE; plot the path on the loss curve; try α = 0.001, 0.1, 1.1.
- 📊 **Measure:** loss per step; α too small = slow, α too big = diverges (show both).
- 📈 **Improve:** fixed α → decaying α → momentum. Count steps to reach loss < 1e-6.
- 🎤 **Interview:** Learning rate too big / too small? · Batch vs stochastic vs mini-batch? · Local minimum vs saddle point?
- ✅ **Done when:** you can predict, before running, whether a given α will diverge.

### ☐ Day 8 — Probability, Bayes, distributions
- 🧠 **Idea:** probability = belief in numbers. **Bayes** updates belief with evidence. Know Normal, Bernoulli, Binomial, Poisson, Uniform.
- ➗ **Equation:** `P(A|B) = P(B|A)·P(A)/P(B)` · `E[X] = Σ x·p(x)` · Normal pdf `1/(σ√(2π)) · exp(−(x−μ)²/(2σ²))`
- ⌨️ **Build:** simulate coins, dice, normal samples. Medical-test / spam example with Bayes from scratch. Monte-Carlo estimate of π.
- 📊 **Measure:** law of large numbers — error of the estimate vs n (plot).
- 📈 **Improve:** guess with no prior → add prior → update with more evidence; watch the posterior move.
- 🎤 **Interview:** Explain Bayes with an example. · Prior vs posterior? · Independent vs uncorrelated?
- ✅ **Done when:** you solve a Bayes problem on paper without help.

### ☐ Day 9 — MLE, entropy, cross-entropy, KL ➜ **Phase 1 checkpoint**
- 🧠 **Idea:** **Maximum likelihood** = choose the parameters that make the data most likely. **Entropy** = surprise. **Cross-entropy** = surprise when you believe q but truth is p. This is the loss of every classifier.
- ➗ **Equation:** `θ̂ = argmax Σ log p(xᵢ|θ)` · `H(p) = −Σ p log p` · `H(p,q) = −Σ p log q` · `KL(p‖q) = Σ p log(p/q) = H(p,q) − H(p)`
- ⌨️ **Build:** MLE of a coin bias and of a normal mean (grid search vs formula). Entropy of fair vs biased coin. Cross-entropy of two distributions. Show: **MSE = MLE under Gaussian noise**, **cross-entropy = MLE for classification**.
- 📊 **Measure:** log-likelihood curve peaks at the MLE.
- 📈 **Improve (checkpoint):** mini-project **"Stats report"** on your sales data (centre, spread, correlations, 3 findings). Wrap `summary(df)` in a FastAPI function + one pytest.
- 🎤 **Interview:** answer **20 questions** from Days 1–9 (write them in `plan120/interview_phase1.md`).
- ✅ **Done when:** you can derive "why cross-entropy" from MLE on one page.

---

# 🧹 PHASE 2 — Data & Features (Days 10–16)

### ☐ Day 10 — EDA & data types
- 🧠 **Idea:** look before you model. Types: numeric (continuous / discrete), categorical (nominal / ordinal), date-time, text.
- ➗ **Equation:** skewness `E[(x−μ)³]/σ³` · IQR rule · missing % `= #NaN / n`
- ⌨️ **Build:** profile your sales data: `shape, dtypes, describe, value_counts, isna().mean()`, duplicates, constant columns; histograms, boxplots, correlation map.
- 📊 **Measure:** write a **data-quality checklist** (missing %, duplicates, skew, wrong dtypes, impossible values).
- 📈 **Improve:** raw → correct dtypes → documented issue list (V3 = issues ranked by impact).
- 🎤 **Interview:** Steps of EDA? · How do you find bad data? · What does a skewed feature do to a model?
- ✅ **Done when:** you have a 1-page EDA report.

### ☐ Day 11 — Missing values & outliers
- 🧠 **Idea:** missing is not random: MCAR / MAR / MNAR. Outliers can be errors or real signals.
- ➗ **Equation:** IQR fence `x < Q1 − 1.5·IQR or x > Q3 + 1.5·IQR` · z-score `|z| > 3` · mean impute `x̂ = x̄`
- ⌨️ **Build:** detect + impute (mean / median / mode / KNN / iterative); add a *missing-indicator* column; outlier methods (IQR, z-score, winsorize).
- 📊 **Measure:** same model, each strategy → validation RMSE (fit imputer on **train only**).
- 📈 **Improve:** drop rows → mean → median → KNN + indicator.
- 🎤 **Interview:** MCAR vs MAR vs MNAR? · Drop or impute? · Why fit the imputer on train only?
- ✅ **Done when:** a table shows the best strategy with numbers.

### ☐ Day 12 — Encoding (7 types) — *your notes: Encoding*
- 🧠 **Idea:** models need numbers. **Label, One-Hot, Binary, Ordinal, Frequency, Mean/Target, Embedding.**
- ➗ **Equation:** one-hot `k categories → k (or k−1) columns` · frequency `count(c)/n` · smoothed target `(Σy_c + m·ȳ)/(n_c + m)`
- ⌨️ **Build:** each by hand, then `OneHotEncoder`, `OrdinalEncoder`, `category_encoders` (Binary, Target).
- 📊 **Measure:** score + number of columns + **leakage check** for target encoding (out-of-fold).
- 📈 **Improve:** label → one-hot → smoothed out-of-fold target encoding on a high-cardinality column.
- 🎤 **Interview:** One-hot vs label? · How to handle 10 000 categories? · Why does target encoding leak?
- ✅ **Done when:** you can pick the encoder for any column in 10 seconds.

### ☐ Day 13 — Scaling & transformation (5 types) — *your notes: Transformation*
- 🧠 **Idea:** put features on similar ranges. **Min-Max, Standardization (Z), Log, Robust, Max-Abs** (+ Power / Quantile).
- ➗ **Equation:** `(x−min)/(max−min)` · `(x−μ)/σ` · `(x−median)/IQR` · `x/max|x|` · `log(1+x)`
- ⌨️ **Build:** from scratch + sklearn. Skewed salary before/after log. Fit on train only.
- 📊 **Measure:** KNN / SVM / logistic / tree score **with vs without** scaling.
- 📈 **Improve:** none → standard → robust → log + standard.
- 🎤 **Interview:** Which models need scaling? · Normalization vs standardization? · Why log for skew?
- ✅ **Done when:** you can show trees ignore scaling and KNN does not.

### ☐ Day 14 — Feature creation, selection, extraction
- 🧠 **Idea:** make new features (ratios, dates, interactions). **Selection** keeps some columns (filter / wrapper / embedded). **Extraction** builds new ones (PCA).
- ➗ **Equation:** mutual information `I(X;Y) = ΣΣ p(x,y) log[p(x,y)/(p(x)p(y))]` · `VIF = 1/(1−R²)` · polynomial `x₁x₂, x₁²`
- ⌨️ **Build:** date-time parts, lag, ratio, interaction, polynomial; correlation / mutual-info / chi² filters; RFE; Lasso / tree importance.
- 📊 **Measure:** score vs number of features (plot).
- 📈 **Improve:** all features → filter → RFE → embedded; keep the smallest set within 1 % of the best.
- 🎤 **Interview:** Selection vs extraction? · What is multicollinearity? · Filter vs wrapper vs embedded?
- ✅ **Done when:** you removed ≥ 30 % of features with no score loss.

### ☐ Day 15 — Imbalanced data & data leakage
- 🧠 **Idea:** when 98 % of rows are "normal", accuracy lies. Fix with weights, re-sampling (SMOTE), and the right metric + threshold.
- ➗ **Equation:** class weight `w_c = n/(k·n_c)` · SMOTE `x_new = xᵢ + λ(x_nn − xᵢ)`, `λ ∈ [0,1]`
- ⌨️ **Build:** make a 2 % fraud set. Show the accuracy trap. `class_weight`, random over/under, SMOTE, SMOTE-Tomek (inside CV only!). Leakage demo: scale **before** split → inflated score.
- 📊 **Measure:** confusion matrix, recall, **PR-AUC** (not accuracy).
- 📈 **Improve:** baseline → class weights → SMOTE in CV → threshold tuning.
- 🎤 **Interview:** Why does accuracy fail? · Why SMOTE only inside CV? · Name 3 leakage examples.
- ✅ **Done when:** you can catch leakage in someone else's notebook.

### ☐ Day 16 — Pipelines ➜ **Phase 2 checkpoint**
- 🧠 **Idea:** put every step in one `Pipeline` + `ColumnTransformer`, so the same steps run in training and in production, with no leakage.
- ➗ **Equation:** none — think "fit on train → transform everything".
- ⌨️ **Build:** full pipeline (impute → encode → scale → select) on the sales data; `joblib.dump`; reload and predict.
- 📊 **Measure:** CV score of the whole pipeline.
- 📈 **Improve (checkpoint):** mini-project **"Clean-and-feature pipeline"**; FastAPI function `prepare(df)` + pytest; commit.
- 🎤 **Interview:** answer **20 questions** from Days 10–16.
- ✅ **Done when:** a new CSV goes through the saved pipeline with one call.

---

# 📈 PHASE 3 — Classical Machine Learning (Days 17–47)

## 3a. Linear models for numbers (Days 17–23)

### ☐ Day 17 — Simple linear regression: the line & the residual — *your notes: Pandas + Simple Linear Regression + Residuals*
- 🧠 **Idea:** predict a number from one feature with a straight line. **Residual** = actual − predicted.
- ➗ **Equation:** `ŷ = w·x + b` · `eᵢ = yᵢ − ŷᵢ` · closed form `w = Σ(x−x̄)(y−ȳ) / Σ(x−x̄)²`, `b = ȳ − w·x̄`
- ⌨️ **Build:** compute w, b by hand on 10 points; plot line + residuals; `LinearRegression`; read `coef_`, `intercept_`.
- 📊 **Measure:** `Σe ≈ 0`; RMSE vs the Day-1 mean baseline.
- 📈 **Improve:** mean baseline → best single feature (use r from Day 3).
- 🎤 **Interview:** What is a residual? · Meaning of slope and intercept? · Why *squared* errors?
- ✅ **Done when:** your w, b equal sklearn's.

### ☐ Day 18 — Cost function & the normal equation — *your notes: Cost Functions*
- 🧠 **Idea:** the **cost** `J` scores a line; the best line is the lowest point of a bowl-shaped surface. The normal equation jumps straight to the bottom.
- ➗ **Equation:** `J(w,b) = (1/2n) Σ(ŷᵢ − yᵢ)²` (the ½ cancels the 2 from the derivative) · matrix `J = (1/2n)‖Xw − y‖²` · `w = (XᵀX)⁻¹ Xᵀ y`
- ⌨️ **Build:** contour plot of `J(w,b)`; solve normal equation with NumPy; compare with sklearn.
- 📊 **Measure:** same weights. Error analysis: make columns collinear → `XᵀX` is singular (see the error).
- 📈 **Improve:** `inv` → `pinv` / `lstsq` → add regularization (preview of Day 23).
- 🎤 **Interview:** Why MSE and not sum of absolute error? · When does the normal equation fail? · Its time cost?
- ✅ **Done when:** you can draw the cost bowl and mark the minimum.

### ☐ Day 19 — Gradient descent for linear regression (from scratch)
- 🧠 **Idea:** same bowl, but walk down in small steps. Needed when data is huge.
- ➗ **Equation:** `∂J/∂w = (1/n)Σ(ŷ−y)x` · `∂J/∂b = (1/n)Σ(ŷ−y)` · vector form `∇J = (1/n)Xᵀ(Xw − y)` · `w ← w − α∇J`
- ⌨️ **Build:** batch GD, SGD, mini-batch; loss curve; **with and without feature scaling**.
- 📊 **Measure:** steps to converge; final RMSE must equal the normal equation.
- 📈 **Improve:** raw features → scaled → tuned α → momentum.
- 🎤 **Interview:** Batch vs SGD vs mini-batch? · Why scale features for GD? · How do you know it converged?
- ✅ **Done when:** GD weights match the normal-equation weights to 4 decimals.

### ☐ Day 20 — Multiple linear regression & its assumptions — *your notes: Linear Regression*
- 🧠 **Idea:** many features. Read each coefficient as "change in y when this x goes up 1, others fixed". Check the assumptions (LINE).
- ➗ **Equation:** `ŷ = w₁x₁ + … + w_p x_p + b = Xw` · Assumptions: **L**inearity, **I**ndependence, **N**ormal residuals, **E**qual variance
- ⌨️ **Build:** sklearn + `statsmodels` OLS summary (coef, std err, p-value, R², F-stat). Residual-vs-fitted plot, Q-Q plot, VIF.
- 📊 **Measure:** which assumption is broken and how it looks on the plot.
- 📈 **Improve:** raw → drop collinear → log-target → add polynomial term.
- 🎤 **Interview:** Assumptions of linear regression? · How to read a coefficient? · What does multicollinearity do?
- ✅ **Done when:** you can read an OLS table line by line.

### ☐ Day 21 — Regression metrics
- 🧠 **Idea:** pick the metric that matches the business. **R² is not accuracy** — it is "share of variance explained".
- ➗ **Equation:** `MAE = (1/n)Σ|e|` · `MSE = (1/n)Σe²` · `RMSE = √MSE` · `R² = 1 − SS_res/SS_tot` · `adj R² = 1 − (1−R²)(n−1)/(n−p−1)` · `MAPE = (100/n)Σ|e/y|`
- ⌨️ **Build:** all metrics from scratch → compare with `sklearn.metrics`.
- 📊 **Measure:** add 3 outliers → see RMSE jump, MAE barely move. When can R² be negative?
- 📈 **Improve:** choose MAE for "typical error", RMSE when big errors are costly; report both.
- 🎤 **Interview:** MSE vs MAE vs RMSE? · Can R² be negative? · Why adjusted R²?
- ✅ **Done when:** you can justify a metric for 3 business cases.

### ☐ Day 22 — Overfitting, underfitting & bias–variance — *your notes: Bias-Variance*
- 🧠 **Idea:** too simple = **high bias** (underfit). Too flexible = **high variance** (overfit). Find the middle.
- ➗ **Equation:** `E[(y − ŷ)²] = Bias² + Variance + Noise`
- ⌨️ **Build:** polynomial degree 1…15 on noisy data; train vs validation error; **learning curve** and **validation curve**.
- 📊 **Measure:** the train–validation gap.
- 📈 **Improve:** underfit → add features/degree · overfit → more data, regularize, simplify.
- 🎤 **Interview:** Define bias and variance. · How do learning curves show which one you have? · Four ways to reduce overfitting?
- ✅ **Done when:** you can read a learning curve and say what to do next.

### ☐ Day 23 — Regularization (Ridge, Lasso, ElasticNet) ➜ **checkpoint 3a**
- 🧠 **Idea:** punish big weights so the model stays simple. Ridge shrinks; Lasso can set weights to exactly 0 (feature selection).
- ➗ **Equation:** Ridge `J + λΣw²` · Lasso `J + λΣ|w|` · ElasticNet `J + λ(ρΣ|w| + (1−ρ)Σw²/2)` · Ridge closed form `w = (XᵀX + λI)⁻¹Xᵀy`
- ⌨️ **Build:** Ridge from scratch (closed form) → check sklearn; Lasso with sklearn; coefficient-vs-λ path; `RidgeCV`, `LassoCV`.
- 📊 **Measure:** validation RMSE vs λ (U-shaped curve).
- 📈 **Improve (ladder, log it):** linear → polynomial → poly + Ridge → poly + ElasticNet (tuned).
- 🎤 **Interview:** L1 vs L2 — why does L1 give zeros? · How to choose λ? · Why scale before regularizing?
- ✅ **Checkpoint:** mini-project **"Price predictor"** (sales / diabetes) + FastAPI `/predict` + test + 20 interview questions.

## 3b. Linear models for categories (Days 24–27)

### ☐ Day 24 — Logistic regression: sigmoid & log loss
- 🧠 **Idea:** predict the **probability** of "yes". Squash a linear score into 0…1.
- ➗ **Equation:** `p = σ(z) = 1/(1+e^(−z))`, `z = w·x + b` · log loss `L = −(1/n)Σ[y·log p + (1−y)·log(1−p)]` · gradient `∇ = (1/n)Xᵀ(p − y)` (same shape as linear regression!)
- ⌨️ **Build:** sigmoid, loss, GD from scratch on `breast_cancer`; 2-D decision boundary plot; compare `LogisticRegression`.
- 📊 **Measure:** accuracy + loss curve; coefficient = change in **log-odds**.
- 📈 **Improve:** unscaled → scaled → tuned α → L2 `C`.
- 🎤 **Interview:** Why sigmoid? · Why not MSE for classification? · How to read a coefficient (odds ratio)?
- ✅ **Done when:** your GD model matches sklearn within 1 %.

### ☐ Day 25 — Multi-class: softmax
- 🧠 **Idea:** many classes → one score per class → turn scores into probabilities that add to 1.
- ➗ **Equation:** `softmax(zₖ) = e^{zₖ}/Σⱼ e^{zⱼ}` · cross-entropy `L = −Σₖ yₖ log pₖ` · gradient w.r.t. scores `= p − y`
- ⌨️ **Build:** softmax regression from scratch on `digits` / `wine` (subtract max for stability); One-vs-Rest vs multinomial in sklearn.
- 📊 **Measure:** per-class precision/recall; confusion matrix; which digits are confused and why.
- 📈 **Improve:** raw pixels → scaled → regularized → tuned C.
- 🎤 **Interview:** Softmax vs sigmoid? · OvR vs OvO? · Why subtract the max?
- ✅ **Done when:** you can explain the confusion matrix of digits.

### ☐ Day 26 — Classification metrics
- 🧠 **Idea:** different mistakes cost different money. Pick the metric from the cost.
- ➗ **Equation:** `Precision = TP/(TP+FP)` · `Recall = TP/(TP+FN)` · `F1 = 2PR/(P+R)` · `FPR = FP/(FP+TN)` · ROC-AUC = P(score of random positive > random negative) · macro / micro / weighted averages
- ⌨️ **Build:** confusion matrix by hand; ROC and PR curves from thresholds; `classification_report`.
- 📊 **Measure:** fraud (miss = costly) vs spam (false alarm = costly): which metric?
- 📈 **Improve:** accuracy → F1 → PR-AUC for imbalanced data.
- 🎤 **Interview:** Precision–recall trade-off? · What does AUC mean? · ROC-AUC vs PR-AUC?
- ✅ **Done when:** you can compute F1 on paper from a 2×2 table.

### ☐ Day 27 — Thresholds & calibration ➜ **checkpoint 3b**
- 🧠 **Idea:** 0.5 is not magic. Choose the threshold from cost. A good probability should be **calibrated** ("70 % → right 70 % of the time").
- ➗ **Equation:** expected cost `C_FP·FP + C_FN·FN` · Brier score `(1/n)Σ(p − y)²`
- ⌨️ **Build:** threshold sweep that minimizes cost; calibration curve; `CalibratedClassifierCV`.
- 📊 **Measure:** cost at 0.5 vs best threshold.
- 📈 **Improve:** default → best threshold → calibrated.
- 🎤 **Interview:** How do you choose a threshold? · What is calibration and when does it matter?
- ✅ **Checkpoint:** mini-project **"Employee attrition / churn classifier"** + FastAPI + test + 20 questions (Days 24–27).

## 3c. KNN, Naive Bayes, SVM (Days 28–31)

### ☐ Day 28 — K-Nearest Neighbours — *your notes: Distance Metrics*
- 🧠 **Idea:** "tell me who your neighbours are". No training; all work at prediction time.
- ➗ **Equation:** `ŷ = majority / mean of the k nearest` · weighted vote `wᵢ = 1/dᵢ`
- ⌨️ **Build:** from scratch with NumPy; k vs validation error curve; effect of scaling; KD-tree timing.
- 📊 **Measure:** bias–variance in k (k=1 overfits, big k underfits).
- 📈 **Improve:** k=1 → tuned k → scaled → distance-weighted → better metric.
- 🎤 **Interview:** How to choose k? · Why is predict slow? · Why does KNN suffer in high dimensions?
- ✅ **Done when:** from-scratch KNN = sklearn KNN.

### ☐ Day 29 — Naive Bayes
- 🧠 **Idea:** Bayes' rule + the "naive" assumption that features are independent given the class.
- ➗ **Equation:** `P(c|x) ∝ P(c)·Πᵢ P(xᵢ|c)` · Laplace smoothing `(count + α)/(N + α·V)` · Gaussian NB uses the normal pdf per class
- ⌨️ **Build:** spam toy example from scratch (use log-probabilities); sklearn `GaussianNB`, `MultinomialNB`.
- 📊 **Measure:** what breaks if a word was never seen (zero probability).
- 📈 **Improve:** no smoothing → Laplace → TF-IDF features.
- 🎤 **Interview:** Why "naive"? · Zero-frequency problem? · Why is it good on text?
- ✅ **Done when:** you can compute a spam probability by hand.

### ☐ Day 30 — Support Vector Machine
- 🧠 **Idea:** draw the line with the **widest margin**. Support vectors = the points that touch the margin. Kernels bend the line.
- ➗ **Equation:** hyperplane `w·x + b = 0` · margin `2/‖w‖` · hinge loss `max(0, 1 − y(w·x + b))` · soft margin `½‖w‖² + C·Σξᵢ` · RBF kernel `exp(−γ‖x − x′‖²)`
- ⌨️ **Build:** linear SVM by sub-gradient descent from scratch; `SVC` with linear / poly / RBF kernels.
- 📊 **Measure:** effect of C (soft vs hard margin) and γ (smooth vs wiggly boundary) on `make_moons`.
- 📈 **Improve:** linear → RBF → tuned (C, γ) → scaled.
- 🎤 **Interview:** What are support vectors? · Role of C and gamma? · What is the kernel trick?
- ✅ **Done when:** you can draw margin + support vectors on paper.

### ☐ Day 31 — Model shoot-out ➜ **checkpoint 3c**
- 🧠 **Idea:** no model wins everywhere ("no free lunch"). Compare fairly: same split, same CV, same metric.
- ➗ **Equation:** `CV score = (1/K)Σ scoreₖ` ± std.
- ⌨️ **Build:** logistic, KNN, NB, SVM on 3 datasets with the same 5-fold CV; one summary table.
- 📊 **Measure:** accuracy, F1, train time, predict time.
- 📈 **Improve:** write a one-page **"how to choose a model"** guide from your own table.
- 🎤 **Interview:** answer **20 questions** on Days 24–31. When KNN? When SVM? When NB?
- ✅ **Checkpoint:** FastAPI endpoint that serves the best model + test.

## 3d. Trees & ensembles (Days 32–38)

### ☐ Day 32 — Decision tree: how a split is chosen — *your notes: Decision Tree*
- 🧠 **Idea:** a flowchart of yes/no questions. At each node pick the question that makes the groups **purest**.
- ➗ **Equation:** entropy `H = −Σ pᵢ log₂ pᵢ` · Gini `1 − Σ pᵢ²` · information gain `IG = H(parent) − Σ (nᵢ/n)·H(childᵢ)` · regression: variance (MSE) reduction
- ⌨️ **Build:** compute IG by hand on the small "play tennis" table; best-split search over thresholds for one numeric column.
- 📊 **Measure:** Gini vs entropy choose (almost) the same splits — show it.
- 📈 **Improve:** one split (stump) → depth 2 → depth 3: log accuracy.
- 🎤 **Interview:** Entropy vs Gini? · What is information gain? · How are numeric features split?
- ✅ **Done when:** your hand-made tree equals `DecisionTreeClassifier` on the toy table.

### ☐ Day 33 — Tree from scratch, overfitting & pruning
- 🧠 **Idea:** a full tree memorizes. Limit it or prune it.
- ➗ **Equation:** cost-complexity `R_α(T) = R(T) + α·|T|` (|T| = number of leaves) · stop rules: `max_depth`, `min_samples_leaf`
- ⌨️ **Build:** recursive tree (~60 lines) → compare sklearn; `plot_tree`; `ccp_alpha` path.
- 📊 **Measure:** train vs validation accuracy as depth grows.
- 📈 **Improve:** full tree → depth-limited → pruned (log all).
- 🎤 **Interview:** Why do trees overfit? · Pre-pruning vs post-pruning? · Pros and cons of trees?
- ✅ **Done when:** your tree gets within 2 % of sklearn.

### ☐ Day 34 — Bagging & Random Forest — *your notes: Random Forest*
- 🧠 **Idea:** many different trees vote. Each tree sees a random sample of rows and a random subset of features → errors cancel.
- ➗ **Equation:** bootstrap keeps ≈ 63.2 % unique rows · variance of an average `ρσ² + (1−ρ)σ²/B` · features per split `≈ √p`
- ⌨️ **Build:** bagging of your trees from scratch; `RandomForest`; **OOB score**; impurity vs **permutation** importance.
- 📊 **Measure:** accuracy vs number of trees (plateau); OOB ≈ CV score.
- 📈 **Improve:** one tree → bagging → random forest → tuned (`max_features`, `min_samples_leaf`).
- 🎤 **Interview:** Why does averaging reduce variance? · What is OOB? · Why is impurity importance biased?
- ✅ **Done when:** you can explain `ρ` (tree correlation) and why feature sub-sampling lowers it.

### ☐ Day 35 — AdaBoost
- 🧠 **Idea:** train weak learners one after another; **raise the weight of rows the last learner got wrong**.
- ➗ **Equation:** error `εₜ = Σ wᵢ·1[hₜ(xᵢ) ≠ yᵢ]` · learner weight `αₜ = ½ ln((1−εₜ)/εₜ)` · `wᵢ ← wᵢ·exp(−αₜ yᵢ hₜ(xᵢ))` (then normalize) · `H(x) = sign(Σ αₜ hₜ(x))`
- ⌨️ **Build:** AdaBoost with decision stumps from scratch; sklearn `AdaBoostClassifier`.
- 📊 **Measure:** sample-weight plot per round; sensitivity to noisy labels.
- 📈 **Improve:** 1 stump → 50 → 200 rounds → tuned learning rate.
- 🎤 **Interview:** How does AdaBoost pick weights? · Why sensitive to outliers? · Bagging vs boosting?
- ✅ **Done when:** from-scratch accuracy ≈ sklearn.

### ☐ Day 36 — Gradient Boosting
- 🧠 **Idea:** each new tree fits the **mistakes (residuals)** of the model so far. It is gradient descent in "function space".
- ➗ **Equation:** `Fₘ(x) = Fₘ₋₁(x) + ν·hₘ(x)` · for squared loss, `hₘ` fits `rᵢ = yᵢ − Fₘ₋₁(xᵢ)` (the negative gradient) · `ν` = learning rate
- ⌨️ **Build:** gradient boosting regressor from scratch with depth-3 trees; compare `GradientBoostingRegressor`.
- 📊 **Measure:** validation error vs number of trees (it turns up → overfit) → early stopping.
- 📈 **Improve:** ν=1 → ν=0.1 with more trees → subsample 0.8 → early stopping.
- 🎤 **Interview:** Why is it called *gradient* boosting? · Learning rate vs n_estimators? · Boosting vs random forest?
- ✅ **Done when:** your from-scratch model matches sklearn's RMSE within 3 %.

### ☐ Day 37 — XGBoost, LightGBM, CatBoost
- 🧠 **Idea:** gradient boosting made fast and regularized. Uses first **and second** derivatives.
- ➗ **Equation:** objective `Σ L(yᵢ, ŷᵢ) + Σ Ω(f)`, `Ω = γT + ½λΣw²` · best leaf weight `w* = −G/(H + λ)` (G = Σ gradients, H = Σ hessians) · split gain `½[G_L²/(H_L+λ) + G_R²/(H_R+λ) − (G_L+G_R)²/(H_L+H_R+λ)] − γ`
- ⌨️ **Build:** the three libraries on the same tabular set; early stopping; feature importance; CatBoost with raw categorical columns.
- 📊 **Measure:** score, train time, memory. LightGBM = leaf-wise growth; XGBoost = level-wise; CatBoost = ordered target statistics.
- 📈 **Improve:** defaults → key params (`learning_rate, max_depth, subsample, colsample_bytree, reg_lambda`) → Optuna (Day 44).
- 🎤 **Interview:** What does XGBoost add over GBM? · Leaf-wise vs level-wise? · Why is CatBoost good with categories?
- ✅ **Done when:** you can name the 5 most important boosting params and what each does.

### ☐ Day 38 — Stacking, voting, blending ➜ **checkpoint 3d**
- 🧠 **Idea:** combine different models. A **meta-learner** learns how to trust each one, using **out-of-fold** predictions.
- ➗ **Equation:** voting `ŷ = argmax Σ wₘ·1[ŷₘ = c]` · blending `ŷ = Σ wₘ ŷₘ`
- ⌨️ **Build:** `VotingClassifier`, `StackingClassifier`; manual out-of-fold stacking.
- 📊 **Measure:** gain over the best single model; correlation between model errors.
- 📈 **Improve:** best single → soft vote → stack with logistic meta-learner.
- 🎤 **Interview:** Stacking vs blending? · Why out-of-fold? · When does an ensemble not help?
- ✅ **Checkpoint:** **"Tabular benchmark"** — one table with *all* models from Days 17–38 on one dataset (CV score, time) + FastAPI + 20 questions.

## 3e. Unsupervised learning (Days 39–42)

### ☐ Day 39 — K-Means
- 🧠 **Idea:** find k group centres; assign each point to the nearest centre; move centres; repeat.
- ➗ **Equation:** `J = Σₖ Σ_{x∈Cₖ} ‖x − μₖ‖²` · update `μₖ = mean of Cₖ` · silhouette `s = (b − a)/max(a, b)`
- ⌨️ **Build:** Lloyd's algorithm from scratch; k-means++ start; elbow plot + silhouette; customer segmentation on sales data.
- 📊 **Measure:** inertia, silhouette, stability across seeds.
- 📈 **Improve:** random start → k-means++ → scaled features → best k.
- 🎤 **Interview:** How to choose k? · Weaknesses of K-means? · Why scale features?
- ✅ **Done when:** you can explain why K-means fails on moons.

### ☐ Day 40 — Hierarchical, DBSCAN, Gaussian Mixture
- 🧠 **Idea:** other ways to group: build a tree of merges; or by **density**; or soft assignments with Gaussians.
- ➗ **Equation:** linkage (single / complete / ward) · DBSCAN: core point has ≥ `minPts` neighbours within `ε` · GMM `p(x) = Σₖ πₖ·N(x|μₖ, Σₖ)` (fit with EM)
- ⌨️ **Build:** dendrogram; DBSCAN on moons; `GaussianMixture`; compare on blobs / moons / circles.
- 📊 **Measure:** silhouette, adjusted Rand index (if labels exist), noise points found.
- 📈 **Improve:** K-means → DBSCAN (tuned ε) → GMM; pick by data shape.
- 🎤 **Interview:** When DBSCAN over K-means? · Hard vs soft clustering? · What does EM do?
- ✅ **Done when:** you can choose a clustering method from a scatter plot.

### ☐ Day 41 — PCA from scratch + t-SNE / UMAP
- 🧠 **Idea:** PCA = rotate the data so the first axis has the most variance. Keep the top axes. t-SNE / UMAP = pictures that keep neighbours together.
- ➗ **Equation:** centre `X`; `C = XᵀX/(n−1)`; eigenvectors `W`; project `Z = XW_k`; explained variance ratio `λᵢ/Σλ` · t-SNE minimizes `KL(P‖Q)`
- ⌨️ **Build:** PCA with `np.linalg.eigh`, compare sklearn; reconstruct; scree plot; t-SNE / UMAP on `digits`.
- 📊 **Measure:** accuracy of a classifier on PCA features vs k.
- 📈 **Improve:** raw → scaled → PCA 95 % → (compare) t-SNE only for plots.
- 🎤 **Interview:** What does PCA maximize? · Why not use t-SNE for features? · How many components?
- ✅ **Done when:** your PCA = sklearn PCA (up to sign).

### ☐ Day 42 — Anomaly detection ➜ **checkpoint 3e**
- 🧠 **Idea:** find the rare and strange rows. Your **HRM payslip detector** is exactly this.
- ➗ **Equation:** Isolation Forest score `s(x,n) = 2^(−E[h(x)]/c(n))` (short path = anomaly) · LOF = local density ratio · z-score
- ⌨️ **Build:** Isolation Forest, LOF, One-Class SVM on HRM payslips (reuse `hrm_detective/`); inject known anomalies to test.
- 📊 **Measure:** precision@k, recall of injected anomalies; look at false alarms.
- 📈 **Improve:** z-score → Isolation Forest → tuned contamination → add rule-based checks.
- 🎤 **Interview:** Supervised vs unsupervised anomaly detection? · How do you evaluate with no labels? · Contamination parameter?
- ✅ **Checkpoint:** **"Payslip anomaly service"** + FastAPI + test + 20 questions (Days 39–42).

## 3f. Evaluate, tune, explain (Days 43–47)

### ☐ Day 43 — Cross-validation & honest evaluation
- 🧠 **Idea:** one split can be lucky. Use K folds. Use the *right* split for the data.
- ➗ **Equation:** `CV = (1/K)Σ scoreₖ` and `±` standard deviation · nested CV = outer loop (evaluate) + inner loop (tune)
- ⌨️ **Build:** K-Fold, Stratified, Group, **TimeSeriesSplit**, LOOCV, repeated CV; nested CV.
- 📊 **Measure:** spread of scores; show that tuning on the test set inflates the score.
- 📈 **Improve:** single split → K-fold → repeated → nested.
- 🎤 **Interview:** Why stratified? · Why not shuffle time series? · What is nested CV for?
- ✅ **Done when:** you can pick the CV scheme for any dataset.

### ☐ Day 44 — Hyper-parameter tuning
- 🧠 **Idea:** settings that are not learned (depth, λ, k). Search them smartly.
- ➗ **Equation:** random search finds a top-p region with probability `1 − (1−p)ⁿ` (n = 60 tries → 95 % for the top 5 %) · Bayesian / TPE: model the score, pick the next try by expected improvement
- ⌨️ **Build:** `GridSearchCV`, `RandomizedSearchCV`, **Optuna** (TPE), successive halving; genetic idea.
- 📊 **Measure:** best score vs number of trials (same budget for each method).
- 📈 **Improve:** defaults → grid → random → Optuna (all with the same time budget).
- 🎤 **Interview:** Grid vs random? · What is Bayesian optimization? · How do you avoid overfitting the validation set?
- ✅ **Done when:** you log a tuning curve for one model.

### ☐ Day 45 — Explainability, error analysis, fairness ➜ **checkpoint 3f**
- 🧠 **Idea:** know *why* a model decides. Find **which groups** it fails on. Check fairness.
- ➗ **Equation:** permutation importance `= score − score(shuffled feature)` · SHAP `φᵢ = Σ_{S⊆F∖{i}} [|S|!(|F|−|S|−1)!/|F|!]·[f(S∪{i}) − f(S)]` · demographic parity `P(ŷ=1|A=a) = P(ŷ=1|A=b)`
- ⌨️ **Build:** permutation importance, SHAP summary + force plot, LIME, partial-dependence; error by slice (e.g. department, month).
- 📊 **Measure:** the 3 worst slices; fairness gap between groups.
- 📈 **Improve:** fix the worst slice (features / weights / more data) and re-measure.
- 🎤 **Interview:** SHAP vs permutation importance? · What is partial dependence? · How do you check fairness?
- ✅ **Checkpoint:** one full **ML project report** (problem → data → baseline → ladder → errors → explanation). 20 questions (Days 43–45).

### ☐ Day 46 — Time series
- 🧠 **Idea:** order matters; never shuffle. Trend + seasonality + noise. Predict the future from the past.
- ➗ **Equation:** AR(1) `yₜ = c + φ·yₜ₋₁ + εₜ` · ARIMA(p,d,q) = AR + differencing + MA · autocorrelation `ρₖ = Cov(yₜ, yₜ₋ₖ)/Var(y)` · `sMAPE = (100/n)Σ 2|e|/(|y|+|ŷ|)`
- ⌨️ **Build:** decompose; stationarity (ADF test); lag + rolling features + gradient boosting; ARIMA / Prophet; **expanding-window backtest** on your sales data.
- 📊 **Measure:** MAPE / sMAPE vs the **seasonal-naive** baseline (must beat it).
- 📈 **Improve:** naive → seasonal-naive → ARIMA → lag features + LightGBM.
- 🎤 **Interview:** What is stationarity? · Why not random CV for time series? · Naive baseline for forecasting?
- ✅ **Done when:** your forecast beats seasonal-naive in a backtest.

### ☐ Day 47 — Recommenders, A/B tests, causal thinking ➜ **PHASE 3 checkpoint**
- 🧠 **Idea:** recommend with similarity or with latent factors. **A/B test** = the honest way to know if a change works. Causal ≠ correlation.
- ➗ **Equation:** user-CF cosine `sim(u,v)` · matrix factorization `r̂ᵤᵢ = pᵤ·qᵢ`, loss `Σ(rᵤᵢ − pᵤ·qᵢ)² + λ(‖p‖² + ‖q‖²)` · NDCG · two-proportion z-test
- ⌨️ **Build:** item-based CF; small matrix factorization with SGD; A/B-test calculator (sample size + p-value).
- 📊 **Measure:** precision@k, NDCG; A/B: effect size + confidence interval.
- 📈 **Improve:** popularity baseline → CF → matrix factorization.
- 🎤 **Interview:** Cold-start problem? · How big must an A/B test be? · Confounder example?
- ✅ **Phase checkpoint:** **mock interview — 50 classical-ML questions** (record yourself) + review the "algorithm cards" for Days 17–46.

---

# 🧠 PHASE 4 — Deep Learning (Days 48–59)

### ☐ Day 48 — The neuron & the perceptron
- 🧠 **Idea:** a neuron = weighted sum + a bend (activation). One neuron = a linear classifier. It **cannot** solve XOR.
- ➗ **Equation:** `z = w·x + b`, `a = f(z)` · perceptron update `w ← w + η(y − ŷ)x`
- ⌨️ **Build:** perceptron from scratch (AND, OR works; XOR fails) → plot the decision line.
- 📊 **Measure:** epochs until no errors; XOR stays at 50 %.
- 📈 **Improve:** 1 neuron → add a hidden layer (preview of Day 49).
- 🎤 **Interview:** Why can't one neuron solve XOR? · Role of the bias? · Perceptron vs logistic regression?
- ✅ **Done when:** you can explain XOR failure with a drawing.

### ☐ Day 49 — Multi-layer network: forward pass & activations
- 🧠 **Idea:** stack layers. Without a non-linear activation, many layers = one linear layer.
- ➗ **Equation:** `a⁽ˡ⁾ = f(W⁽ˡ⁾a⁽ˡ⁻¹⁾ + b⁽ˡ⁾)` · ReLU `max(0,z)` · sigmoid · tanh · softmax · GELU · parameters of a layer `= n_in·n_out + n_out`
- ⌨️ **Build:** 2-layer forward pass in NumPy with random weights; derivative of every activation; count parameters by hand vs `sum(p.numel())`.
- 📊 **Measure:** shape check for every tensor; saturating sigmoid → tiny gradients.
- 📈 **Improve:** sigmoid → tanh → ReLU: compare output ranges and gradient sizes.
- 🎤 **Interview:** Why non-linear activations? · Why ReLU? · Dying ReLU?
- ✅ **Done when:** you predict every tensor shape before running.

### ☐ Day 50 — Loss functions — *your notes: Loss Functions*
- 🧠 **Idea:** the loss is the only thing the network "feels". Choose it for the task.
- ➗ **Equation:** MSE `(y−ŷ)²` · MAE `|y−ŷ|` · Huber `½e²` if `|e| ≤ δ` else `δ(|e| − ½δ)` · BCE `−[y log p + (1−y)log(1−p)]` · CE `−Σ y log p` · hinge `max(0, 1 − y·f)` · softmax+CE gradient `= p − y`
- ⌨️ **Build:** all losses from scratch vs `torch.nn`; plot each loss against the error.
- 📊 **Measure:** training with outliers: MSE vs MAE vs Huber.
- 📈 **Improve:** MSE → Huber on noisy targets; BCE with `pos_weight` on imbalance.
- 🎤 **Interview:** Why cross-entropy for classification? · Huber vs MSE? · What is `BCEWithLogitsLoss` and why use it?
- ✅ **Done when:** you can choose a loss for 5 tasks.

### ☐ Day 51 — Backpropagation by hand
- 🧠 **Idea:** the chain rule, applied layer by layer from the loss back to every weight.
- ➗ **Equation:** output error `δ⁽²⁾ = p − y` (softmax + CE) · hidden error `δ⁽¹⁾ = (W⁽²⁾ᵀδ⁽²⁾) ⊙ f′(z⁽¹⁾)` · `∂L/∂W⁽ˡ⁾ = δ⁽ˡ⁾·a⁽ˡ⁻¹⁾ᵀ` · `∂L/∂b⁽ˡ⁾ = δ⁽ˡ⁾`
- ⌨️ **Build:** pen-and-paper backprop for a 2-2-1 net with real numbers; then NumPy; **gradient check** `(L(w+h) − L(w−h))/2h`.
- 📊 **Measure:** analytic vs numeric gradient error < 1e-6.
- 📈 **Improve:** find and fix one bug on purpose (transpose, missing `f′`).
- 🎤 **Interview:** Explain backprop in 3 sentences. · Why is it efficient? · What is a vanishing gradient?
- ✅ **Done when:** you can do one backprop step on paper.

### ☐ Day 52 — Neural network from scratch (NumPy)
- 🧠 **Idea:** build the whole loop yourself: forward → loss → backward → update.
- ➗ **Equation:** He init `Var(w) = 2/n_in` · Xavier `Var(w) = 2/(n_in + n_out)` · mini-batch update `w ← w − α·(1/m)Σ∇`
- ⌨️ **Build:** a network class (XOR first, then `digits`); mini-batches; accuracy curve.
- 📊 **Measure:** loss + accuracy per epoch; error analysis on mistakes.
- 📈 **Improve:** zero init (fails — why?) → small random → He init → tuned α.
- 🎤 **Interview:** Why not initialize with zeros? · Mini-batch size trade-offs? · How do you know the net is learning?
- ✅ **Done when:** > 95 % on `digits` with pure NumPy.

### ☐ Day 53 — PyTorch basics
- 🧠 **Idea:** PyTorch = NumPy + automatic gradients + GPU.
- ➗ **Equation:** `loss.backward()` computes `∂loss/∂θ` for every parameter by the chain rule you did on Day 51.
- ⌨️ **Build:** tensors, `requires_grad`, `autograd`, `nn.Module`, `nn.Linear`; rebuild Day 52's net; **check gradients equal your NumPy gradients**.
- 📊 **Measure:** same loss curve as Day 52.
- 📈 **Improve:** manual weights → `nn.Sequential` → custom `nn.Module`.
- 🎤 **Interview:** What does `zero_grad()` do? · `detach()` vs `no_grad()`? · Static vs dynamic graph?
- ✅ **Done when:** PyTorch and NumPy gradients match.

### ☐ Day 54 — The training loop & MNIST
- 🧠 **Idea:** the 5 steps — zero_grad → forward → loss → backward → step. Datasets, DataLoaders, batches, train/eval mode.
- ➗ **Equation:** accuracy `= correct/total` · epoch = one pass over data
- ⌨️ **Build:** `Dataset` + `DataLoader`; train MNIST; eval loop with `model.eval()` and `no_grad()`; save/load `state_dict`.
- 📊 **Measure:** train vs validation accuracy per epoch; confusion matrix.
- 📈 **Improve:** logistic regression (linear) → 1 hidden layer → 2 hidden layers.
- 🎤 **Interview:** `train()` vs `eval()`? · Why shuffle? · What is an epoch vs a step?
- ✅ **Done when:** > 97 % on MNIST test.

### ☐ Day 55 — Optimizers & learning-rate schedules
- 🧠 **Idea:** smarter steps. Momentum keeps speed. Adam adapts the step per weight.
- ➗ **Equation:** momentum `v ← βv + g; w ← w − αv` · RMSprop `s ← βs + (1−β)g²; w ← w − αg/(√s + ε)` · **Adam** `m ← β₁m + (1−β₁)g; v ← β₂v + (1−β₂)g²; m̂ = m/(1−β₁ᵗ); v̂ = v/(1−β₂ᵗ); w ← w − α·m̂/(√v̂ + ε)` · AdamW = Adam + decoupled weight decay
- ⌨️ **Build:** implement SGD, momentum, Adam by hand on a toy loss; then compare `torch.optim` on MNIST; LR schedules (step, cosine, warm-up); LR range test.
- 📊 **Measure:** loss curves for each optimizer (same seed).
- 📈 **Improve:** SGD → momentum → Adam → AdamW + cosine schedule.
- 🎤 **Interview:** Why Adam? · Adam vs AdamW? · Why warm-up?
- ✅ **Done when:** you can implement Adam without notes.

### ☐ Day 56 — Regularization in deep learning
- 🧠 **Idea:** deep nets overfit easily. Tools: dropout, weight decay, normalization, early stopping, augmentation.
- ➗ **Equation:** inverted dropout `a ← a·mask/(1−p)` · L2 `L + (λ/2)Σw²` · **BatchNorm** `x̂ = (x−μ_B)/√(σ_B² + ε); y = γx̂ + β` · LayerNorm = same over features
- ⌨️ **Build:** make a net overfit on purpose; add each fix one by one; implement dropout and BatchNorm forward from scratch.
- 📊 **Measure:** train vs validation curves after each fix.
- 📈 **Improve:** overfit → +weight decay → +dropout → +BatchNorm → +early stopping.
- 🎤 **Interview:** Why does dropout work? · BatchNorm vs LayerNorm? · What does early stopping watch?
- ✅ **Done when:** validation gap shrinks to < 2 %.

### ☐ Day 57 — Debugging training & experiment logs
- 🧠 **Idea:** most bugs are silent. Use a checklist.
- ➗ **Equation:** expected initial loss for K classes `≈ ln K` · gradient norm `‖∇‖`
- ⌨️ **Build:** the **debug checklist**: overfit one batch → check initial loss → check shapes → check data labels → gradient clipping `g ← g·min(1, c/‖g‖)` → LR sweep. Log runs to MLflow or a CSV.
- 📊 **Measure:** reproduce 3 classic failures (loss = NaN, loss flat, train ≫ val) and fix each.
- 📈 **Improve:** record the fix for each in `plan120/debug_playbook.md`.
- 🎤 **Interview:** Loss not decreasing — what do you check? · Exploding gradients? · How do you make runs reproducible?
- ✅ **Done when:** your playbook has ≥ 8 symptoms with fixes.

### ☐ Day 58 — TensorFlow / Keras (same model, second framework)
- 🧠 **Idea:** employers often ask for both. Rebuild the same MNIST model in Keras.
- ➗ **Equation:** same maths; `tf.GradientTape` = autograd.
- ⌨️ **Build:** `Sequential` + `Functional` API; `compile / fit / evaluate`; callbacks (EarlyStopping, ModelCheckpoint); a custom loop with `GradientTape`; save `.keras`.
- 📊 **Measure:** accuracy equals the PyTorch version (± 0.5 %).
- 📈 **Improve:** side-by-side code table PyTorch ↔ Keras (write it as a cheat-sheet).
- 🎤 **Interview:** PyTorch vs TensorFlow? · What does `model.fit` do internally? · When use the functional API?
- ✅ **Done when:** you have the cheat-sheet.

### ☐ Day 59 — Tabular deep learning vs boosting ➜ **Phase 4 checkpoint**
- 🧠 **Idea:** on tables, boosted trees often win. Know *why*, and when a neural net still helps (embeddings, multi-modal).
- ➗ **Equation:** categorical embedding `e = E[idx]` (a learned lookup table).
- ⌨️ **Build:** MLP with embeddings for categoricals vs XGBoost on the same table.
- 📊 **Measure:** score, training time, tuning effort.
- 📈 **Improve:** plain MLP → embeddings → tuned → compare to boosting.
- 🎤 **Interview:** answer **20 questions** (Days 48–59). Why do trees beat NNs on tables?
- ✅ **Checkpoint:** **"MLP on HRM / sales data"** + FastAPI + test.

---

# 👁️ PHASE 5 — Computer Vision, short (Days 60–62)

### ☐ Day 60 — Convolution & the CNN
- 🧠 **Idea:** a small filter slides over the image and looks for patterns (edges → shapes → objects). Shares weights → far fewer parameters than a dense net.
- ➗ **Equation:** `(I∗K)(i,j) = Σₘ Σₙ I(i+m, j+n)·K(m,n)` · output size `⌊(n + 2p − f)/s⌋ + 1` · conv params `= (f·f·C_in + 1)·C_out`
- ⌨️ **Build:** `conv2d` from scratch in NumPy; OpenCV load / resize / filters (blur, edges); `nn.Conv2d` + pooling CNN on MNIST.
- 📊 **Measure:** CNN vs dense net: accuracy and number of parameters.
- 📈 **Improve:** dense → small CNN → CNN + BatchNorm.
- 🎤 **Interview:** Why do CNNs beat dense nets on images? · Stride, padding, pooling? · Receptive field?
- ✅ **Done when:** you can compute output shape and parameter count on paper.

### ☐ Day 61 — CIFAR-10, augmentation & transfer learning
- 🧠 **Idea:** more data via augmentation. Better start via a **pretrained** network (ImageNet = a *dataset*; ResNet = the *model*).
- ➗ **Equation:** residual block `y = F(x) + x`
- ⌨️ **Build:** CNN on CIFAR-10 → augmentation (flip, crop, colour) → fine-tune pretrained ResNet (freeze, then unfreeze).
- 📊 **Measure:** accuracy, per-class errors, confusion matrix, 20 worst images.
- 📈 **Improve:** small CNN → +augmentation → pretrained frozen → fine-tuned (log all).
- 🎤 **Interview:** What is transfer learning? · Why do skip connections help? · Freeze vs fine-tune?
- ✅ **Done when:** ≥ 90 % with transfer learning.

### ☐ Day 62 — Detection, segmentation, ViT ➜ **Phase 5 checkpoint**
- 🧠 **Idea:** classify = *what*; detect = *what + where*; segment = *which pixels*. Vision Transformers cut the image into patches.
- ➗ **Equation:** IoU `= |A∩B|/|A∪B|` · mAP · Non-Max Suppression · ViT patch embedding.
- ⌨️ **Build:** run pretrained YOLO on your own photos; compute IoU by hand; read the U-Net diagram; ViT patch-embedding demo.
- 📊 **Measure:** detections vs your own labels; confidence threshold effect.
- 📈 **Improve:** default threshold → tuned threshold + NMS.
- 🎤 **Interview:** answer **20 questions** (Days 60–62). IoU? mAP? YOLO vs Faster R-CNN?
- ✅ **Checkpoint:** **"Document / receipt image classifier"** (ties to HRM) + FastAPI + test.

---

# 📝 PHASE 6 — NLP (Days 63–73)

### ☐ Day 63 — Text preprocessing
- 🧠 **Idea:** clean text before counting. Tokenize, lower-case, remove stop-words, stem or lemmatize, tag parts of speech, find entities.
- ➗ **Equation:** vocabulary size `|V|` · type–token ratio.
- ⌨️ **Build:** regex cleaning; NLTK and spaCy: tokenization, stop-words, Porter stemmer vs lemmatizer, POS tags, NER.
- 📊 **Measure:** vocabulary size and classifier score before/after each cleaning step.
- 📈 **Improve:** raw → lower-case → no stop-words → lemmatized (check each really helps).
- 🎤 **Interview:** Stemming vs lemmatization? · Should you always remove stop-words? · What is NER?
- ✅ **Done when:** a reusable `clean_text()` exists with tests.

### ☐ Day 64 — Bag-of-words, TF-IDF & classic text classification
- 🧠 **Idea:** count words → vectors → classic classifiers. TF-IDF down-weights common words.
- ➗ **Equation:** `tf-idf(t,d) = tf(t,d)·log(N/df(t))` (sklearn uses a smoothed form) · n-grams · cosine similarity
- ⌨️ **Build:** CountVectorizer + TF-IDF from scratch → sklearn; Naive Bayes / SVM / logistic sentiment classifier. Stretch: LDA topic modelling.
- 📊 **Measure:** F1, confusion matrix, top words per class, worst mistakes.
- 📈 **Improve:** BoW → TF-IDF → +bigrams → tuned C.
- 🎤 **Interview:** Why TF-IDF over counts? · What is an n-gram? · Limits of bag-of-words?
- ✅ **Done when:** > 85 % F1 on a review dataset.

### ☐ Day 65 — Word embeddings: Word2Vec, GloVe, FastText
- 🧠 **Idea:** words that appear in similar contexts get similar vectors. "king − man + woman ≈ queen".
- ➗ **Equation:** skip-gram `max Σ log p(w_{t+j}|w_t)`, `p(o|c) = exp(u_o·v_c)/Σ_w exp(u_w·v_c)` · negative sampling · cosine similarity
- ⌨️ **Build:** train a small Word2Vec with `gensim`; nearest neighbours; analogy test; use pretrained GloVe / FastText.
- 📊 **Measure:** similarity tests; where does it fail (one vector per word, no context)?
- 📈 **Improve:** TF-IDF features → averaged Word2Vec → pretrained vectors.
- 🎤 **Interview:** CBOW vs skip-gram? · Why negative sampling? · Static vs contextual embeddings?
- ✅ **Done when:** you can explain why "bank" needs context.

### ☐ Day 66 — Recurrent neural networks
- 🧠 **Idea:** read text one word at a time and keep a **memory** `h`.
- ➗ **Equation:** `hₜ = tanh(Wₓₕxₜ + Wₕₕhₜ₋₁ + b)` · back-prop through time (BPTT) multiplies many `Wₕₕ` → vanishing / exploding gradients
- ⌨️ **Build:** RNN cell in NumPy; `nn.RNN` sentiment model on a small dataset.
- 📊 **Measure:** accuracy vs sentence length (long sentences hurt).
- 📈 **Improve:** unidirectional → bidirectional → gradient clipping.
- 🎤 **Interview:** Why do RNNs forget? · What is BPTT? · Why clip gradients?
- ✅ **Done when:** you can draw the unrolled RNN.

### ☐ Day 67 — LSTM & GRU
- 🧠 **Idea:** gates decide what to **forget**, **write**, **read** — a protected memory cell.
- ➗ **Equation:** `f = σ(W_f[h,x] + b_f)` · `i = σ(W_i[h,x] + b_i)` · `c̃ = tanh(W_c[h,x] + b_c)` · `c = f⊙c₋₁ + i⊙c̃` · `o = σ(W_o[h,x] + b_o)` · `h = o⊙tanh(c)` · GRU: update + reset gates
- ⌨️ **Build:** LSTM cell from scratch; `nn.LSTM`, `nn.GRU` sentiment classifiers; compare RNN / LSTM / GRU.
- 📊 **Measure:** accuracy, parameters, speed.
- 📈 **Improve:** RNN → LSTM → bi-LSTM + pretrained embeddings + dropout.
- 🎤 **Interview:** How does the LSTM fix vanishing gradients? · LSTM vs GRU? · Why bidirectional?
- ✅ **Done when:** you can write the 6 LSTM equations from memory.

### ☐ Day 68 — Sequence-to-sequence & attention
- 🧠 **Idea:** encoder reads, decoder writes. A single summary vector is a bottleneck → let the decoder **look back** at every encoder state (attention).
- ➗ **Equation:** score `eₜₛ = score(hₜ, h̄ₛ)` · weights `αₜₛ = softmax(eₜₛ)` · context `cₜ = Σₛ αₜₛ h̄ₛ`
- ⌨️ **Build:** a tiny seq2seq with attention (e.g. date formats `"3 Jan 2026" → "2026-01-03"`); plot the attention map.
- 📊 **Measure:** exact-match accuracy; BLEU.
- 📈 **Improve:** no attention → attention → bigger hidden size.
- 🎤 **Interview:** Why attention? · Teacher forcing? · What does the attention map show?
- ✅ **Done when:** the attention heat-map looks diagonal for a copy task.

### ☐ Day 69 — Self-attention & the Transformer (from scratch)
- 🧠 **Idea:** every word looks at every other word **at once** (no recurrence). Parallel, fast, powerful.
- ➗ **Equation:** `Attention(Q,K,V) = softmax(QKᵀ/√d_k)·V` · multi-head = several attentions in parallel, then concatenated · positional encoding `PE(pos,2i) = sin(pos/10000^{2i/d})` · block = attention + residual + LayerNorm + feed-forward
- ⌨️ **Build:** a Transformer block in PyTorch (~60 lines); causal mask; shape table for every tensor.
- 📊 **Measure:** why divide by `√d_k`? Show softmax saturation without it.
- 📈 **Improve:** 1 head → 4 heads → 2 layers; check a copy / reverse task.
- 🎤 **Interview:** Explain Q, K, V. · Why positional encoding? · Complexity of attention (O(n²))?
- ✅ **Done when:** you can draw the Transformer from memory.

### ☐ Day 70 — BERT, GPT, T5 & Hugging Face
- 🧠 **Idea:** pretrained models. **Encoder** (BERT, masked-word), **decoder** (GPT, next-word), **encoder–decoder** (T5). BERT is a Transformer, not an RNN.
- ➗ **Equation:** masked LM loss `−Σ_{masked} log p(wᵢ|context)` · causal LM `−Σ log p(wₜ|w<ₜ)` · subword tokenizers (WordPiece, BPE)
- ⌨️ **Build:** `pipeline()` for sentiment, fill-mask, generation; tokenizer inspection; sentence-embedding model + semantic search.
- 📊 **Measure:** zero-shot accuracy on your data.
- 📈 **Improve:** zero-shot → add a classifier on frozen embeddings (preview of fine-tuning).
- 🎤 **Interview:** BERT vs GPT? · Why subword tokens? · What is masked language modelling?
- ✅ **Done when:** you ran 5 different Hugging Face tasks.

### ☐ Day 71 — Fine-tune BERT
- 🧠 **Idea:** start from a pretrained model; train a little on **your** labels.
- ➗ **Equation:** classification head `softmax(W·h_[CLS] + b)` · AdamW with LR ≈ 2e-5 and warm-up
- ⌨️ **Build:** `datasets` + `Trainer`; tokenization with padding / truncation; evaluate F1; **error analysis** on the 30 worst examples.
- 📊 **Measure:** F1 vs the TF-IDF baseline from Day 64.
- 📈 **Improve:** frozen features + logistic → full fine-tune → tuned LR / epochs → DistilBERT (speed).
- 🎤 **Interview:** Fine-tune vs feature extraction? · Catastrophic forgetting? · How to pick LR and epochs?
- ✅ **Done when:** fine-tuned model beats TF-IDF by a clear margin (log it).

### ☐ Day 72 — NER, QA, summarization, translation & NLP metrics
- 🧠 **Idea:** other NLP tasks, each with its own metric.
- ➗ **Equation:** entity-level F1 · QA exact-match / F1 · ROUGE (n-gram overlap) · `BLEU = BP·exp(Σ wₙ log pₙ)` · perplexity `= exp(−(1/N)Σ log p(wᵢ|w<ᵢ))`
- ⌨️ **Build:** NER pipeline; extractive QA; summarization; translation; compute each metric by hand on 3 examples.
- 📊 **Measure:** where metrics disagree with human judgement.
- 📈 **Improve:** off-the-shelf → domain fine-tune idea → post-processing rules.
- 🎤 **Interview:** BLEU vs ROUGE? · What is perplexity? · Token-level vs entity-level F1?
- ✅ **Done when:** you can pick the metric for each task.

### ☐ Day 73 — NLP project ➜ **Phase 6 checkpoint**
- 🧠 **Idea:** put it together on your own domain.
- ➗ **Equation:** none new — report F1 and error slices.
- ⌨️ **Build:** **"HR document / complaint classifier + entity extractor"**; clean → model → API.
- 📊 **Measure:** F1 per class; 20 worst mistakes grouped by cause.
- 📈 **Improve:** TF-IDF → fine-tuned BERT → rules for the top error cause.
- 🎤 **Interview:** answer **20 questions** (Days 63–73). Transformer walk-through at the whiteboard.
- ✅ **Checkpoint:** FastAPI endpoint + test + README.

---

# 🎮 PHASE 7 — Reinforcement Learning, short (Days 74–76)

### ☐ Day 74 — MDP, Bellman equation & Q-learning
- 🧠 **Idea:** an agent acts, gets rewards, and learns a policy. Start with **bandits** (one state), then states.
- ➗ **Equation:** return `Gₜ = Σ γᵏ rₜ₊ₖ₊₁` · Bellman `V(s) = maxₐ Σ P(s′|s,a)[R + γV(s′)]` · **Q-learning** `Q(s,a) ← Q(s,a) + α[r + γ·maxₐ′ Q(s′,a′) − Q(s,a)]` · ε-greedy
- ⌨️ **Build:** multi-armed bandit; Q-learning on FrozenLake / GridWorld from scratch; SARSA for comparison.
- 📊 **Measure:** average reward per episode; success rate.
- 📈 **Improve:** random → greedy → ε-greedy → decaying ε → tuned α, γ.
- 🎤 **Interview:** Explore vs exploit? · On-policy vs off-policy? · What is γ?
- ✅ **Done when:** the agent solves FrozenLake > 70 %.

### ☐ Day 75 — DQN, policy gradient, PPO
- 🧠 **Idea:** use a neural net for Q (DQN) or directly for the policy (policy gradient). PPO = a safe, popular policy-gradient method.
- ➗ **Equation:** DQN loss `(r + γ·max Q_target(s′,·) − Q(s,a))²` + replay buffer + target net · REINFORCE `∇J = E[∇log π(a|s)·G]` · PPO `min(rₜAₜ, clip(rₜ, 1−ε, 1+ε)Aₜ)`
- ⌨️ **Build:** CartPole with a DQN (or Stable-Baselines3 DQN / PPO); read about actor-critic, A3C, DDPG, model-based RL.
- 📊 **Measure:** reward curve; seeds matter (run 3).
- 📈 **Improve:** DQN → +replay + target network → PPO.
- 🎤 **Interview:** Why a replay buffer? · Value-based vs policy-based? · Why clip in PPO?
- ✅ **Done when:** CartPole is solved (≥ 195 average).

### ☐ Day 76 — RL for language models ➜ **Phase 7 checkpoint**
- 🧠 **Idea:** RL turns a text predictor into a helpful assistant. **RLHF**, **DPO**, **GRPO / RLVR** (verifiable rewards).
- ➗ **Equation:** reward model (Bradley–Terry) `P(a ≻ b) = σ(r_a − r_b)` · RLHF objective `max E[r(x,y)] − β·KL(π‖π_ref)`
- ⌨️ **Build:** a tiny **bandit that chooses among 3 prompts** by reward; write a one-page explanation of RLHF → DPO → GRPO.
- 📊 **Measure:** regret of your bandit.
- 📈 **Improve:** uniform → ε-greedy → UCB.
- 🎤 **Interview:** answer **20 questions** (Days 74–76). What does the KL term do? RLHF vs DPO?
- ✅ **Done when:** you can explain how a chat model is trained, end to end.

---

# 🤖 PHASE 8 — Generative AI & LLMs (Days 77–90)

### ☐ Day 77 — How an LLM really works
- 🧠 **Idea:** an LLM predicts the **next token**. Pre-training (read the internet) → SFT (follow instructions) → preference tuning (be helpful and safe). Know: token, context window, KV-cache.
- ➗ **Equation:** `P(w₁…w_T) = Π P(wₜ|w<ₜ)` · loss `−(1/T)Σ log P(wₜ|w<ₜ)` · BPE merges the most frequent pair of symbols, again and again
- ⌨️ **Build:** a mini **BPE tokenizer** from scratch; count tokens of a text with a real tokenizer; estimate cost = tokens × price.
- 📊 **Measure:** tokens per word in English vs another language; context-window budget for a long document.
- 📈 **Improve:** char-level → word-level → BPE: compare vocabulary and sequence length.
- 🎤 **Interview:** What is a token? · Why a context limit? · Pre-training vs fine-tuning vs RLHF?
- ✅ **Done when:** you can explain "next-token prediction" to a non-technical person.

### ☐ Day 78 — Tiny GPT, part 1: attention block
- 🧠 **Idea:** build a decoder-only Transformer on characters (follow Karpathy's *Let's build GPT*).
- ➗ **Equation:** causal mask `scores[i,j] = −∞ for j > i` · `softmax(QKᵀ/√d)V` · block = LayerNorm → attention → residual → LayerNorm → MLP → residual
- ⌨️ **Build:** data loader (context windows), embeddings, one masked attention head, then multi-head; a transformer block.
- 📊 **Measure:** loss at init `≈ ln(vocab)`; overfit one batch (Day-57 check).
- 📈 **Improve:** bigram model → 1 head → multi-head → full block.
- 🎤 **Interview:** Why mask? · Decoder-only vs encoder-decoder? · Why residual connections?
- ✅ **Done when:** loss drops below the bigram baseline.

### ☐ Day 79 — Tiny GPT, part 2: train, sample, decode
- 🧠 **Idea:** stack blocks, train, then **generate** by sampling one token at a time.
- ➗ **Equation:** temperature `softmax(z/T)` · top-k keeps k best · top-p keeps the smallest set with probability ≥ p · perplexity `= exp(loss)`
- ⌨️ **Build:** train on a small text (e.g. your own HR policies); generate with greedy / temperature / top-k / top-p.
- 📊 **Measure:** validation loss / perplexity; quality of samples at T = 0.2, 1.0, 1.5.
- 📈 **Improve:** more layers → longer context → tuned LR + cosine schedule → dropout.
- 🎤 **Interview:** What does temperature do? · Top-k vs top-p? · Why is generation slow (KV-cache)?
- ✅ **Done when:** your model writes text that looks like the training text.

### ☐ Day 80 — LLM APIs: messages, streaming, cost
- 🧠 **Idea:** use a hosted model through an API. Know: system prompt, messages, `max_tokens`, `temperature`, streaming, rate limits, retries.
- ➗ **Equation:** cost `= (in_tokens × price_in) + (out_tokens × price_out)`
- ⌨️ **Build:** Claude API: first call, multi-turn chat, streaming, token counting, retry with back-off, error handling; a tiny CLI chat.
- 📊 **Measure:** latency (first token / total), tokens, cost per call.
- 📈 **Improve:** non-streaming → streaming; long prompt → trimmed prompt (cost drops).
- 🎤 **Interview:** System vs user message? · How do you handle rate limits? · How do you cut cost?
- ✅ **Done when:** a script chats, streams and prints cost.

### ☐ Day 81 — Prompt engineering & structured output
- 🧠 **Idea:** prompts are code. Zero-shot, few-shot, chain-of-thought, clear roles, delimiters, **JSON output validated by a schema**.
- ➗ **Equation:** accuracy on a **test set** of 30 cases `= correct/30` — never judge a prompt by feeling.
- ⌨️ **Build:** extract fields from messy HR text → JSON validated by `pydantic`; retry when invalid.
- 📊 **Measure:** accuracy, invalid-JSON rate, cost for each prompt version.
- 📈 **Improve:** V1 plain → V2 clear instructions → V3 few-shot examples → V4 schema + retry.
- 🎤 **Interview:** Few-shot vs chain-of-thought? · How do you stop prompt injection? · How do you test prompts?
- ✅ **Done when:** V4 is ≥ 95 % on your test set.

### ☐ Day 82 — Embeddings & vector databases
- 🧠 **Idea:** turn text into a vector so **meaning** can be compared. Store vectors in a vector DB; search by nearest neighbour.
- ➗ **Equation:** cosine `a·b/(‖a‖‖b‖)` · ANN indexes: flat (exact), IVF, **HNSW** (graph) · `recall@k`
- ⌨️ **Build:** embed 200 HR sentences; brute-force search → FAISS → Chroma → pgvector; metadata filters.
- 📊 **Measure:** recall@k and latency per index type.
- 📈 **Improve:** keyword search → embedding search → + filters.
- 🎤 **Interview:** Why cosine? · Exact vs approximate search? · How do you pick an embedding model?
- ✅ **Done when:** semantic search finds answers with zero shared keywords.

### ☐ Day 83 — RAG, version 1
- 🧠 **Idea:** the model does not know *your* documents. **Retrieve** the right chunks, put them in the prompt, answer **only** from them.
- ➗ **Equation:** chunk size `c` and overlap `o` · top-k retrieval `argmax_k cos(q, dᵢ)`
- ⌨️ **Build:** load HRM rulebook → chunk → embed → store → retrieve → prompt → answer ("What is the overtime policy?").
- 📊 **Measure:** 20 test questions: right chunk retrieved? right answer?
- 📈 **Improve:** V1 chunk 1000 → V2 chunk 400 + overlap → V3 k tuned.
- 🎤 **Interview:** What is RAG and why not fine-tune? · How do you choose chunk size? · What if the answer is not in the documents?
- ✅ **Done when:** it answers 15 / 20 questions correctly.

### ☐ Day 84 — RAG, version 2: hybrid search, rerank, citations
- 🧠 **Idea:** better retrieval = better answers. Combine keyword (BM25) and vector search, **rerank** with a cross-encoder, rewrite the query, **cite** sources.
- ➗ **Equation:** Reciprocal Rank Fusion `score(d) = Σ 1/(k + rankᵢ(d))` · BM25 (TF-IDF family)
- ⌨️ **Build:** BM25 + vectors + RRF; reranker; query rewriting; answer with `[source: file p.3]`.
- 📊 **Measure:** recall@k and answer accuracy vs V1.
- 📈 **Improve:** vector only → hybrid → + rerank → + query rewrite.
- 🎤 **Interview:** Why hybrid search? · What does a reranker do? · How do you reduce hallucination?
- ✅ **Done when:** every answer has a citation that is correct.

### ☐ Day 85 — RAG evaluation & improvement
- 🧠 **Idea:** you cannot improve what you do not measure. Split failures into **retrieval** vs **generation**.
- ➗ **Equation:** `MRR = (1/Q) Σ 1/rankᵢ` · `recall@k` · faithfulness (answer supported by context?) · answer relevance · LLM-as-judge (check it against human labels)
- ⌨️ **Build:** an eval set of 40 Q&A; automatic metrics; judge prompt; a table of failures by cause.
- 📊 **Measure:** metrics for V1…V4; the biggest failure cause.
- 📈 **Improve:** fix the top cause → re-run → log.
- 🎤 **Interview:** How do you evaluate RAG? · LLM-as-judge risks? · Retrieval failure vs generation failure?
- ✅ **Done when:** a results table shows V1 → V4 gains.

### ☐ Day 86 — Fine-tuning theory: SFT, LoRA, QLoRA
- 🧠 **Idea:** change the model itself. **LoRA** trains two tiny matrices instead of the whole weight. When to use: prompt first → RAG for knowledge → fine-tune for **style / format / skill**.
- ➗ **Equation:** `W′ = W + (α/r)·B·A`, `B ∈ ℝ^{d×r}`, `A ∈ ℝ^{r×k}`, `r ≪ d` · trainable params `= r(d + k)` vs `d·k` · QLoRA = 4-bit base weights
- ⌨️ **Build:** compute the parameter savings for r = 8; format an SFT dataset (instruction → answer); a preference pair for DPO.
- 📊 **Measure:** memory / parameter count with and without LoRA.
- 📈 **Improve:** decision table "prompt vs RAG vs fine-tune" for 6 real tasks.
- 🎤 **Interview:** Why does LoRA work? · RAG vs fine-tuning? · What is QLoRA?
- ✅ **Done when:** you can justify the choice for 6 tasks.

### ☐ Day 87 — LoRA fine-tuning project
- 🧠 **Idea:** do it for real on a small open model (≤ 1–3 B) on a free GPU.
- ➗ **Equation:** same as Day 86; watch training loss and eval loss.
- ⌨️ **Build:** `transformers` + `peft` + `trl`; train on 500–2 000 examples; merge or load the adapter; push to the Hugging Face Hub.
- 📊 **Measure:** base vs prompted vs fine-tuned on a held-out set.
- 📈 **Improve:** r = 4 → 8 → 16; LR; epochs; data quality (clean 100 bad examples).
- 🎤 **Interview:** What can go wrong (overfit, forgetting, bad data)? · How do you evaluate a fine-tune? · Adapter vs merged weights?
- ✅ **Done when:** model card on the Hub + a results table.

### ☐ Day 88 — Image generation, multimodal & speech
- 🧠 **Idea:** **VAE** compresses, **GAN** plays a forger-vs-detective game, **diffusion** learns to remove noise (today's best). Vision-language models read images; Whisper hears; TTS speaks.
- ➗ **Equation:** VAE `ELBO = E[log p(x|z)] − KL(q(z|x)‖p(z))` · GAN `min_G max_D E[log D(x)] + E[log(1 − D(G(z)))]` · diffusion `x_t = √ᾱ_t·x₀ + √(1−ᾱ_t)·ε`, the net predicts `ε`
- ⌨️ **Build:** a tiny VAE on MNIST; `diffusers` text-to-image; a vision-language question on a photo; Whisper transcription; a voice round-trip.
- 📊 **Measure:** sample quality (look), speed, cost; word-error-rate for speech.
- 📈 **Improve:** default → prompt / guidance scale / steps → negative prompts.
- 🎤 **Interview:** GAN vs VAE vs diffusion? · Why is diffusion stable to train? · How does CLIP link text and images?
- ✅ **Done when:** you generated an image and transcribed an audio file.

### ☐ Day 89 — LLM safety, evaluation, cost & latency
- 🧠 **Idea:** production LLM apps fail in new ways: hallucination, prompt injection, data leaks, cost spikes.
- ➗ **Equation:** p50 / p95 latency · cache hit rate `= hits/requests` · cost per 1 000 requests
- ⌨️ **Build:** an **eval harness** (cases + metrics + report); guardrails (input / output checks, PII masking); response cache; batching; streaming.
- 📊 **Measure:** before / after: latency, cost, error rate.
- 📈 **Improve:** no guard → guard → guard + cache.
- 🎤 **Interview:** What is prompt injection and how do you defend? · How do you detect hallucination? · How do you cut latency and cost?
- ✅ **Done when:** you have a red-team list of 10 attacks and the results.

### ☐ Day 90 — GenAI project ➜ **Phase 8 checkpoint**
- 🧠 **Idea:** put it all together.
- ➗ **Equation:** none new — report the metrics from Day 85.
- ⌨️ **Build:** **"HR policy assistant"**: RAG with citations, streaming FastAPI endpoint, eval set, cost report.
- 📊 **Measure:** accuracy, citation accuracy, p95 latency, cost / question.
- 📈 **Improve:** one full V1 → V4 ladder, written up.
- 🎤 **Interview:** answer **20 questions** (Days 77–90). Design a RAG system on a whiteboard.
- ✅ **Checkpoint:** README + test + demo GIF.

---

# 🕹️ PHASE 9 — Agentic AI (Days 91–99)

### ☐ Day 91 — Tool calling & the agent loop (no framework)
- 🧠 **Idea:** an agent = an LLM in a **loop**: think → call a tool → read the result → repeat until done.
- ➗ **Equation:** success rate `= tasks solved/total` · expected cost `= steps × cost per step` · `max_steps` guards against infinite loops
- ⌨️ **Build:** define 3 tools with JSON schemas (calculator, search, DB lookup); write the loop by hand with the Claude API; handle tool errors.
- 📊 **Measure:** steps, tokens and success on 10 tasks.
- 📈 **Improve:** one-shot answer → tool loop → better tool descriptions → better error messages.
- 🎤 **Interview:** How does tool calling work? · Agent vs workflow? · How do you stop loops?
- ✅ **Done when:** your loop solves a 3-step task without a framework.

### ☐ Day 92 — ReAct, planning & task decomposition
- 🧠 **Idea:** reason → act → observe. Plan first for long tasks. Reflect and retry on failure.
- ➗ **Equation:** none — measure plan quality: steps wasted, success rate.
- ⌨️ **Build:** ReAct prompt; plan-and-execute; a self-check step ("is the answer supported by the tool output?").
- 📊 **Measure:** success vs the plain loop on 15 multi-step tasks.
- 📈 **Improve:** loop → ReAct → plan-and-execute → + reflection.
- 🎤 **Interview:** What is ReAct? · When is a single call better than an agent? · How does reflection help?
- ✅ **Done when:** measured gain from planning (or an honest "no gain").

### ☐ Day 93 — Memory & context engineering
- 🧠 **Idea:** the context window is a budget. Decide what goes in: recent messages, summaries, retrieved facts, tool results.
- ➗ **Equation:** token budget `system + history + retrieved + tools + answer ≤ window`
- ⌨️ **Build:** short-term memory (message trimming), summarization, long-term memory in a vector store; context compaction.
- 📊 **Measure:** answer quality vs context size; cost.
- 📈 **Improve:** full history → trimmed → summarized → retrieved memory.
- 🎤 **Interview:** Short- vs long-term memory? · What is context compaction? · Why does more context sometimes hurt?
- ✅ **Done when:** the agent remembers a fact from 50 turns ago using < 20 % of the tokens.

### ☐ Day 94 — LangChain & LangGraph
- 🧠 **Idea:** frameworks give structure: chains, tools, retrievers; **LangGraph** = a state machine (nodes, edges, conditions, checkpoints, human-in-the-loop).
- ➗ **Equation:** none — graph `G = (nodes, edges)`, state is passed along.
- ⌨️ **Build:** rebuild the Day-91 agent in LangGraph; add a conditional edge, a retry node, a human-approval step.
- 📊 **Measure:** lines of code, success, debuggability vs the hand-written loop.
- 📈 **Improve:** write when to use a framework and when not to.
- 🎤 **Interview:** LangChain vs LangGraph? · Why a graph for agents? · What is a checkpoint?
- ✅ **Done when:** the same agent works in both styles.

### ☐ Day 95 — MCP: Model Context Protocol
- 🧠 **Idea:** a standard way to give models **tools and data**. A server exposes tools / resources; any compatible client can use them.
- ➗ **Equation:** none — client ↔ server messages (JSON-RPC).
- ⌨️ **Build:** an MCP server with **read-only HRM tools** (search payslips, get policy); connect a client; test the tool schemas.
- 📊 **Measure:** does the model pick the right tool? tool-call accuracy on 20 prompts.
- 📈 **Improve:** vague tool names → clear names + descriptions + examples.
- 🎤 **Interview:** What is MCP and why? · MCP tool vs function calling? · Security risks of tools?
- ✅ **Done when:** a client lists and calls your server's tools.

### ☐ Day 96 — Multi-agent systems
- 🧠 **Idea:** several agents with roles (researcher, writer, reviewer) or a manager with workers. More agents = more cost; use only when it helps.
- ➗ **Equation:** total cost `= Σ over agents (tokens × price)`
- ⌨️ **Build:** manager + 2 workers (CrewAI / AutoGen-style patterns, or plain code); shared state; hand-offs.
- 📊 **Measure:** quality, cost and time vs one agent.
- 📈 **Improve:** single agent → manager + workers → add a reviewer.
- 🎤 **Interview:** When is multi-agent worth it? · How do agents hand off? · Failure modes?
- ✅ **Done when:** a table compares single vs multi-agent on cost and quality.

### ☐ Day 97 — Agent evaluation, guardrails & safety
- 🧠 **Idea:** agents act in the real world, so **permissions and tests** come first. Read-only by default; confirm before writes; treat tool output as untrusted (injection).
- ➗ **Equation:** task success rate · tool-call accuracy · steps per task · cost per task · p95 latency
- ⌨️ **Build:** a test set of 30 tasks with expected outcomes; trajectory logs; allow-list of tools; read-only DB user; human approval for risky actions; Langfuse (or similar) tracing.
- 📊 **Measure:** success rate and failure categories.
- 📈 **Improve:** fix the top 3 failure causes; re-run.
- 🎤 **Interview:** How do you evaluate an agent? · Prompt injection through tool output? · How do you limit blast radius?
- ✅ **Done when:** a repeatable eval run produces a report.

### ☐ Day 98 — Build: the HRM payslip agent
- 🧠 **Idea:** an agent that answers questions about payslips using **tools**: read-only text-to-SQL, the anomaly model (Day 42), the policy RAG (Day 90). Re-use the existing tool-calling agent in `hrm_app/`.
- ➗ **Equation:** none new — use the Day-97 metrics.
- ⌨️ **Build:** wire the 3 tools; SQL safety (read-only user, `SELECT` only, row limit); structured answers with citations.
- 📊 **Measure:** 30-question test set: correctness, safe-SQL rate, steps, cost.
- 📈 **Improve:** V1 → V4 (better schema description, few-shot SQL, retry on SQL error, guardrails).
- 🎤 **Interview:** Text-to-SQL risks? · How do you give the model the DB schema? · How do you make it deterministic enough?
- ✅ **Done when:** ≥ 85 % correct, 0 unsafe queries.

### ☐ Day 99 — Agent project ➜ **Phase 9 checkpoint**
- 🧠 **Idea:** one more agent end to end: a **research / support agent** with memory, tools, tracing and an eval report.
- ➗ **Equation:** none new.
- ⌨️ **Build:** the agent + traces + eval + README.
- 📊 **Measure:** the Day-97 metrics.
- 📈 **Improve:** one ladder written up.
- 🎤 **Interview:** answer **20 questions** (Days 91–99). Design an agent platform on a whiteboard.
- ✅ **Checkpoint:** demo recording + eval report.

---

# 🛠️ PHASE 10 — Software Engineering with AI/ML (Days 100–111)

> You already have SQL (5 years) and FastAPI experience. These days focus on what is **different for AI services**: model loading, latency, validation, drift, cost, tests for non-deterministic code.

### ☐ Day 100 — Serve a model with FastAPI
- 🧠 **Idea:** a model is useful only when other software can call it. Load the model **once at start-up**, validate every input, return clear errors.
- ➗ **Equation:** latency `p50 / p95` · throughput `= requests/second` · `workers × (1/latency)` ≈ capacity
- ⌨️ **Build:** `pydantic` request/response models; `lifespan` loads `joblib` / PyTorch model; `/health`, `/predict`, `/predict_batch`; async vs sync; OpenAPI docs; load test with `locust` or `hey`.
- 📊 **Measure:** p50 / p95 latency, error rate, memory.
- 📈 **Improve:** load model per request → once → batch endpoint → quantized / ONNX model (awareness: TorchServe, TF Serving).
- 🎤 **Interview:** Why load the model at start-up? · How do you handle bad input? · Sync vs async for ML endpoints?
- ✅ **Done when:** p95 latency is measured and written in the README.

### ☐ Day 101 — API security: auth, rate limits, secrets
- 🧠 **Idea:** an AI endpoint costs money and can leak data. Protect it.
- ➗ **Equation:** JWT = `header.payload.signature` · token bucket `tokens += rate·Δt (max burst)`
- ⌨️ **Build:** password hashing, JWT login, API keys, role checks, rate limiting (Redis / `slowapi`), CORS, `.env` secrets, request-size limits.
- 📊 **Measure:** attack tests: no token, expired token, 1 000 req/min, oversized body.
- 📈 **Improve:** open → API key → JWT + roles + rate limit.
- 🎤 **Interview:** JWT vs session? · How do you rate-limit? · Where do secrets live?
- ✅ **Done when:** all 4 attack tests are blocked.

### ☐ Day 102 — Databases inside AI apps (PostgreSQL, pgvector)
- 🧠 **Idea:** you know SQL — focus on **app integration**: ORM, async, migrations, vector columns, indexes.
- ➗ **Equation:** HNSW index = approximate nearest neighbours (recall ↔ speed trade-off)
- ⌨️ **Build:** SQLAlchemy async + Alembic; a `documents` table with a `vector` column (pgvector); store predictions + feedback; (optional MongoDB for logs).
- 📊 **Measure:** query time with and without an index; N+1 query check.
- 📈 **Improve:** sequential scan → HNSW index → connection pool tuned.
- 🎤 **Interview:** pgvector vs a vector DB? · How do you store predictions for audit? · Migrations in production?
- ✅ **Done when:** RAG runs on pgvector with an index.

### ☐ Day 103 — Docker & docker-compose
- 🧠 **Idea:** package code + dependencies so "it works on my machine" is the same everywhere.
- ➗ **Equation:** image size `= Σ layers` — smaller is faster to deploy.
- ⌨️ **Build:** `Dockerfile` (multi-stage, slim, non-root user, cached layers); `docker-compose` with api + postgres + redis; health-checks; `.dockerignore`.
- 📊 **Measure:** image size, build time, start-up time.
- 📈 **Improve:** fat image → slim base → multi-stage → layer caching.
- 🎤 **Interview:** Image vs container? · Why multi-stage? · How do containers talk to each other?
- ✅ **Done when:** `docker compose up` starts the whole service.

### ☐ Day 104 — Git workflow & CI/CD
- 🧠 **Idea:** every change goes through branch → pull request → review → automatic checks → merge.
- ➗ **Equation:** none — pipeline = lint → test → build → (deploy).
- ⌨️ **Build:** feature branch + PR; small commits (`feat:`, `fix:`); GitHub Actions: `ruff` + `pytest` + Docker build; a PR template; branch protection.
- 📊 **Measure:** pipeline time; a failing test blocks the merge (prove it).
- 📈 **Improve:** manual checks → CI → cached CI.
- 🎤 **Interview:** Merge vs rebase? · What does CI do? · How do you review a PR?
- ✅ **Done when:** a red test blocks a PR in your own repo.

### ☐ Day 105 — Testing ML & LLM code
- 🧠 **Idea:** ML code is hard to test because outputs are fuzzy. Test the **parts**: data checks, pure functions, API contracts, and **score thresholds**.
- ➗ **Equation:** model regression test `score ≥ baseline − tolerance`
- ⌨️ **Build:** `pytest` fixtures; unit tests for preprocessing; data validation (`pandera`); API tests with `TestClient`; mock the LLM; golden-set test for prompts.
- 📊 **Measure:** coverage; flaky-test count.
- 📈 **Improve:** no tests → unit tests → data tests → model-score gate in CI.
- 🎤 **Interview:** How do you test a model? · How do you test non-deterministic LLM output? · What is a golden set?
- ✅ **Done when:** CI fails if the model score drops.

### ☐ Day 106 — Async work: Redis, Celery, caching
- 🧠 **Idea:** slow jobs (training, big LLM batches) must not block the API. Use a queue + workers. Cache repeated answers.
- ➗ **Equation:** cache hit rate `= hits/requests` · retry with exponential back-off `delay = base·2ⁿ`
- ⌨️ **Build:** Celery worker + Redis broker; job status endpoint; cache LLM / prediction results; idempotent retries.
- 📊 **Measure:** latency before/after cache; queue depth.
- 📈 **Improve:** inline → background job → + cache → + retries.
- 🎤 **Interview:** When use a queue? · Idempotency? · Cache invalidation?
- ✅ **Done when:** a long job runs in the background and reports progress.

### ☐ Day 107 — MLflow, DVC & reproducibility
- 🧠 **Idea:** you must reproduce any result: code + data + params + environment.
- ➗ **Equation:** none — run = (git commit, data hash, params, metrics, artifacts).
- ⌨️ **Build:** MLflow tracking + model registry; DVC for data; fixed seeds; pinned `requirements.txt`; a model card.
- 📊 **Measure:** re-run an old experiment and get the same number.
- 📈 **Improve:** notebook only → script + MLflow → + DVC + registry.
- 🎤 **Interview:** What do you log for every run? · Model registry stages? · Data versioning?
- ✅ **Done when:** you reproduce a result from 2 weeks ago.

### ☐ Day 108 — Monitoring, drift & LLM tracing
- 🧠 **Idea:** a model decays when the world changes. Watch inputs, outputs, errors, cost.
- ➗ **Equation:** PSI `= Σ (aᵢ − eᵢ)·ln(aᵢ/eᵢ)` (< 0.1 ok, > 0.25 big shift) · KS test for drift
- ⌨️ **Build:** structured logging; Prometheus-style metrics (latency, errors); drift report with Evidently; alert rule; Langfuse traces for LLM calls.
- 📊 **Measure:** simulate drift (shift a feature) and detect it.
- 📈 **Improve:** no monitoring → logs → metrics → drift alert → retraining trigger.
- 🎤 **Interview:** Data drift vs concept drift? · What do you monitor for an LLM app? · When retrain?
- ✅ **Done when:** a drift alert fires on your simulated shift.

### ☐ Day 109 — PySpark, part 1
- 🧠 **Idea:** data too big for one machine. Spark splits it into **partitions** and runs on many cores. Lazy: nothing runs until an **action**.
- ➗ **Equation:** speed-up ≈ `1/((1−p) + p/N)` (Amdahl's law)
- ⌨️ **Build:** local Spark; DataFrame API; transformations vs actions; `groupBy`, `join`, window functions; read / write **Parquet**.
- 📊 **Measure:** pandas vs Spark time on a 1–5 GB file.
- 📈 **Improve:** CSV → Parquet → partition by a key → cache.
- 🎤 **Interview:** Transformation vs action? · What is a shuffle? · When NOT to use Spark?
- ✅ **Done when:** you processed a file larger than your RAM.

### ☐ Day 110 — PySpark, part 2
- 🧠 **Idea:** ETL + features + models at scale. Know Spark MLlib and Dask as options.
- ➗ **Equation:** none new.
- ⌨️ **Build:** ETL pipeline: read → clean → features → write; a Spark MLlib `Pipeline` (or pandas-on-Spark); compare with your sklearn pipeline.
- 📊 **Measure:** score + time vs sklearn on the same data.
- 📈 **Improve:** skewed partitions → repartition / salting; fewer shuffles.
- 🎤 **Interview:** What is data skew? · Batch vs streaming? · Spark vs Dask?
- ✅ **Done when:** one reproducible Spark job with a README.

### ☐ Day 111 — Cloud deploy ➜ **Phase 10 checkpoint**
- 🧠 **Idea:** put the service on the internet. Options: Render / Railway / Hugging Face Spaces (easy), AWS (ECR + ECS / Lambda), plus awareness of Kubernetes (pod, deployment, service) and managed ML (SageMaker, Vertex AI, Azure ML).
- ➗ **Equation:** monthly cost `≈ (instance price × hours) + (egress) + (LLM tokens)`
- ⌨️ **Build:** deploy your **FastAPI + Docker** service publicly with secrets set in the platform; health-check; logs; rollback.
- 📊 **Measure:** cold-start, p95, cost per day.
- 📈 **Improve:** manual deploy → CI deploy on merge.
- 🎤 **Interview:** answer **20 questions** (Days 100–111). Blue-green vs canary?
- ✅ **Checkpoint:** a **live URL** for your HR policy assistant.

---

# 🏆 PHASE 11 — System Design, Interviews & Capstone (Days 112–120)

### ☐ Day 112 — ML system design, part 1
- 🧠 **Idea:** a repeatable framework: **requirements & metric → data → features → model → training → serving (batch / online) → monitoring → iteration**.
- ➗ **Equation:** back-of-envelope: `QPS = users × requests/day / 86 400` · storage `= rows × bytes` · cost.
- ⌨️ **Build:** design on paper: spam filter, fraud detection, recommender. Draw the boxes and data flow.
- 📊 **Measure:** self-score each design with a checklist (metric? baseline? failure modes? monitoring?).
- 📈 **Improve:** V1 sketch → V2 with numbers → V3 with trade-offs.
- 🎤 **Interview:** "Design a fraud detection system." (record yourself, 30 min)
- ✅ **Done when:** you can walk through the framework without notes.

### ☐ Day 113 — ML / LLM system design, part 2 + the design doc
- 🧠 **Idea:** LLM systems: RAG at scale, agent platform, search ranking. Trade-offs: quality ↔ latency ↔ cost ↔ safety.
- ➗ **Equation:** cost per request `= tokens_in·p_in + tokens_out·p_out + retrieval cost` · caching / batching savings.
- ⌨️ **Build:** a 2-page **design doc** (context, goals, non-goals, design, alternatives, risks, metrics, rollout).
- 📊 **Measure:** have a peer (or an LLM) review the doc against a checklist.
- 📈 **Improve:** V1 → reviewed V2.
- 🎤 **Interview:** "Design an enterprise HR assistant used by 5 000 employees."
- ✅ **Done when:** you have a design-doc template you reuse.

### ☐ Day 114 — Capstone design: **Intelligent HRM Assistant**
- 🧠 **Idea:** one product: upload payslips → **anomaly model** flags rows → **RAG** explains which policy was broken (with citations) → **agent** answers questions with tools → **API + UI** → deployed.
- ➗ **Equation:** define success metrics now: anomaly precision@k, RAG citation accuracy, agent task success, p95 latency, cost / query.
- ⌨️ **Build:** architecture diagram, data flow, API contract (OpenAPI), eval plan, risk list (privacy, wrong flags, injection), milestones.
- 📊 **Measure:** review against the Day-113 doc checklist.
- 📈 **Improve:** cut scope to what fits in 3 build days.
- 🎤 **Interview:** present the design in 5 minutes.
- ✅ **Done when:** the design doc is committed.

### ☐ Day 115 — Capstone build 1: model + RAG
- 🧠 **Idea:** the intelligence layer.
- ➗ **Equation:** use your Day-114 metrics.
- ⌨️ **Build:** wrap the anomaly model (Day 42, `hrm_detective/`) as a service; reuse the Day-90 RAG for policy explanations.
- 📊 **Measure:** anomaly precision@k; citation accuracy.
- 📈 **Improve:** V1 → V3 on the worst error slice.
- 🎤 **Interview:** explain one trade-off you made.
- ✅ **Done when:** both services pass their tests.

### ☐ Day 116 — Capstone build 2: agent + API + UI
- 🧠 **Idea:** the product layer.
- ➗ **Equation:** use your Day-114 metrics.
- ⌨️ **Build:** the Day-98 agent behind a FastAPI app (`hrm_app/`), JWT auth, rate limiting, a simple front-end (upload data, see flags, chat).
- 📊 **Measure:** agent task success; p95 latency.
- 📈 **Improve:** V1 → V3.
- 🎤 **Interview:** how do you keep the agent safe?
- ✅ **Done when:** an end-to-end demo works locally.

### ☐ Day 117 — Capstone build 3: ship it
- 🧠 **Idea:** production readiness.
- ➗ **Equation:** use your Day-114 metrics + cost per query.
- ⌨️ **Build:** Docker + compose, CI (lint + tests + eval gate), monitoring + drift alert, deploy to a public URL.
- 📊 **Measure:** smoke test on the live URL; cost per day.
- 📈 **Improve:** fix what the smoke test finds.
- 🎤 **Interview:** how would you roll this out in a company?
- ✅ **Done when:** the live URL works.

### ☐ Day 118 — Polish & document
- 🧠 **Idea:** a project is only as good as its README.
- ➗ **Equation:** none.
- ⌨️ **Build:** README (problem, architecture diagram, how to run, results table V1 → V4, limits), model card, 3-minute demo video, screenshots.
- 📊 **Measure:** ask someone to run it from the README alone.
- 📈 **Improve:** fix every place they got stuck.
- 🎤 **Interview:** give the 2-minute project pitch (record it).
- ✅ **Done when:** a stranger can run your project.

### ☐ Day 119 — Full mock interview
- 🧠 **Idea:** rehearse the real thing.
- ➗ **Equation:** derive on a whiteboard (no notes): linear regression normal equation · logistic gradient · softmax + CE gradient · backprop for 2 layers · attention · Adam · PCA · Bayes.
- ⌨️ **Build:** code from memory: K-means, logistic regression with GD, a simple decision split, cosine search.
- 📊 **Measure:** 50 ML-theory questions (random from your 20-question sets) + 1 system design; self-score and list weak spots.
- 📈 **Improve:** re-study the 5 weakest topics for 90 minutes each, then re-test.
- 🎤 **Interview:** a full 60-minute mock (record it).
- ✅ **Done when:** ≥ 80 % on the theory set.

### ☐ Day 120 — Portfolio & **gap audit**
- 🧠 **Idea:** make your work visible and check nothing is missing.
- ➗ **Equation:** none.
- ⌨️ **Build:** pin 4–6 GitHub repos; CV + LinkedIn headline; fill the **gap-audit table** below (tick every row); write a 30-day follow-up list (Kaggle, open source, papers, one deeper area).
- 📊 **Measure:** every roadmap topic has a ✅ or a written reason.
- 📈 **Improve:** schedule the 30-day list.
- 🎤 **Interview:** tell the story: "what I built, what failed, what I improved, what I learned".
- ✅ **Done when:** gap-audit is fully ticked. **You finished.** 🎓

---

# ✅ Gap audit (topic from the roadmaps → day that covers it)

| Roadmap topic | Day(s) | ☐ |
|---|---|---|
| Python, OOP, errors (you know it — used daily) | all | ☐ |
| NumPy · Pandas · Matplotlib/Seaborn · Polars (awareness) | 1, 4, 10, 17 | ☐ |
| Linear algebra · calculus · probability · statistics · hypothesis tests | 2–9 | ☐ |
| Optimization: gradient descent, variants, convex vs non-convex | 7, 19, 55 | ☐ |
| EDA · cleaning · encoding · scaling · feature engineering · selection · imbalance | 10–16 | ☐ |
| Linear / polynomial / Ridge / Lasso / ElasticNet · statsmodels | 17–23 | ☐ |
| Logistic · KNN · Naive Bayes · SVM · metrics · calibration | 24–31 | ☐ |
| Decision tree · Random Forest · AdaBoost · GBM · XGBoost · LightGBM · CatBoost · stacking | 32–38 | ☐ |
| K-means · hierarchical · DBSCAN · GMM · PCA · t-SNE/UMAP · anomaly detection | 39–42 | ☐ |
| Cross-validation · tuning (grid / random / Bayesian / genetic idea) · SHAP/LIME | 43–45 | ☐ |
| Time series · recommenders · A/B tests · causal basics | 46–47 | ☐ |
| Neural networks · backprop · activations · losses · optimizers · regularization | 48–57 | ☐ |
| PyTorch · TensorFlow/Keras | 53–54, 58 | ☐ |
| CNN · transfer learning · YOLO / Faster R-CNN · U-Net · ViT · OpenCV | 60–62 | ☐ |
| Tokenization · stemming · lemmatization · POS · NER · BoW · TF-IDF · topic modelling | 63–64 | ☐ |
| Word2Vec · GloVe · FastText | 65 | ☐ |
| RNN · LSTM · GRU · Seq2Seq · attention | 66–68 | ☐ |
| Transformers · BERT · GPT · T5 · Hugging Face · fine-tuning · NLP metrics | 69–73 | ☐ |
| Reinforcement learning: MDP · Q-learning · SARSA · DQN · PPO · actor-critic · RLHF/DPO | 74–76 | ☐ |
| LLM fundamentals · tokens · context · tiny GPT · decoding | 77–79 | ☐ |
| LLM APIs · prompt engineering · structured output | 80–81 | ☐ |
| Embeddings · vector DBs (FAISS, Chroma, pgvector) · RAG · RAG evaluation | 82–85 | ☐ |
| Fine-tuning: SFT · LoRA · QLoRA · PEFT | 86–87 | ☐ |
| VAE · GAN · diffusion · multimodal · speech | 88 | ☐ |
| LLM safety · evals · cost / latency | 89–90 | ☐ |
| Agents: tool calling · ReAct · planning · memory · LangChain · LangGraph · MCP · multi-agent (CrewAI/AutoGen ideas) · agent evals · guardrails | 91–99 | ☐ |
| FastAPI model serving · REST · validation · latency | 100 | ☐ |
| Auth (JWT) · rate limiting · CORS · secrets | 101 | ☐ |
| PostgreSQL · pgvector · ORM · MongoDB (optional) | 102 | ☐ |
| Docker · docker-compose | 103 | ☐ |
| Git / GitHub · CI/CD (GitHub Actions) | 104 | ☐ |
| Testing ML / LLM code | 105 | ☐ |
| Redis · Celery · caching · async | 106 | ☐ |
| MLflow · DVC · model registry · reproducibility | 107 | ☐ |
| Monitoring · drift · LLM tracing | 108 | ☐ |
| Spark / PySpark · Dask · Parquet · ETL | 109–110 | ☐ |
| Cloud (Render / Railway / HF Spaces / AWS) · Kubernetes awareness · SageMaker / Vertex AI awareness | 111 | ☐ |
| ML system design · design docs · interviews · portfolio | 112–120 | ☐ |

**Skipped on purpose (with reasons):** Django/DRF (we use FastAPI; same ideas) · Java / C++ (optional in the roadmaps) · Hadoop & Kubeflow (awareness only — Spark and Kubernetes cover the ideas) · basic SQL (you have 5 years) · JAX (awareness only).

---

# 📋 Templates

### Results log (`plan120/results_log.md`)
| Day | Task | Version | Change made | Metric | Score | Note |
|---|---|---|---|---|---|---|
| 1 | diabetes regression | V1 | mean baseline | RMSE | … | score to beat |
| 23 | diabetes regression | V4 | poly + ElasticNet (tuned) | RMSE | … | best |

### Interview tracker
| Phase | 20 questions done | Mock done | Weak topics to redo |
|---|---|---|---|
| 1 Foundations | ☐ | — | |
| 2 Data & features | ☐ | — | |
| 3 Classical ML | ☐ (per sub-block) | ☐ (D47, 50 Qs) | |
| 4 Deep learning | ☐ | — | |
| 5 CV | ☐ | — | |
| 6 NLP | ☐ | — | |
| 7 RL | ☐ | — | |
| 8 GenAI | ☐ | — | |
| 9 Agents | ☐ | — | |
| 10 Software engineering | ☐ | — | |
| 11 Final | — | ☐ (D119, 60 min) | |

### Progress tracker
- ☐ Phase 1 (D1–9) · ☐ Phase 2 (D10–16) · ☐ Phase 3 (D17–47) · ☐ Phase 4 (D48–59) · ☐ Phase 5 (D60–62) · ☐ Phase 6 (D63–73)
- ☐ Phase 7 (D74–76) · ☐ Phase 8 (D77–90) · ☐ Phase 9 (D91–99) · ☐ Phase 10 (D100–111) · ☐ Phase 11 (D112–120)

---

# 🏢 Company habits (build these from Day 1)

1. **Write a one-line goal and a metric** before you code.
2. **Baseline first.** Always.
3. **Small commits, clear messages, pull requests, code review.**
4. **Tests + CI** for anything that will be re-run.
5. **Log experiments** (params, data version, metrics) so a teammate can repeat them.
6. **Explain results to non-technical people:** one sentence, one chart, one risk, one next step.
7. **Monitor in production** and plan for rollback.
8. **Safety by default:** least privilege, read-only data access, no secrets in code, privacy-aware logs.
9. **Write a design doc** before big work; keep a decision log.
10. **Say "I don't know — here is how I would find out."** (Good interview answer, good engineer habit.)

---

# 📚 Resources

- **Roadmaps (source of this plan):** <https://github.com/rashakil-ds/Roadmap-Docs> — AI Engineer · Generative AI Engineer · AI Agent Developer · NLP Engineer · Machine Learning Engineer · Software Engineering with ML-AI
- **Your class notes:** [course_notes/](course_notes/)
- **Docs:** [scikit-learn](https://scikit-learn.org/stable/) · [PyTorch tutorials](https://pytorch.org/tutorials/beginner/basics/intro.html) · [TensorFlow tutorials](https://www.tensorflow.org/tutorials) · [Hugging Face learn](https://huggingface.co/learn) · [LangChain](https://python.langchain.com/docs/introduction/) · [FastAPI](https://fastapi.tiangolo.com/) · [Spinning Up (RL)](https://spinningup.openai.com/)
- **Channels:** Andrej Karpathy · Sebastian Raschka · StatQuest · 3Blue1Brown · Study Mart
- **Old plans (archived):** [old_plans/](old_plans/)
