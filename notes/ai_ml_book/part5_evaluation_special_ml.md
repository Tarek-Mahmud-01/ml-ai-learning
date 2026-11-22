# PART V — Evaluate, Tune & Special ML

[📖 Table of contents](README.md) · [← previous part](part4_unsupervised.md) · [next part →](part6_deep_learning_vision.md) · [Appendices](appendix.md)

> **Days 40–47 · Category: model evaluation, tuning, explanation, and specialised problems · Levels: 1 → 3 in every chapter**
> **You will be able to:** evaluate honestly, tune with a budget, explain a model and find where it fails, forecast time series, build a recommender, run an A/B test, and pass a 50-question classical-ML mock interview.
> **Math you meet here (just-in-time):** Shapley values (Day 42) · autocorrelation and stationarity (43) · matrix factorization (45) · power and sample size (46).
> **Your class notes used:** *Grid Search and Random Search, Data Leakage, Train/Test evaluation*.

---

## Chapter 21 — Cross-validation and honest evaluation

> ⚠️ **Common mistakes:** shuffling time series · tuning and evaluating on the same folds (use nested CV) · leakage through preprocessing outside the pipeline.

### Levels 1 → 3 (inside the day)
<a id="day-40"></a>
#### ☐ Day 40 — Cross-validation & honest evaluation
- 🧠 **Idea · L1:** one split can be lucky. Use K folds. Use the *right* split for the data.
- ➗ **Equation · L1:** `CV = (1/K)Σ scoreₖ` and `±` standard deviation · nested CV = outer loop (evaluate) + inner loop (tune)
- ⌨️ **Build · L2:** K-Fold, Stratified, Group, **TimeSeriesSplit**, LOOCV, repeated CV; nested CV.
- 📊 **Measure · L2:** spread of scores; show that tuning on the test set inflates the score.
- 📈 **Improve · L3:** single split → K-fold → repeated → nested.
- 🎤 **Interview · L3:** Why stratified? · Why not shuffle time series? · What is nested CV for?
- ✅ **Done when:** you can pick the CV scheme for any dataset.


## Chapter 22 — Hyper-parameter tuning

> **You will learn:** grid, random, Bayesian (Optuna), successive halving and **genetic algorithms**.
> ⚠️ **Common mistakes:** grid search on 8 parameters · unequal budgets when comparing methods · overfitting the validation set.

### Levels 1 → 3 (inside the day)
<a id="day-41"></a>
#### ☐ Day 41 — Hyper-parameter tuning
- 🧠 **Idea · L1:** settings that are not learned (depth, λ, k). Search them smartly.
- ➗ **Equation · L1:** random search finds a top-p region with probability `1 − (1−p)ⁿ` (n = 60 tries → 95 % for the top 5 %) · Bayesian / TPE: model the score, pick the next try by expected improvement
- ⌨️ **Build · L2:** `GridSearchCV`, `RandomizedSearchCV`, **Optuna** (TPE), successive halving; a **genetic algorithm** search (population → selection → crossover → mutation; `DEAP` / `TPOT`).
- 📊 **Measure · L2:** best score vs number of trials (same budget for each method).
- 📈 **Improve · L3:** defaults → grid → random → Optuna (all with the same time budget).
- 🎤 **Interview · L3:** Grid vs random? · What is Bayesian optimization? · How do you avoid overfitting the validation set?
- ✅ **Done when:** you log a tuning curve for one model.


## Chapter 23 — Explainability, error analysis and fairness

> ⚠️ **Common mistakes:** explaining with impurity importance only · looking at average error only (look at **slices**) · treating SHAP as causal.

