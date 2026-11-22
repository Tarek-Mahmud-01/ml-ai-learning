# PART II — Supervised Learning (a): Regression

[📖 Table of contents](README.md) · [← previous part](part1_start_here.md) · [next part →](part3_supervised_classification.md) · [Appendices](appendix.md)

> **Days 4–15 · Category: Supervised learning — predict a number · Levels: 1 → 3 in every chapter**
> **You will be able to:** build a linear regression three ways (closed form, gradient descent, matrices), check its assumptions, clean and encode data for it, measure it, fix over-/under-fitting, and ship a "Price predictor".
> **Math you meet here (just-in-time):** derivatives and partial derivatives (Day 5) · gradient and learning rate (Day 6) · vectors, matrices, the normal equation (Day 7) · hypothesis tests and p-values (Day 8) · L1 / L2 norms (Day 14).
> **Your class notes used:** *Pandas + Simple Linear Regression + Residuals + Cost* · *Loss Functions, Partial Derivatives & GD* · *Linear Regression, Evaluation, Bias–Variance* · *Feature Engineering, Transformation & Encoding*.

| Model | Predicts | Key equation | Day |
|---|---|---|---|
| Simple linear regression | a number from 1 feature | `ŷ = wx + b` | 4 |
| Multiple linear regression | a number from many features | `ŷ = Xw` | 7 |
| Polynomial / quadratic | curved relationships | `ŷ = w₀ + w₁x + w₂x²` | 14 |
| Ridge / Lasso / ElasticNet | regularized linear | `J + λΣw²`, `J + λΣ|w|` | 14 |

---

## Chapter 4 — Linear regression: from one line to many features

> **You will learn:** the line, residuals, the cost function, gradient descent, the matrix form, the normal equation, assumptions and p-values.
> ⚠️ **Common mistakes:** reading R² as accuracy · not scaling before GD · trusting coefficients when features are collinear · forgetting residual plots.

### Level 1 — Beginner: the line, the cost, the slope
<a id="day-4"></a>
#### ☐ Day 4 — Simple linear regression: the line & the residual — *your notes: Pandas + Simple Linear Regression + Residuals*
- 🧠 **Idea · L1:** predict a number from one feature with a straight line. **Residual** = actual − predicted.
- ➗ **Equation · L1:** `ŷ = w·x + b` · `eᵢ = yᵢ − ŷᵢ` · closed form `w = Σ(x−x̄)(y−ȳ) / Σ(x−x̄)²`, `b = ȳ − w·x̄`
- ⌨️ **Build · L2:** compute w, b by hand on 10 points; plot line + residuals; `LinearRegression`; read `coef_`, `intercept_`.
- 📊 **Measure · L2:** `Σe ≈ 0`; RMSE vs the Day-1 mean baseline.
- 📈 **Improve · L3:** mean baseline → best single feature (use r from Day 3).
- 🎤 **Interview · L3:** What is a residual? · Meaning of slope and intercept? · Why *squared* errors?
- ✅ **Done when:** your w, b equal sklearn's.

<a id="day-5"></a>
#### ☐ Day 5 — Cost function + derivatives — *your notes: Loss Functions, Partial Derivatives & GD*
- 🧮 **New math today (just-in-time):** derivative = slope · chain rule · partial derivative. (You already did this on paper in your earlier Day-2 calculus notes, `advanced_day2_calculus.md` / `.py` — reuse them if you still have them.)
- 🧠 **Idea · L1:** the **cost** `J` scores a line: low cost = good line. The best line is the lowest point of a bowl-shaped surface. A derivative tells you which way is *downhill*; a **partial derivative** does the same for one weight while the others stand still.
- ➗ **Equation · L1:** `J(w,b) = (1/2n) Σ(ŷᵢ − yᵢ)²` (the ½ cancels the 2) · `f′(x) = lim (f(x+h) − f(x))/h` · chain rule `d/dx f(g(x)) = f′(g(x))·g′(x)` · `∂J/∂w = (1/n) Σ(ŷ−y)·x` · `∂J/∂b = (1/n) Σ(ŷ−y)`
- ⌨️ **Build · L2:** compute `J` for a grid of `(w, b)` → contour plot of the bowl. Numeric derivative (central difference) of `x²`, `sin x` and of one-weight `J`. Check your formulas for `∂J/∂w`, `∂J/∂b` against the numeric result and against PyTorch autograd.
- 📊 **Measure · L2:** numeric vs analytic error shrinks as `h` gets smaller, then grows again (floating-point noise) — plot it.
- 📈 **Improve · L3:** forward difference → central difference → analytic formula → autograd. Why MSE and not absolute error? (MSE has a smooth derivative everywhere.)
- 🎤 **Interview · L3:** What is a cost function? · What is a partial derivative? · Why squared errors?
- ✅ **Done when:** numeric and analytic gradients agree to 1e-6 and you can draw the cost bowl and mark its minimum.


