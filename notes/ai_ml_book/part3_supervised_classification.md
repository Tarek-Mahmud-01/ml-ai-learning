# PART III — Supervised Learning (b): Classification

[📖 Table of contents](README.md) · [← previous part](part2_supervised_regression.md) · [next part →](part4_unsupervised.md) · [Appendices](appendix.md)


> **Days 16–33 · Category: Supervised learning — predict a category (best: a probability) · Levels: 1 → 3 in every chapter**
> **You will be able to:** explain, build and improve the 12 classic classifiers — logistic regression, KNN, Naive Bayes, LDA/QDA, SVM/SVR, decision trees, Random Forest, Extra Trees, AdaBoost, Gradient Boosting, XGBoost / LightGBM / CatBoost, stacking — and choose between them with the right metric.
> **Math you meet here (just-in-time):** probability, Bayes, distributions (Day 16) · odds, sigmoid (17) · MLE, entropy, cross-entropy, KL (18) · distances (23) · margin, hinge loss (25) · information gain (27) · variance of an average (29) · Hessian (32).
> **Your class notes used:** *Distance Metrics (KNN, Naive Bayes, K-Means)* · *Decision Tree, XGBoost, SVM, Ensembles* · *Random Forest, Post-pruning, Data Leakage, Grid / Random search*.

---

## Chapter 8 — Logistic regression and softmax

> **You will learn:** from a line to a probability: odds, sigmoid, maximum likelihood, log loss, gradient descent from scratch, multi-class softmax.
> ⚠️ **Common mistakes:** linear regression on 0/1 labels · MSE as a classification loss · reading a coefficient as a probability change (it is a **log-odds** change) · forgetting to scale features.

### Level 1 — Beginner: probability, odds, sigmoid
<a id="day-16"></a>
#### ☐ Day 16 — Probability, Bayes and distributions — and what "classification" means
- 🧮 **New math today (just-in-time):** probability rules · conditional probability · Bayes' theorem · random variables, expected value · Bernoulli, Binomial, Normal, Poisson, Uniform, Exponential · combinatorics · Law of Large Numbers · Markov-chain idea.
- 🧠 **Idea · L1:** regression predicts a *number*; **classification** predicts a *category* — and the best answer is a **probability**. Probability = belief in numbers. **Bayes** updates a belief with evidence.
- ➗ **Equation · L1:** `P(A|B) = P(B|A)·P(A)/P(B)` · `E[X] = Σ x·p(x)` · Normal pdf `1/(σ√(2π))·exp(−(x−μ)²/(2σ²))` · permutations `n!/(n−k)!` · combinations `n!/(k!(n−k)!)`
- ⌨️ **Build · L2:** simulate coins, dice and Normal samples. Medical-test / spam example with Bayes from scratch. Monte-Carlo estimate of π. Plot the 6 distributions.
- 📊 **Measure · L2:** law of large numbers — error of an estimate vs `n` (plot). Check: Bayes by hand = Bayes in code.
- 📈 **Improve · L3:** guess with no prior → add a prior → update with more evidence (watch the posterior move).
- 🎤 **Interview · L3:** Explain Bayes with an example. · Prior vs posterior? · Independent vs uncorrelated? · Why predict probabilities, not just labels?
- ✅ **Done when:** you solve a Bayes problem on paper without help.

<a id="day-17"></a>
#### ☐ Day 17 — Logistic regression I: odds, log-odds and the sigmoid
- 🧮 **New math today (just-in-time):** odds · log-odds (logit) · sigmoid function.
- 🧠 **Idea · L1:** start from the linear regression you know. A line gives any number; a probability must stay in 0…1. The **sigmoid** squashes any score into 0…1. The coefficient now means "change in **log-odds**".
- ➗ **Equation · L1:** `z = w·x + b` · `p = σ(z) = 1/(1 + e^(−z))` · odds `= p/(1−p)` · `logit(p) = ln(p/(1−p)) = z` · decision rule `ŷ = 1 if p ≥ 0.5`
- ⌨️ **Build · L2:** try linear regression on 0/1 labels (see predictions below 0 and above 1 — why it fails). Sigmoid + prediction from scratch with given weights; 2-D decision-boundary plot on `breast_cancer`; `LogisticRegression` → read `coef_` as odds ratios (`e^w`).
- 📊 **Measure · L2:** accuracy vs the majority-class baseline. Where is the boundary and which points are on the wrong side?
- 📈 **Improve · L3:** linear regression on 0/1 → logistic (trained properly on Day 18).
- 🎤 **Interview · L3:** Why sigmoid? · Why not linear regression for classification? · How to read a coefficient (odds ratio)?
- ✅ **Done when:** you can turn a coefficient into "odds multiply by …".