### Levels 1 → 3 (inside the day) — Checkpoint D1
<a id="day-42"></a>
#### ☐ Day 42 — Explainability, error analysis, fairness
- 🧮 **New math today (just-in-time):** Shapley values (fair credit between features).
- 🧠 **Idea · L1:** know *why* a model decides. Find **which groups** it fails on. Check fairness.
- ➗ **Equation · L1:** permutation importance `= score − score(shuffled feature)` · SHAP `φᵢ = Σ_{S⊆F∖{i}} [|S|!(|F|−|S|−1)!/|F|!]·[f(S∪{i}) − f(S)]` · demographic parity `P(ŷ=1|A=a) = P(ŷ=1|A=b)`
- ⌨️ **Build · L2:** permutation importance, SHAP summary + force plot, LIME, partial-dependence; error by slice (e.g. department, month).
- 📊 **Measure · L2:** the 3 worst slices; fairness gap between groups.
- 📈 **Improve · L3:** fix the worst slice (features / weights / more data) and re-measure.
- 🎤 **Interview · L3:** SHAP vs permutation importance? · What is partial dependence? · How do you check fairness? · What privacy and ethics risks does an HR model have?
- ✅ **Checkpoint:** one full **ML project report** (problem → data → baseline → ladder → errors → explanation). 20 questions (Days 40–42).


## Chapter 24 — Time series

> **You will learn:** trend / seasonality, stationarity, ACF / PACF, AR / MA / ARIMA / SARIMA, lag-feature boosting, Prophet, backtesting.
> ⚠️ **Common mistakes:** random train/test split · no seasonal-naive baseline · future information in features.

### Level 1–2: classical models
<a id="day-43"></a>
#### ☐ Day 43 — Time series I: trend, seasonality, ACF/PACF and ARIMA
- 🧮 **New math today (just-in-time):** autocorrelation (ACF, PACF) · stationarity · differencing · moving average.
- 🧠 **Idea · L1:** order matters — never shuffle. A series = trend + seasonality + noise. **AR** uses past values, **MA** uses past errors, **ARIMA(p,d,q)** = AR + differencing + MA. Always beat the **seasonal-naive** baseline first.
- ➗ **Equation · L1:** AR(p) `yₜ = c + φ₁yₜ₋₁ + … + φₚyₜ₋ₚ + εₜ` · MA(q) `yₜ = μ + εₜ + θ₁εₜ₋₁ + …` · differencing `y′ₜ = yₜ − yₜ₋₁` · autocorrelation `ρₖ = Cov(yₜ, yₜ₋ₖ)/Var(y)`
- ⌨️ **Build · L2:** decompose your sales series; moving averages; ADF stationarity test; ACF/PACF plots → choose p, q; fit ARIMA / SARIMA with `statsmodels`; seasonal-naive baseline.
- 📊 **Measure · L2:** MAE / MAPE / sMAPE on a hold-out *at the end* of the series; residuals should look like white noise.
- 📈 **Improve · L3:** naive → seasonal-naive → moving average → ARIMA → SARIMA.
- 🎤 **Interview · L3:** What is stationarity and why does it matter? · AR vs MA? · Why not random CV for time series?
- ✅ **Done when:** you can read an ACF plot and pick (p, d, q) with a reason.


### Level 3: machine-learning forecasters and backtesting
<a id="day-44"></a>
#### ☐ Day 44 — Time series II: lag features, boosting, Prophet and backtesting
- 🧠 **Idea · L1:** turn forecasting into ordinary supervised learning with **lag / rolling / calendar features**, then use gradient boosting. Check with an **expanding-window backtest**. Prophet = a ready-made trend + seasonality + holidays model.
- ➗ **Equation · L1:** features `yₜ₋₁, yₜ₋₇, rolling_mean₇, month, holiday` · `sMAPE = (100/n)Σ 2|e|/(|y|+|ŷ|)` · backtest = repeat (train on past → predict next block)
- ⌨️ **Build · L2:** lag + rolling + calendar features; LightGBM / XGBoost forecaster; Prophet; expanding-window backtest on your sales data.
- 📊 **Measure · L2:** error per fold; where does it fail (holidays? level shifts? new products?).
- 📈 **Improve · L3:** seasonal-naive → ARIMA (Day 43) → lag features + LightGBM → + holiday features.
- 🎤 **Interview · L3:** Why lag features? · How do you avoid leakage in time series? · Backtesting vs ordinary CV?
- ✅ **Done when:** your forecast beats seasonal-naive in a backtest, and you can say why.


## Chapter 25 — Recommender systems