### Level 2 — Intermediate: gradient descent and matrices
<a id="day-6"></a>
#### ☐ Day 6 — Gradient descent for linear regression — *your notes: Gradient Descent*
- 🧮 **New math today (just-in-time):** gradient vector · learning rate · momentum.
- 🧠 **Idea · L1:** to reduce the cost, take a step **downhill** — opposite to the gradient. The learning rate `α` is the step size. The same idea trains every neural network later in this book.
- ➗ **Equation · L1:** `w ← w − α·∂J/∂w` · `b ← b − α·∂J/∂b` (gradients from Day 5) · momentum `v ← βv + g; w ← w − αv`
- ⌨️ **Build · L2:** GD on `f(x) = (x−3)²` first; then GD for linear regression on your Day-4 data; plot the path on the cost bowl; try `α = 0.001, 0.1, 1.1`; batch vs SGD vs mini-batch; with and without feature scaling (you will see why Day 11 matters).
- 📊 **Measure · L2:** loss per step; steps to converge; final RMSE must equal the closed-form line of Day 4.
- 📈 **Improve · L3:** fixed α → decaying α → momentum; count the steps to reach loss < 1e-6.
- 🎤 **Interview · L3:** Learning rate too big / too small? · Batch vs stochastic vs mini-batch? · How do you know GD converged? · Local minimum vs saddle point?
- ✅ **Done when:** your GD line equals the closed-form line to 4 decimals, and you can predict (before running) whether a given α will diverge.

<a id="day-7"></a>
#### ☐ Day 7 — Vectors & matrices ➜ multiple regression and the normal equation
- 🧮 **New math today (just-in-time):** vector, dot product, norm, matrix, transpose, matrix product, inverse · solving `Ax = b` (Gaussian elimination).
- 🧠 **Idea · L1:** many features = a table = a **matrix** `X`. The whole model is one matrix product `ŷ = Xw`. You can solve for the best `w` directly (**normal equation**) or with GD in matrix form. Read each coefficient as "how much `y` changes when this feature goes up by 1, others fixed".
- ➗ **Equation · L1:** `a·b = Σaᵢbᵢ` · `‖a‖ = √Σaᵢ²` · `Cᵢⱼ = Σₖ Aᵢₖ Bₖⱼ` · `ŷ = Xw` (X has a column of 1s for `b`) · `J = (1/2n)‖Xw − y‖²` · **normal equation** `w = (XᵀX)⁻¹Xᵀy` · `∇J = (1/n)Xᵀ(Xw − y)`
- ⌨️ **Build · L2:** matrix multiply with 3 loops vs `@`. Gaussian elimination solver for `Ax = b` (check with `np.linalg.solve`). Normal equation in NumPy. Matrix-form GD. Compare all with sklearn `LinearRegression` on `load_diabetes`. Make two columns collinear → `XᵀX` becomes singular → use `pinv` / `lstsq`.
- 📊 **Measure · L2:** the three methods give the same `w` (1e-6). RMSE vs the Day-1 baseline and vs the best single feature of Day 4. Timing: loops vs NumPy; read shape-mismatch errors.
- 📈 **Improve · L3:** `inv` → `solve` → `lstsq`; one feature → all features.
- 🎤 **Interview · L3:** When does the normal equation fail? · Its cost (O(p³))? · Why GD for huge data? · What does multicollinearity do to the coefficients?
- ✅ **Done when:** normal equation, GD and sklearn agree, and you can multiply a 2×3 and a 3×2 matrix on paper.