### Level 2 — Intermediate: maximum likelihood and training from scratch
<a id="day-18"></a>
#### ☐ Day 18 — Logistic regression II: likelihood, log loss and training from scratch
- 🧮 **New math today (just-in-time):** maximum likelihood (MLE) · entropy · cross-entropy · KL divergence.
- 🧠 **Idea · L1:** **maximum likelihood** = choose the parameters that make the data most likely. **Entropy** = surprise. **Cross-entropy** = surprise when you believe `q` but the truth is `p` — this is the loss of every classifier. MSE is MLE under Gaussian noise; log loss is MLE for yes/no data.
- ➗ **Equation · L1:** `θ̂ = argmax Σ log p(xᵢ|θ)` · `H(p) = −Σ p log p` · `H(p,q) = −Σ p log q` · `KL(p‖q) = H(p,q) − H(p)` · **log loss** `L = −(1/n)Σ[y·log p + (1−y)·log(1−p)]` · gradient `∇ = (1/n)Xᵀ(p − y)` (same shape as linear regression!)
- ⌨️ **Build · L2:** MLE of a coin bias (grid search vs formula); entropy of a fair vs biased coin; cross-entropy of two distributions. Then logistic regression by **gradient descent from scratch** on `breast_cancer` (loss curve) → compare `LogisticRegression`.
- 📊 **Measure · L2:** log-likelihood peaks at the MLE; accuracy + loss curve; your model matches sklearn within 1 %.
- 📈 **Improve · L3:** unscaled → scaled → tuned α → L2 penalty (`C`).
- 🎤 **Interview · L3:** Why cross-entropy and not MSE for classification? · What is KL divergence? · Derive the logistic gradient.
- ✅ **Done when:** you can derive "why cross-entropy" from MLE on one page.


### Level 3 — Advanced: many classes
<a id="day-19"></a>
#### ☐ Day 19 — Multi-class: softmax
- 🧮 **New math today (just-in-time):** the softmax function and its cross-entropy gradient `p − y`.
- 🧠 **Idea · L1:** many classes → one score per class → turn scores into probabilities that add to 1.
- ➗ **Equation · L1:** `softmax(zₖ) = e^{zₖ}/Σⱼ e^{zⱼ}` · cross-entropy `L = −Σₖ yₖ log pₖ` · gradient w.r.t. scores `= p − y`
- ⌨️ **Build · L2:** softmax regression from scratch on `digits` / `wine` (subtract max for stability); One-vs-Rest vs multinomial in sklearn.
- 📊 **Measure · L2:** per-class precision/recall; confusion matrix; which digits are confused and why.
- 📈 **Improve · L3:** raw pixels → scaled → regularized → tuned C.
- 🎤 **Interview · L3:** Softmax vs sigmoid? · OvR vs OvO? · Why subtract the max?
- ✅ **Done when:** you can explain the confusion matrix of digits.


## Chapter 9 — Classification metrics, imbalance and thresholds

> **You will learn:** confusion matrix, precision / recall / F1, ROC-AUC vs PR-AUC, class imbalance, data leakage, threshold choice and calibration.
> ⚠️ **Common mistakes:** accuracy on imbalanced data · SMOTE before the split · using 0.5 as a sacred threshold · reporting AUC without a PR curve for rare events.

