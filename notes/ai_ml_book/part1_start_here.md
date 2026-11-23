# PART I — Start Here: the ML workflow, your first look at data, correlation

[📖 Table of contents](README.md) · [next part →](part2_supervised_regression.md) · [Appendices](appendix.md)


> **Days 1–3 · Category: Foundations of practice · Levels: 1 → 3 inside every day**
> **You will be able to:** run any ML project in the right order (question → data → split → baseline → model → metric → error analysis → improve), describe a dataset with numbers and plots, and measure how two columns move together.
> **Math you meet here (just-in-time):** error and RMSE (Day 1) · mean, variance, std, IQR, z-score, CLT (Day 2) · covariance and Pearson r (Day 3).
> **No separate maths block.** From here to Day 47 every new maths idea is taught on the day an algorithm first needs it. See [Appendix A — Math map](appendix.md#a-math-map).

---

## Chapter 1 — The ML workflow: baseline, split, metric, error

> **Why first:** every later chapter ends with "baseline → V1 … V4". Learn the loop once, use it 100 times.
> ⚠️ **Common mistakes:** no baseline · tuning on the test set · choosing a metric after seeing the results · fitting scalers on all data (leakage).

### Levels 1 → 3 (inside the day)
<a id="day-1"></a>
#### ☐ Day 1 — Setup + the ML workflow (baseline, split, metric, error)
- 🧮 **New math today (just-in-time):** error `e = y − ŷ`, RMSE, and the mean as the simplest predictor (the baseline).
- 🧠 **Idea · L1:** ML = learn a rule from examples. Workflow: question → data → **split** → **baseline** → model → **metric** → **error analysis** → improve. A *baseline* (always predict the mean) is the score every model must beat.
- ➗ **Equation · L1:** `error eᵢ = yᵢ − ŷᵢ` · baseline `ŷ = ȳ` · `RMSE = √( (1/n) Σ eᵢ² )`
- ⌨️ **Build · L2:** check `venv` + `requirements.txt`; create `plan120/`. Load `load_diabetes`; split 70/15/15 by hand; baseline mean predictor; RMSE by hand → check with `DummyRegressor`.
- 📊 **Measure · L2:** baseline RMSE on validation. List the 10 biggest errors. Write: "this is the score to beat".
- 📈 **Improve · L3:** V1 = mean baseline (log it). Preview V2 = a one-feature line (done properly on Day 4).
- 🎤 **Interview · L3:** Train vs validation vs test? · Why a baseline? · What is data leakage (one example)?
- ✅ **Done when:** environment runs, baseline RMSE is in `results_log.md`.


## Chapter 2 — First look at data: EDA and descriptive statistics

> **You will learn:** types of data, centre / spread / shape, plots, data-quality checks, sampling and the Central Limit Theorem.
> ⚠️ **Common mistakes:** trusting `describe()` without plots · using the mean on skewed data · ignoring duplicates and wrong dtypes.

### Levels 1 → 3 (inside the day)
<a id="day-2"></a>
#### ☐ Day 2 — First look at data: EDA + descriptive statistics
- 🧮 **New math today (just-in-time):** mean, median, variance, standard deviation, IQR, z-score, skewness · population vs sample (`n−1`) · Central Limit Theorem · sampling and bias.
- 🧠 **Idea · L1:** look before you model. Describe every column by its **centre**, **spread** and **shape**. Know the data types: numeric (continuous / discrete), categorical (nominal / ordinal), date-time, text. A *sample* is a small piece of the *population*. The CLT says: averages of many samples look Normal, even if the data does not.
- ➗ **Equation · L1:** `x̄ = Σx/n` · `s² = Σ(x−x̄)²/(n−1)` · `z = (x−x̄)/s` · standard error `= s/√n` · `IQR = Q3 − Q1` · skewness `E[(x−μ)³]/σ³` · missing % `= #NaN/n`
- ⌨️ **Build · L2:** load your **sales data** (`data/`) and `load_diabetes`: `shape, dtypes, describe, value_counts, isna().mean()`, duplicates, constant columns. Mean / median / variance / std / IQR **from scratch** → compare with NumPy, pandas, SciPy. Plot histogram + boxplot with Matplotlib and Seaborn (try Plotly and Polars on the same table). CLT simulation: means of 1 000 samples from a skewed distribution.
- 📊 **Measure · L2:** your numbers = library numbers (diff < 1e-9). Why `n−1`? Show the bias of dividing by `n` on tiny samples. Write a **data-quality checklist** (missing %, duplicates, skew, wrong dtypes, impossible values).
- 📈 **Improve · L3:** mean → median → trimmed mean on data with outliers (which centre stays stable?). Raw table → fixed dtypes → ranked list of data issues.
- 🎤 **Interview · L3:** Mean vs median — when? · Why divide by n−1? · Steps of EDA? · What does a skewed feature do to a model?
- ✅ **Done when:** you have a 1-page EDA report on the sales data and can explain the CLT with your own simulation plot.


## Chapter 3 — Correlation: do two columns move together?

> **You will learn:** covariance, Pearson r (both formulas), Spearman, correlation ≠ causation. **Your class notes:** *Study Notes: Correlation (Pearson)*.
> ⚠️ **Common mistakes:** r = 0 means "no relationship" (it only means no *linear* one) · one outlier changing r · reading a heat-map as causation.

### Levels 1 → 3 (inside the day)
<a id="day-3"></a>
#### ☐ Day 3 — Correlation & covariance (Pearson r) — *your notes: Correlation*
- 🧮 **New math today (just-in-time):** covariance and the Pearson correlation coefficient `r`.
- 🧠 **Idea · L1:** do two variables move together? Covariance has a sign; correlation rescales it to −1…1. Only **linear** relationships. Correlation ≠ causation.
- ➗ **Equation · L1:** `cov(X,Y) = Σ(x−x̄)(y−ȳ)/(n−1)` · `r = cov(X,Y)/(sₓ·s_y)` = `[nΣxy − ΣxΣy] / √([nΣx² − (Σx)²][nΣy² − (Σy)²])`
- ⌨️ **Build · L2:** r with **both** formulas → check `np.corrcoef`. Correlation heat-map on diabetes. Counter-example: `y = x²` gives r ≈ 0.
- 📊 **Measure · L2:** Pearson vs Spearman (Pearson on ranks). Error analysis: one outlier can change r a lot (Anscombe's quartet).
- 📈 **Improve · L3:** Pearson → Spearman for curved-but-monotone data → remove outlier. Use r to rank features.
- 🎤 **Interview · L3:** What does r = 0 mean? · Pearson vs Spearman? · Give a correlation-not-causation example.
- ✅ **Done when:** both formulas give the same r to 1e-12.


---

### ✅ Part I summary (cheat card)
| Idea | One-line rule |
|---|---|
| Baseline | Always compute the dumb score first (mean / majority class). |
| Split | Train fits, validation chooses, test is touched **once**. |
| Centre | Mean for symmetric data, median for skewed or outlier-heavy data. |
| Spread | Standard deviation (normal data) or IQR (any data). |
| Pearson r | −1…1, linear only, sensitive to outliers. |

[📖 Table of contents](README.md) · [next part →](part2_supervised_regression.md) · [Appendices](appendix.md)