### Level 3 — Advanced: assumptions and inference
<a id="day-8"></a>
#### ☐ Day 8 — Assumptions, statsmodels and p-values — *your notes: Linear Regression*
- 🧮 **New math today (just-in-time):** hypothesis test · p-value · standard error · confidence interval · t-test, F-test (and the family: z-test, chi-square, ANOVA).
- 🧠 **Idea · L1:** a fitted line is only trustworthy if its **assumptions** hold — **L**inearity, **I**ndependence, **N**ormal residuals, **E**qual variance. A p-value answers: "if the true coefficient were 0, how surprising is what I saw?" (It is *not* the probability that the coefficient is 0.)
- ➗ **Equation · L1:** `t = ŵⱼ / SE(ŵⱼ)` · 95 % CI `ŵⱼ ± t*·SE(ŵⱼ)` · F-test for the whole model · `VIF = 1/(1 − R²ⱼ)` · residual `eᵢ = yᵢ − ŷᵢ`
- ⌨️ **Build · L2:** `statsmodels` OLS summary (coef, std err, t, p-value, CI, R², F-stat, Durbin–Watson). Residual-vs-fitted plot, Q–Q plot, VIF. One t-test, one chi-square test, one ANOVA with SciPy to see the family.
- 📊 **Measure · L2:** which assumption is broken, and how it looks on the plot; which coefficients are not significant.
- 📈 **Improve · L3:** raw → drop collinear features → log-transform the target → add a polynomial term (preview of Day 14).
- 🎤 **Interview · L3:** Assumptions of linear regression? · How do you read a coefficient and its p-value? · What does a confidence interval mean?
- ✅ **Done when:** you can read an OLS table line by line.


## Chapter 5 — Preparing data for regression

> **You will learn:** missing values, outliers, the 7 encodings and the 5 scalers — each shown *with its effect on the score*. **Your class notes:** *Feature Engineering, Transformation & Encoding*.
> ⚠️ **Common mistakes:** fitting the imputer / scaler on all data · one-hot on 10 000 categories · label-encoding a nominal feature for a linear model · deleting outliers that are real.

### Level 1 — Beginner: missing values and outliers
<a id="day-9"></a>
#### ☐ Day 9 — Missing values & outliers
- 🧠 **Idea · L1:** missing is not random: MCAR / MAR / MNAR. Outliers can be errors or real signals.
- ➗ **Equation · L1:** IQR fence `x < Q1 − 1.5·IQR or x > Q3 + 1.5·IQR` · z-score `|z| > 3` · mean impute `x̂ = x̄`
- ⌨️ **Build · L2:** detect + impute (mean / median / mode / KNN / iterative); add a *missing-indicator* column; outlier methods (IQR, z-score, winsorize).
- 📊 **Measure · L2:** same model, each strategy → validation RMSE (fit imputer on **train only**).
- 📈 **Improve · L3:** drop rows → mean → median → KNN + indicator.
- 🎤 **Interview · L3:** MCAR vs MAR vs MNAR? · Drop or impute? · Why fit the imputer on train only?
- ✅ **Done when:** a table shows the best strategy with numbers.


### Level 2 — Intermediate: encoding categories
<a id="day-10"></a>
#### ☐ Day 10 — Encoding (7 types) — *your notes: Encoding*
- 🧠 **Idea · L1:** models need numbers. **Label, One-Hot, Binary, Ordinal, Frequency, Mean/Target, Embedding.**
- ➗ **Equation · L1:** one-hot `k categories → k (or k−1) columns` · frequency `count(c)/n` · smoothed target `(Σy_c + m·ȳ)/(n_c + m)`
- ⌨️ **Build · L2:** each by hand, then `OneHotEncoder`, `OrdinalEncoder`, `category_encoders` (Binary, Target).
- 📊 **Measure · L2:** score + number of columns + **leakage check** for target encoding (out-of-fold).
- 📈 **Improve · L3:** label → one-hot → smoothed out-of-fold target encoding on a high-cardinality column.
- 🎤 **Interview · L3:** One-hot vs label? · How to handle 10 000 categories? · Why does target encoding leak?
- ✅ **Done when:** you can pick the encoder for any column in 10 seconds.