### Level 1 — Beginner: the metrics
<a id="day-20"></a>
#### ☐ Day 20 — Classification metrics
- 🧠 **Idea · L1:** different mistakes cost different money. Pick the metric from the cost.
- ➗ **Equation · L1:** `Precision = TP/(TP+FP)` · `Recall = TP/(TP+FN)` · `F1 = 2PR/(P+R)` · `FPR = FP/(FP+TN)` · ROC-AUC = P(score of random positive > random negative) · macro / micro / weighted averages
- ⌨️ **Build · L2:** confusion matrix by hand; ROC and PR curves from thresholds; `classification_report`.
- 📊 **Measure · L2:** fraud (miss = costly) vs spam (false alarm = costly): which metric?
- 📈 **Improve · L3:** accuracy → F1 → PR-AUC for imbalanced data.
- 🎤 **Interview · L3:** Precision–recall trade-off? · What does AUC mean? · ROC-AUC vs PR-AUC?
- ✅ **Done when:** you can compute F1 on paper from a 2×2 table.


### Level 2 — Intermediate: imbalance and leakage
<a id="day-21"></a>
#### ☐ Day 21 — Imbalanced data & data leakage
- 🧠 **Idea · L1:** when 98 % of rows are "normal", accuracy lies. Fix with weights, re-sampling (SMOTE), and the right metric + threshold.
- ➗ **Equation · L1:** class weight `w_c = n/(k·n_c)` · SMOTE `x_new = xᵢ + λ(x_nn − xᵢ)`, `λ ∈ [0,1]`
- ⌨️ **Build · L2:** make a 2 % fraud set. Show the accuracy trap. `class_weight`, random over/under, SMOTE, SMOTE-Tomek (inside CV only!). Leakage demo: scale **before** split → inflated score.
- 📊 **Measure · L2:** confusion matrix, recall, **PR-AUC** (not accuracy).
- 📈 **Improve · L3:** baseline → class weights → SMOTE in CV → threshold tuning.
- 🎤 **Interview · L3:** Why does accuracy fail? · Why SMOTE only inside CV? · Name 3 leakage examples.
- ✅ **Done when:** you can catch leakage in someone else's notebook.


### Level 3 — Advanced: thresholds, cost and calibration (Checkpoint B1)
<a id="day-22"></a>
#### ☐ Day 22 — Thresholds & calibration
- 🧠 **Idea · L1:** 0.5 is not magic. Choose the threshold from cost. A good probability should be **calibrated** ("70 % → right 70 % of the time").
- ➗ **Equation · L1:** expected cost `C_FP·FP + C_FN·FN` · Brier score `(1/n)Σ(p − y)²`
- ⌨️ **Build · L2:** threshold sweep that minimizes cost; calibration curve; `CalibratedClassifierCV`.
- 📊 **Measure · L2:** cost at 0.5 vs best threshold.
- 📈 **Improve · L3:** default → best threshold → calibrated.
- 🎤 **Interview · L3:** How do you choose a threshold? · What is calibration and when does it matter?
- ✅ **Checkpoint:** mini-project **"Employee attrition / churn classifier"** + FastAPI + test + 20 questions (Days 16–22).


## Chapter 10 — K-Nearest Neighbours and distance metrics

> **Your class notes:** *Distance Metrics* (Manhattan, Euclidean, cosine, KNN).
> ⚠️ **Common mistakes:** not scaling · wrong `k` · using it on 1 000 features (curse of dimensionality).

### Levels 1 → 3 (inside the day)
<a id="day-23"></a>
#### ☐ Day 23 — K-Nearest Neighbours and distance metrics — *your notes: Distance Metrics*
- 🧮 **New math today (just-in-time):** distance metrics: Euclidean, Manhattan, Minkowski, cosine · the curse of dimensionality.
- 🧠 **Idea · L1:** "tell me who your neighbours are". No training; all work at prediction time.
- ➗ **Equation · L1:** Euclidean `√Σ(aᵢ−bᵢ)²` · Manhattan `Σ|aᵢ−bᵢ|` · Minkowski `(Σ|aᵢ−bᵢ|ᵖ)^(1/p)` · cosine `a·b/(‖a‖‖b‖)` · `ŷ = majority / mean of the k nearest` · weighted vote `wᵢ = 1/dᵢ`
- ⌨️ **Build · L2:** every distance from scratch vs `scipy.spatial.distance`; "nearest row to a query row"; KNN from scratch with NumPy; k vs validation error curve; effect of scaling; KD-tree timing.
- 📊 **Measure · L2:** bias–variance in k (k=1 overfits, big k underfits).
- 📈 **Improve · L3:** k=1 → tuned k → scaled → distance-weighted → better metric.
- 🎤 **Interview · L3:** Euclidean vs Manhattan vs cosine — when? · How to choose k? · Why is predict slow? · Why does KNN suffer in high dimensions?
- ✅ **Done when:** from-scratch KNN = sklearn KNN.