### Levels 1 → 3 (inside the day)
<a id="day-45"></a>
#### ☐ Day 45 — Recommender systems
- 🧮 **New math today (just-in-time):** cosine similarity (again) · matrix factorization · ranking metric NDCG.
- 🧠 **Idea · L1:** recommend with similarity (people like you / items like this) or with **latent factors** learned from a ratings matrix.
- ➗ **Equation · L1:** user-CF `sim(u,v) = cos(rᵤ, rᵥ)` · matrix factorization `r̂ᵤᵢ = pᵤ·qᵢ`, loss `Σ(rᵤᵢ − pᵤ·qᵢ)² + λ(‖p‖² + ‖q‖²)` · `NDCG = DCG/IDCG`
- ⌨️ **Build · L2:** item-based collaborative filtering; matrix factorization with SGD on a small ratings table (e.g. MovieLens-small, or your sales basket data).
- 📊 **Measure · L2:** precision@k, recall@k, NDCG; the cold-start problem (new user / new item).
- 📈 **Improve · L3:** popularity baseline → collaborative filtering → matrix factorization.
- 🎤 **Interview · L3:** Cold-start problem? · Explicit vs implicit feedback? · Why NDCG?
- ✅ **Done when:** your recommender beats the popularity baseline on precision@10.


## Chapter 26 — A/B testing and causal thinking

### Levels 1 → 3 (inside the day)
<a id="day-46"></a>
#### ☐ Day 46 — A/B tests and causal thinking
- 🧮 **New math today (just-in-time):** two-proportion z-test · power and sample size · confounders.
- 🧠 **Idea · L1:** an **A/B test** is the honest way to know if a change works. **Correlation ≠ causation** (Day 3): a *confounder* can create a fake link. Random assignment removes confounders.
- ➗ **Equation · L1:** `z = (p̂ᴮ − p̂ᴬ)/√(p̂(1−p̂)(1/nᴬ + 1/nᴮ))` · sample size per group `n ≈ 16σ²/δ²` (80 % power, 5 % level) · uplift `= P(buy|treated) − P(buy|control)`
- ⌨️ **Build · L2:** an A/B-test calculator (sample size + p-value + confidence interval); simulate a confounder (ice-cream sales vs drownings) and remove it by stratifying.
- 📊 **Measure · L2:** effect size + confidence interval, not just the p-value; what if you stop the test early (peeking)?
- 📈 **Improve · L3:** "looks better" → significance test → power analysis → pre-registered plan.
- 🎤 **Interview · L3:** How big must an A/B test be? · Give a confounder example. · What is peeking?
- ✅ **Done when:** you can design an A/B test for an HR-policy change.


## Chapter 27 — Classical-ML mock interview

### Part checkpoint
<a id="day-47"></a>
#### ☐ Day 47 — Classical-ML mock interview (Parts II–V checkpoint)
- 🧠 **Idea · L1:** rehearse everything from Days 1–46: the equation, how to build it, how it fails, how to improve it.
- ➗ **Equation · L1:** derive on a whiteboard (no notes): normal equation · logistic gradient · softmax + cross-entropy gradient · information gain · PCA from covariance · Bayes.
- ⌨️ **Build · L2:** code from memory: K-Means, logistic regression by GD, one decision-tree split, cosine search.
- 📊 **Measure · L2:** 50 random questions from your 20-question sets; self-score; list the 5 weakest topics.
- 📈 **Improve · L3:** re-study the 5 weakest topics (90 min each), re-test.
- 🎤 **Interview · L3:** record yourself answering the 10 hardest questions (30 minutes).
- ✅ **Done when:** ≥ 80 % on the self-test and the algorithm cheat-sheet table (Appendix C) is filled.


---

### ✅ Part V cheat card — cross-validation schemes
| Data | Scheme | Why |
|---|---|---|
| Normal, balanced | K-Fold (k = 5 or 10) | simple, low variance |
| Classes imbalanced | Stratified K-Fold | keeps class ratio in every fold |
| Same person / group many rows | Group K-Fold | no leakage between folds |
| Time ordered | **TimeSeriesSplit** (expanding window) | never train on the future |
| Tuning + honest score | Nested CV | outer = evaluate, inner = tune |
| Tiny data | Leave-One-Out / repeated K-Fold | use every row, higher cost |

[📖 Table of contents](README.md) · [← previous part](part4_unsupervised.md) · [next part →](part6_deep_learning_vision.md) · [Appendices](appendix.md)