### Level 3 — Advanced: scaling and transforming
<a id="day-11"></a>
#### ☐ Day 11 — Scaling & transformation (5 types) — *your notes: Transformation*
- 🧠 **Idea · L1:** put features on similar ranges. **Min-Max, Standardization (Z), Log, Robust, Max-Abs** (+ Power / Quantile).
- ➗ **Equation · L1:** `(x−min)/(max−min)` · `(x−μ)/σ` · `(x−median)/IQR` · `x/max|x|` · `log(1+x)`
- ⌨️ **Build · L2:** from scratch + sklearn. Skewed salary before/after log. **Binning** (equal-width, equal-frequency, custom; `KBinsDiscretizer`), `PowerTransformer`, `QuantileTransformer`. Fit on train only.
- 📊 **Measure · L2:** KNN / SVM / logistic / tree score **with vs without** scaling.
- 📈 **Improve · L3:** none → standard → robust → log + standard.
- 🎤 **Interview · L3:** Which models need scaling? · Normalization vs standardization? · Why log for skew?
- ✅ **Done when:** you can show trees ignore scaling and KNN does not.


## Chapter 6 — Measuring a regression model and bias–variance

> **You will learn:** MAE / MSE / RMSE / R² / adjusted R² / MAPE, RSS-SST-RSE, train vs validation error, bias and variance, learning curves.
> ⚠️ **Common mistakes:** one metric only · judging on training error · adding features until R² "improves" (use adjusted R²).

### Levels 1 → 2: the metrics
<a id="day-12"></a>
#### ☐ Day 12 — Regression metrics
- 🧠 **Idea · L1:** pick the metric that matches the business. **R² is not accuracy** — it is "share of variance explained".
- ➗ **Equation · L1:** `RSS = Σe²` · `SST = Σ(y−ȳ)²` · `RSE = √(RSS/(n−p−1))` (your notes: *RSS, RSE, SST, R²*) · `MAE = (1/n)Σ|e|` · `MSE = (1/n)Σe²` · `RMSE = √MSE` · `R² = 1 − SS_res/SS_tot` · `adj R² = 1 − (1−R²)(n−1)/(n−p−1)` · `MAPE = (100/n)Σ|e/y|`
- ⌨️ **Build · L2:** all metrics from scratch → compare with `sklearn.metrics`.
- 📊 **Measure · L2:** add 3 outliers → see RMSE jump, MAE barely move. When can R² be negative?
- 📈 **Improve · L3:** choose MAE for "typical error", RMSE when big errors are costly; report both.
- 🎤 **Interview · L3:** MSE vs MAE vs RMSE? · Can R² be negative? · Why adjusted R²?
- ✅ **Done when:** you can justify a metric for 3 business cases.


### Level 3 — Advanced: over- and under-fitting
<a id="day-13"></a>
#### ☐ Day 13 — Overfitting, underfitting & bias–variance — *your notes: Bias-Variance*
- 🧮 **New math today (just-in-time):** the bias–variance decomposition of the expected error.
- 🧠 **Idea · L1:** too simple = **high bias** (underfit). Too flexible = **high variance** (overfit). Find the middle.
- ➗ **Equation · L1:** `E[(y − ŷ)²] = Bias² + Variance + Noise`
- ⌨️ **Build · L2:** polynomial degree 1…15 on noisy data; train vs validation error; **learning curve** and **validation curve**.
- 📊 **Measure · L2:** the train–validation gap.
- 📈 **Improve · L3:** underfit → add features/degree · overfit → more data, regularize, simplify.
- 🎤 **Interview · L3:** Define bias and variance. · How do learning curves show which one you have? · Four ways to reduce overfitting?
- ✅ **Done when:** you can read a learning curve and say what to do next.


## Chapter 7 — Regularization, polynomial features and the checkpoint

> **You will learn:** Ridge, Lasso, ElasticNet, polynomial / quadratic regression, `Pipeline`, and your first end-to-end deliverable.
> ⚠️ **Common mistakes:** not scaling before regularizing · choosing λ on the test set · very high polynomial degree.