## Chapter 11 — Generative classifiers: Naive Bayes, LDA, QDA

> ⚠️ **Common mistakes:** no smoothing · assuming independence blindly · LDA when classes clearly have different spreads.

### Levels 1 → 3 (inside the day)
<a id="day-24"></a>
#### ☐ Day 24 — Generative classifiers: Naive Bayes, LDA and QDA
- 🧮 **New math today (just-in-time):** Bayes in use · class-conditional Gaussian · covariance matrix of a class.
- 🧠 **Idea · L1:** **discriminative** models (logistic) learn the boundary directly. **Generative** models learn how each class *generates* its data, then use Bayes. **Naive Bayes** assumes features are independent given the class. **LDA** assumes one shared covariance (straight boundary); **QDA** one covariance per class (curved boundary).
- ➗ **Equation · L1:** `P(c|x) ∝ P(c)·Πᵢ P(xᵢ|c)` · Laplace smoothing `(count + α)/(N + α·V)` · Gaussian NB uses the normal pdf per class · LDA score `δ_c(x) = xᵀΣ⁻¹μ_c − ½μ_cᵀΣ⁻¹μ_c + ln P(c)`
- ⌨️ **Build · L2:** spam toy example from scratch (use log-probabilities); sklearn `GaussianNB`, `MultinomialNB`, `LinearDiscriminantAnalysis`, `QuadraticDiscriminantAnalysis` on `wine` / `breast_cancer`; decision-boundary plots.
- 📊 **Measure · L2:** accuracy, log loss, what breaks when a word was never seen (zero probability).
- 📈 **Improve · L3:** no smoothing → Laplace → TF-IDF features; LDA → QDA when classes have different shapes.
- 🎤 **Interview · L3:** Why "naive"? · Generative vs discriminative? · LDA vs logistic regression? · Why is NB good on text?
- ✅ **Done when:** you can compute a spam probability by hand and say when LDA beats QDA.


## Chapter 12 — Support vector machines (SVC and SVR)

> ⚠️ **Common mistakes:** RBF kernel without scaling · huge `C` (overfit) · SVM on millions of rows (slow).

### Levels 1 → 3 (inside the day)
<a id="day-25"></a>
#### ☐ Day 25 — Support vector machines (SVC) and support vector regression (SVR)
- 🧮 **New math today (just-in-time):** margin and the norm `‖w‖` · hinge loss · kernel function · ε-insensitive loss.
- 🧠 **Idea · L1:** draw the line with the **widest margin**. Support vectors = the points that touch the margin. Kernels bend the line. **SVR** fits a "tube" of width `ε` around the data and ignores errors inside it.
- ➗ **Equation · L1:** hyperplane `w·x + b = 0` · margin `2/‖w‖` · hinge loss `max(0, 1 − y(w·x + b))` · soft margin `½‖w‖² + C·Σξᵢ` · RBF kernel `exp(−γ‖x − x′‖²)` · SVR loss `max(0, |y − ŷ| − ε)`
- ⌨️ **Build · L2:** linear SVM by sub-gradient descent from scratch; `SVC` with linear / poly / RBF kernels on `make_moons`; `SVR` on a noisy curve.
- 📊 **Measure · L2:** effect of `C` (soft vs hard margin) and `γ` (smooth vs wiggly boundary); number of support vectors.
- 📈 **Improve · L3:** linear → RBF → tuned (C, γ) → scaled features.
- 🎤 **Interview · L3:** What are support vectors? · Role of C and gamma? · What is the kernel trick? · SVR vs linear regression?
- ✅ **Done when:** you can draw margin + support vectors on paper.


## Chapter 13 — Choosing between models (shoot-out)

### Levels 1 → 3 (inside the day) — Checkpoint B2
<a id="day-26"></a>
#### ☐ Day 26 — Model shoot-out
- 🧠 **Idea · L1:** no model wins everywhere ("no free lunch"). Compare fairly: same split, same CV, same metric.
- ➗ **Equation · L1:** `CV score = (1/K)Σ scoreₖ` ± std.
- ⌨️ **Build · L2:** logistic, KNN, NB, SVM on 3 datasets with the same 5-fold CV; one summary table.
- 📊 **Measure · L2:** accuracy, F1, train time, predict time.
- 📈 **Improve · L3:** write a one-page **"how to choose a model"** guide from your own table.
- 🎤 **Interview · L3:** answer **20 questions** on Days 16–26. When KNN? When SVM? When NB?
- ✅ **Checkpoint:** FastAPI endpoint that serves the best model + test.


## Chapter 14 — Decision trees

> **Your class notes:** *Decision Tree Algorithm*, *Post-pruning*.
> ⚠️ **Common mistakes:** a full-depth tree (memorizes) · reading impurity importance as truth · scaling features (trees do not need it).

### Level 1 — Beginner: how a split is chosen
<a id="day-27"></a>
#### ☐ Day 27 — Decision tree: how a split is chosen — *your notes: Decision Tree*
- 🧮 **New math today (just-in-time):** entropy, Gini impurity and information gain (entropy was introduced on Day 18).
- 🧠 **Idea · L1:** a flowchart of yes/no questions. At each node pick the question that makes the groups **purest**.
- ➗ **Equation · L1:** entropy `H = −Σ pᵢ log₂ pᵢ` · Gini `1 − Σ pᵢ²` · information gain `IG = H(parent) − Σ (nᵢ/n)·H(childᵢ)` · regression: variance (MSE) reduction
- ⌨️ **Build · L2:** compute IG by hand on the small "play tennis" table; best-split search over thresholds for one numeric column.
- 📊 **Measure · L2:** Gini vs entropy choose (almost) the same splits — show it.
- 📈 **Improve · L3:** one split (stump) → depth 2 → depth 3: log accuracy.
- 🎤 **Interview · L3:** Entropy vs Gini? · What is information gain? · How are numeric features split?
- ✅ **Done when:** your hand-made tree equals `DecisionTreeClassifier` on the toy table.


### Level 2–3 — Intermediate to Advanced: building it and pruning it
<a id="day-28"></a>
#### ☐ Day 28 — Tree from scratch, overfitting & pruning
- 🧠 **Idea · L1:** a full tree memorizes. Limit it or prune it.
- ➗ **Equation · L1:** cost-complexity `R_α(T) = R(T) + α·|T|` (|T| = number of leaves) · stop rules: `max_depth`, `min_samples_leaf`
- ⌨️ **Build · L2:** recursive tree (~60 lines) → compare sklearn; `plot_tree`; `ccp_alpha` path.
- 📊 **Measure · L2:** train vs validation accuracy as depth grows.
- 📈 **Improve · L3:** full tree → depth-limited → pruned (log all).
- 🎤 **Interview · L3:** Why do trees overfit? · Pre-pruning vs post-pruning? · Pros and cons of trees?
- ✅ **Done when:** your tree gets within 2 % of sklearn.


## Chapter 15 — Bagging, Random Forest and Extra Trees

> **Your class notes:** *Random Forest, Row Sampling, Features*.
> ⚠️ **Common mistakes:** too few trees · judging by training score · trusting impurity importance (use permutation importance).