### Levels 1 → 3: regularization
<a id="day-14"></a>
#### ☐ Day 14 — Regularization (Ridge, Lasso, ElasticNet) + polynomial features
- 🧮 **New math today (just-in-time):** L1 and L2 norms as penalties · polynomial / interaction terms.
- 🧠 **Idea · L1:** punish big weights so the model stays simple. Ridge shrinks; Lasso can set weights to exactly 0 (feature selection).
- ➗ **Equation · L1:** Ridge `J + λΣw²` · Lasso `J + λΣ|w|` · ElasticNet `J + λ(ρΣ|w| + (1−ρ)Σw²/2)` · Ridge closed form `w = (XᵀX + λI)⁻¹Xᵀy`
- ⌨️ **Build · L2:** Ridge from scratch (closed form) → check sklearn; Lasso with sklearn; coefficient-vs-λ path; `RidgeCV`, `LassoCV`. First create features: polynomial / quadratic (`PolynomialFeatures`), interactions, ratios, date-time parts (month, weekday).
- 📊 **Measure · L2:** validation RMSE vs λ (U-shaped curve).
- 📈 **Improve (ladder, log it) · L3:** linear → polynomial → poly + Ridge → poly + ElasticNet (tuned).
- 🎤 **Interview · L3:** L1 vs L2 — why does L1 give zeros? · How to choose λ? · Why scale before regularizing?
- ✅ **Done when:** Ridge shrinks and Lasso zeroes coefficients on your coefficient-vs-λ plot, and poly + ElasticNet beats plain OLS on validation.


### Checkpoint A
<a id="day-15"></a>
#### ☐ Day 15 — Regression checkpoint: pipeline + "Price predictor"
- 🧠 **Idea · L1:** put every step in one `Pipeline` + `ColumnTransformer`, so training and production run the *same* steps with no leakage. Then prove the improvement with your results table.
- ➗ **Equation · L1:** none new — "fit on train → transform everything".
- ⌨️ **Build · L2:** full pipeline (impute → encode → scale → model) on sales data or `load_diabetes`; `joblib.dump`, reload, predict; compare Ridge / Lasso / ElasticNet inside CV.
- 📊 **Measure · L2:** CV score of the *whole* pipeline; error analysis by slice (which rows are worst, why).
- 📈 **Improve (checkpoint) · L3:** mini-project **"Price predictor"** — V1 mean baseline (Day 1) → V2 best single feature (Day 4) → V3 all features + cleaning (Days 7–11) → V4 polynomial + ElasticNet tuned (Day 14). Wrap it in a FastAPI `/predict` + one pytest; commit.
- 🎤 **Interview · L3:** answer **20 questions** from Days 1–15 (write them in `plan120/interview_regression.md`).
- ✅ **Done when:** a new CSV goes through the saved pipeline in one call, and `results_log.md` shows V1 → V4.


---

### ✅ Part II cheat card — regression metrics
| Metric | Formula | Units | Outlier-sensitive? | Use when |
|---|---|---|---|---|
| MAE | `mean(\|e\|)` | same as y | low | "typical error" for business |
| MSE | `mean(e²)` | y² | high | training loss, math convenience |
| RMSE | `√MSE` | same as y | high | big errors are costly |
| R² | `1 − RSS/SST` | none | medium | share of variance explained (**not accuracy**) |
| Adjusted R² | `1 − (1−R²)(n−1)/(n−p−1)` | none | medium | comparing models with different # of features |
| MAPE | `mean(\|e/y\|)·100` | % | high (y ≈ 0) | percent error when y is never ≈ 0 |

### ✅ Part II cheat card — the linear-model family
| Model | Penalty | Shrinks to exactly 0? | Handles collinearity? | Needs scaling? |
|---|---|---|---|---|
| OLS | none | no | poorly | helps GD |
| Ridge | `λΣw²` | no | well | **yes** |
| Lasso | `λΣ\|w\|` | **yes** (selects features) | picks one of a group | **yes** |
| ElasticNet | mix | yes | well | **yes** |
| Huber (shelf, Day 121) | robust loss | no | — | yes |

[📖 Table of contents](README.md) · [← previous part](part1_start_here.md) · [next part →](part3_supervised_classification.md) · [Appendices](appendix.md)