### Levels 1 → 3 (inside the day)
<a id="day-29"></a>
#### ☐ Day 29 — Bagging, Random Forest & Extra Trees — *your notes: Random Forest*
- 🧮 **New math today (just-in-time):** variance of an average: `ρσ² + (1−ρ)σ²/B`.
- 🧠 **Idea · L1:** many different trees vote. Each tree sees a random sample of rows and a random subset of features → errors cancel.
- ➗ **Equation · L1:** bootstrap keeps ≈ 63.2 % unique rows · variance of an average `ρσ² + (1−ρ)σ²/B` · features per split `≈ √p`
- ⌨️ **Build · L2:** bagging of your trees from scratch; `RandomForest`; **OOB score**; impurity vs **permutation** importance; **Extra Trees** (random split thresholds) vs Random Forest — compare score and speed.
- 📊 **Measure · L2:** accuracy vs number of trees (plateau); OOB ≈ CV score.
- 📈 **Improve · L3:** one tree → bagging → random forest → tuned (`max_features`, `min_samples_leaf`).
- 🎤 **Interview · L3:** Why does averaging reduce variance? · What is OOB? · Why is impurity importance biased?
- ✅ **Done when:** you can explain `ρ` (tree correlation) and why feature sub-sampling lowers it.


## Chapter 16 — Boosting: AdaBoost → Gradient Boosting → XGBoost / LightGBM / CatBoost

> **You will learn:** why boosting is "gradient descent in function space" and which library to pick.
> ⚠️ **Common mistakes:** big learning rate with few trees · no early stopping · tuning 20 parameters at once.

### Level 1 — Beginner: re-weighting mistakes
<a id="day-30"></a>
#### ☐ Day 30 — AdaBoost
- 🧠 **Idea · L1:** train weak learners one after another; **raise the weight of rows the last learner got wrong**.
- ➗ **Equation · L1:** error `εₜ = Σ wᵢ·1[hₜ(xᵢ) ≠ yᵢ]` · learner weight `αₜ = ½ ln((1−εₜ)/εₜ)` · `wᵢ ← wᵢ·exp(−αₜ yᵢ hₜ(xᵢ))` (then normalize) · `H(x) = sign(Σ αₜ hₜ(x))`
- ⌨️ **Build · L2:** AdaBoost with decision stumps from scratch; sklearn `AdaBoostClassifier`.
- 📊 **Measure · L2:** sample-weight plot per round; sensitivity to noisy labels.
- 📈 **Improve · L3:** 1 stump → 50 → 200 rounds → tuned learning rate.
- 🎤 **Interview · L3:** How does AdaBoost pick weights? · Why sensitive to outliers? · Bagging vs boosting?
- ✅ **Done when:** from-scratch accuracy ≈ sklearn.


### Level 2 — Intermediate: fitting residuals
<a id="day-31"></a>
#### ☐ Day 31 — Gradient Boosting
- 🧠 **Idea · L1:** each new tree fits the **mistakes (residuals)** of the model so far. It is gradient descent in "function space".
- ➗ **Equation · L1:** `Fₘ(x) = Fₘ₋₁(x) + ν·hₘ(x)` · for squared loss, `hₘ` fits `rᵢ = yᵢ − Fₘ₋₁(xᵢ)` (the negative gradient) · `ν` = learning rate
- ⌨️ **Build · L2:** gradient boosting regressor from scratch with depth-3 trees; compare `GradientBoostingRegressor`.
- 📊 **Measure · L2:** validation error vs number of trees (it turns up → overfit) → early stopping.
- 📈 **Improve · L3:** ν=1 → ν=0.1 with more trees → subsample 0.8 → early stopping.
- 🎤 **Interview · L3:** Why is it called *gradient* boosting? · Learning rate vs n_estimators? · Boosting vs random forest?
- ✅ **Done when:** your from-scratch model matches sklearn's RMSE within 3 %.


### Level 3 — Advanced: the modern libraries
<a id="day-32"></a>
#### ☐ Day 32 — XGBoost, LightGBM, CatBoost (+ HistGradientBoosting)
- 🧮 **New math today (just-in-time):** the second derivative (Hessian) of the loss.
- 🧠 **Idea · L1:** gradient boosting made fast and regularized. Uses first **and second** derivatives.
- ➗ **Equation · L1:** objective `Σ L(yᵢ, ŷᵢ) + Σ Ω(f)`, `Ω = γT + ½λΣw²` · best leaf weight `w* = −G/(H + λ)` (G = Σ gradients, H = Σ hessians) · split gain `½[G_L²/(H_L+λ) + G_R²/(H_R+λ) − (G_L+G_R)²/(H_L+H_R+λ)] − γ`
- ⌨️ **Build · L2:** the three libraries (and the scikit-learn `HistGradientBoosting`) on the same tabular set; early stopping; feature importance; CatBoost with raw categorical columns.
- 📊 **Measure · L2:** score, train time, memory. LightGBM = leaf-wise growth; XGBoost = level-wise; CatBoost = ordered target statistics.
- 📈 **Improve · L3:** defaults → key params (`learning_rate, max_depth, subsample, colsample_bytree, reg_lambda`) → Optuna (Day 41).
- 🎤 **Interview · L3:** What does XGBoost add over GBM? · Leaf-wise vs level-wise? · Why is CatBoost good with categories?
- ✅ **Done when:** you can name the 5 most important boosting params and what each does.


## Chapter 17 — Stacking, voting and blending

### Levels 1 → 3 (inside the day) — Checkpoint B3
<a id="day-33"></a>
#### ☐ Day 33 — Stacking, voting, blending
- 🧠 **Idea · L1:** combine different models. A **meta-learner** learns how to trust each one, using **out-of-fold** predictions.
- ➗ **Equation · L1:** voting `ŷ = argmax Σ wₘ·1[ŷₘ = c]` · blending `ŷ = Σ wₘ ŷₘ`
- ⌨️ **Build · L2:** `VotingClassifier`, `StackingClassifier`; manual out-of-fold stacking.
- 📊 **Measure · L2:** gain over the best single model; correlation between model errors.
- 📈 **Improve · L3:** best single → soft vote → stack with logistic meta-learner.
- 🎤 **Interview · L3:** Stacking vs blending? · Why out-of-fold? · When does an ensemble not help?
- ✅ **Checkpoint:** **"Tabular benchmark"** — one table with *all* models from Days 4–33 on one dataset (CV score, time) + FastAPI + 20 questions.


---

### ✅ Part III cheat card — which classifier?
| Model | Strength | Weakness | Needs scaling? | Non-linear? | Explainable? | Speed (train / predict) |
|---|---|---|---|---|---|---|
| Logistic regression | fast, calibrated, baseline | linear boundary | yes | no | high | fast / fast |
| KNN | no training, simple | slow predict, curse of dimensionality | **yes** | yes | medium | none / slow |
| Naive Bayes | tiny data, text | independence assumption | no | no | high | fast / fast |
| LDA / QDA | small data, Gaussian classes | assumes Gaussian | helps | QDA yes | medium | fast / fast |
| SVM (RBF) | strong on small / medium data | slow on big data, needs tuning | **yes** | yes | low | slow / medium |
| Decision tree | explainable, no scaling | overfits | no | yes | **high** | fast / fast |
| Random Forest | robust, few settings | big, slower | no | yes | medium | medium / medium |
| Extra Trees | faster, lower variance | slightly more bias | no | yes | medium | fast / medium |
| Gradient boosting (XGB / LGBM / Cat) | **best on tables** | many settings, can overfit | no | yes | medium | medium / fast |
| Stacking | squeezes last %, mixes strengths | complex, slow | depends | yes | low | slow / slow |

### ✅ Part III cheat card — classification metrics
| Situation | Metric |
|---|---|
| Balanced, all errors cost the same | Accuracy, F1 |
| Rare positives (fraud, attrition) | **PR-AUC**, recall at a precision target |
| You need good probabilities | Log loss, Brier score, calibration curve |
| Ranking quality | ROC-AUC |
| Many classes | macro-F1 (rare classes matter) or weighted-F1 |

[📖 Table of contents](README.md) · [← previous part](part2_supervised_regression.md) · [next part →](part4_unsupervised.md) · [Appendices](appendix.md)
