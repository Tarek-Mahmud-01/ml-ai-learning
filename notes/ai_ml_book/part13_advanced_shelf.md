# PART XIII — Advanced Shelf ☆ (optional, Days 121–180)

[📖 Table of contents](README.md) · [← previous part](part12_design_interview_capstone.md) · [Appendices](appendix.md)

> **Category: the extra algorithms and skills that separate a good AI engineer from the best one · Level 3 (advanced)**
> The core book (Days 1–120) already makes you job-ready. This shelf adds **60 more algorithms and skills** — everything your roadmap docs did not list, plus what top teams expect.
> **Same 7-line template every day** (idea · equation · build · measure · improve · interview · done-when). Start any shelf day once its prerequisite Part is finished; you do not need to follow the order.
> **Marked ☆ = optional shelf.** ★ = core.


---

## Chapter S1 — Classical and statistical machine learning (Days 121–133)

> Robust / quantile regression, GLMs and GAMs, Bayesian regression, Gaussian processes, kernel methods, ordinal / multi-label / cost-sensitive classification, conformal prediction, survival analysis, semi-supervised and active learning, online learning, HMM / Kalman, MCMC / VI, Bayesian networks and causal graphs.

### Level 3 — Advanced

<a id="day-121"></a>
#### ☐ Day 121 — Robust & quantile regression ☆
- 🧠 **Idea · L1:** OLS is pulled by outliers. **Robust** regression down-weights them (Huber, RANSAC, Theil–Sen). **Quantile** regression predicts a percentile (e.g. the 90th) instead of the mean → prediction intervals.
- ➗ **Equation · L1:** Huber `ρ(e) = ½e²` if `|e| ≤ δ` else `δ(|e| − ½δ)` · pinball loss `ρτ(e) = max(τe, (τ−1)e)`
- ⌨️ **Build · L2:** `HuberRegressor`, `RANSACRegressor`, `TheilSenRegressor`, `QuantileRegressor`; add 5 % outliers to the sales data; fit the 10th / 50th / 90th percentile.
- 📊 **Measure · L2:** coefficient shift caused by outliers; coverage of the 10–90 interval (should be ≈ 80 %).
- 📈 **Improve · L3:** OLS → Huber → RANSAC; mean forecast → quantile interval.
- 🎤 **Interview · L3:** When use robust regression? · What is the pinball loss? · Mean vs median regression?
- ✅ **Done when:** an interval with ≈ 80 % real coverage.

<a id="day-122"></a>
#### ☐ Day 122 — Generalized linear models (GLM) and GAMs ☆
- 🧠 **Idea · L1:** targets that are counts or always positive (claims, orders, days absent) are not Normal. A **GLM** = linear score + a *link* function + the right distribution (Poisson, Gamma, Tweedie). A **GAM** replaces each `wⱼxⱼ` by a smooth curve.
- ➗ **Equation · L1:** `g(E[y]) = Xw` · Poisson: `log μ = Xw`, `P(y) = e^(−μ) μ^y / y!` · GAM: `g(E[y]) = Σ fⱼ(xⱼ)` (splines)
- ⌨️ **Build · L2:** `statsmodels` GLM Poisson on a count target (orders per day); `PoissonRegressor`, `GammaRegressor`; a GAM with `pygam`.
- 📊 **Measure · L2:** deviance, over-dispersion check, residual plots.
- 📈 **Improve · L3:** linear regression → Poisson GLM → GAM for non-linear effects.
- 🎤 **Interview · L3:** What is a link function? · Why not OLS on counts? · GLM vs GAM?
- ✅ **Done when:** a Poisson model beats OLS on a count target.

<a id="day-123"></a>
#### ☐ Day 123 — Bayesian linear regression (MLE vs MAP vs full Bayes) ☆
- 🧠 **Idea · L1:** instead of one best `w`, keep a **distribution** over `w`. A prior on `w` = regularization (Ridge = Gaussian prior). Uncertainty comes for free.
- ➗ **Equation · L1:** posterior `p(w|D) ∝ p(D|w)·p(w)` · MAP `ŵ = argmax [log p(D|w) + log p(w)]` · Gaussian prior ⇒ Ridge with `λ = σ²/τ²`
- ⌨️ **Build · L2:** conjugate Bayesian regression in NumPy; `BayesianRidge`; plot sampled lines from the posterior; compare with Ridge.
- 📊 **Measure · L2:** predictive uncertainty grows away from the data.
- 📈 **Improve · L3:** OLS → Ridge (MAP) → Bayesian posterior with intervals.
- 🎤 **Interview · L3:** MLE vs MAP vs full Bayes? · Why is Ridge a Bayesian model? · What is a conjugate prior?
- ✅ **Done when:** you can show Ridge = MAP on paper.

<a id="day-124"></a>
#### ☐ Day 124 — Gaussian processes ☆
- 🧠 **Idea · L1:** a distribution over *functions*. Give it data and it returns a prediction **and** an error bar. Great on small data and for Bayesian optimization.
- ➗ **Equation · L1:** kernel `k(x,x′) = σ² exp(−‖x−x′‖²/(2ℓ²))` · mean `μ* = K*ᵀ(K+σₙ²I)⁻¹y` · variance `σ*² = k** − K*ᵀ(K+σₙ²I)⁻¹K*`
- ⌨️ **Build · L2:** GP regression from scratch (50 points); `GaussianProcessRegressor` with RBF + noise kernels; plot mean ± 2σ.
- 📊 **Measure · L2:** log marginal likelihood; effect of length-scale ℓ; cost `O(n³)`.
- 📈 **Improve · L3:** fixed kernel → learned hyper-parameters → better kernel (periodic × RBF).
- 🎤 **Interview · L3:** What does a GP give you that a neural net does not? · Why `O(n³)`? · Role of the kernel?
- ✅ **Done when:** a GP fit with believable error bars.

<a id="day-125"></a>
#### ☐ Day 125 — Kernel ridge regression and kernel PCA ☆
- 🧠 **Idea · L1:** the **kernel trick**: work with similarities `k(x,x′)` and never build the huge feature space. Use it to bend ridge regression and PCA.
- ➗ **Equation · L1:** kernel ridge `α = (K + λI)⁻¹y`, `ŷ(x) = Σ αᵢk(xᵢ,x)` · kernel PCA = eigenvectors of the centred kernel matrix
- ⌨️ **Build · L2:** `KernelRidge` (RBF) vs Ridge on a curved target; `KernelPCA` on `make_circles`.
- 📊 **Measure · L2:** CV error vs `γ`, `λ`; PCA fails on circles, kernel PCA separates them.
- 📈 **Improve · L3:** linear → polynomial kernel → RBF kernel (tuned).
- 🎤 **Interview · L3:** What is the kernel trick? · Kernel ridge vs SVR vs GP? · Cost for large n?
- ✅ **Done when:** you can separate two circles with kernel PCA.

<a id="day-126"></a>
#### ☐ Day 126 — Ordinal, multi-label and cost-sensitive classification ☆
- 🧠 **Idea · L1:** not every label problem is "one of K". **Ordinal** (low < medium < high), **multi-label** (many tags at once), **cost-sensitive** (a miss costs more than a false alarm).
- ➗ **Equation · L1:** ordinal cumulative logits `P(y ≤ k) = σ(θₖ − w·x)` · multi-label = K binary heads · expected cost `Σ C(ŷ,y)·P(y|x)`
- ⌨️ **Build · L2:** ordinal logistic (`mord` or `statsmodels`), `MultiOutputClassifier`, classifier chains; cost matrix → decision rule.
- 📊 **Measure · L2:** Hamming loss, subset accuracy, per-label F1; expected cost.
- 📈 **Improve · L3:** plain multi-class → ordinal → cost-aware threshold.
- 🎤 **Interview · L3:** Multi-class vs multi-label? · How to handle ordered categories? · How do you use a cost matrix?
- ✅ **Done when:** you can pick the right formulation for 5 problems.

<a id="day-127"></a>
#### ☐ Day 127 — Conformal prediction: honest uncertainty ☆
- 🧠 **Idea · L1:** wrap *any* model so it outputs a **set / interval that is right ≥ 90 % of the time**, with no distribution assumptions.
- ➗ **Equation · L1:** nonconformity score `sᵢ = |yᵢ − ŷᵢ|` on a calibration set · `q̂ =` the `⌈(n+1)(1−α)⌉/n` quantile · interval `[ŷ − q̂, ŷ + q̂]`
- ⌨️ **Build · L2:** split-conformal intervals around a RandomForest; conformal sets for a classifier (`MAPIE`).
- 📊 **Measure · L2:** empirical coverage vs target 90 %; interval width.
- 📈 **Improve · L3:** fixed ± band → adaptive (normalised) intervals.
- 🎤 **Interview · L3:** Conformal vs Bayesian intervals? · Why a calibration set? · What does "valid coverage" mean?
- ✅ **Done when:** coverage ≈ 90 % on a test set.

<a id="day-128"></a>
#### ☐ Day 128 — Survival analysis (employee attrition, churn) ☆
- 🧠 **Idea · L1:** predict **how long until** an event (leaving, failing), when some people have not had the event yet (**censoring**).
- ➗ **Equation · L1:** Kaplan–Meier `S(t) = Π (1 − dᵢ/nᵢ)` · hazard `h(t)` · Cox model `h(t|x) = h₀(t)·exp(w·x)`
- ⌨️ **Build · L2:** `lifelines`: Kaplan–Meier curves by department, Cox PH fit on HR data, check proportional hazards.
- 📊 **Measure · L2:** concordance index (C-index); curves per group; hazard ratios.
- 📈 **Improve · L3:** logistic "left yes/no" → survival model that uses time.
- 🎤 **Interview · L3:** What is censoring? · Hazard ratio? · Why not plain regression on duration?
- ✅ **Done when:** a hazard-ratio table you can explain to HR.

<a id="day-129"></a>
#### ☐ Day 129 — Semi-supervised and active learning ☆
- 🧠 **Idea · L1:** labels are expensive. **Semi-supervised** uses unlabeled data too (self-training, label propagation, consistency). **Active learning** picks the *most useful* rows to label next.
- ➗ **Equation · L1:** uncertainty sampling `x* = argmax H(p(y|x))` · self-training: add predictions with `p > τ` as pseudo-labels
- ⌨️ **Build · L2:** `SelfTrainingClassifier`, `LabelSpreading`; an active-learning loop vs random labelling on `digits`.
- 📊 **Measure · L2:** accuracy vs number of labels (learning curve for both strategies).
- 📈 **Improve · L3:** random labelling → uncertainty sampling → diversity + uncertainty.
- 🎤 **Interview · L3:** What is pseudo-labelling and its risk? · Active vs semi-supervised? · When does it not help?
- ✅ **Done when:** active learning matches full accuracy with ≤ 30 % of labels.

<a id="day-130"></a>
#### ☐ Day 130 — Online / streaming learning and concept drift ☆
- 🧠 **Idea · L1:** data arrives one row at a time; the model learns **incrementally** and must adapt when the world changes.
- ➗ **Equation · L1:** online SGD `w ← w − η∇L(w; xₜ, yₜ)` · Passive-Aggressive update · drift detector ADWIN / Page–Hinkley
- ⌨️ **Build · L2:** `SGDClassifier.partial_fit`; `river` pipeline with a drift detector on a stream with a sudden shift.
- 📊 **Measure · L2:** prequential (test-then-train) accuracy over time; recovery time after drift.
- 📈 **Improve · L3:** static model → online model → online + drift reset.
- 🎤 **Interview · L3:** Batch vs online learning? · Types of drift? · How do you evaluate a stream?
- ✅ **Done when:** a plot showing the drop and recovery after drift.

<a id="day-131"></a>
#### ☐ Day 131 — Hidden Markov models and Kalman filters ☆
- 🧠 **Idea · L1:** a hidden state evolves in time and you only see noisy signals. **HMM** = discrete states (speech, POS tags, regimes). **Kalman filter** = continuous states (tracking, sensor smoothing).
- ➗ **Equation · L1:** HMM forward `αₜ(j) = Σᵢ αₜ₋₁(i)aᵢⱼ·bⱼ(oₜ)` · Viterbi = best path · Kalman: predict `x⁻ = Fx`, update `x = x⁻ + K(z − Hx⁻)`
- ⌨️ **Build · L2:** a 2-state HMM from scratch (forward + Viterbi); `hmmlearn`; a 1-D Kalman filter that smooths a noisy sensor.
- 📊 **Measure · L2:** state-decoding accuracy; filtered vs raw error.
- 📈 **Improve · L3:** moving average → Kalman filter.
- 🎤 **Interview · L3:** HMM vs RNN? · What does the Kalman gain do? · Forward vs Viterbi?
- ✅ **Done when:** a decoded state sequence you can explain.

<a id="day-132"></a>
#### ☐ Day 132 — MCMC and variational inference ☆
- 🧠 **Idea · L1:** when the posterior cannot be solved by hand: **sample** it (MCMC) or **approximate** it with a simpler distribution (VI). VI's objective (ELBO) is exactly the VAE loss you meet later.
- ➗ **Equation · L1:** Metropolis acceptance `min(1, p(x′)/p(x))` · `ELBO = E_q[log p(x,z)] − E_q[log q(z)]` · `log p(x) = ELBO + KL(q‖p)`
- ⌨️ **Build · L2:** Metropolis–Hastings from scratch for a coin bias; `PyMC` (NUTS) for Bayesian logistic regression; compare with MAP.
- 📊 **Measure · L2:** trace plots, effective sample size, R-hat.
- 📈 **Improve · L3:** short chain → burn-in + thinning → NUTS.
- 🎤 **Interview · L3:** Why MCMC? · MCMC vs VI? · What is the ELBO?
- ✅ **Done when:** posterior histogram that matches the analytic answer.

<a id="day-133"></a>
#### ☐ Day 133 — Bayesian networks, causal graphs and uplift ☆
- 🧠 **Idea · L1:** draw causes as a graph (**DAG**). The graph tells you what to adjust for. **Uplift modelling** predicts *who is changed by* a treatment, not who will buy anyway.
- ➗ **Equation · L1:** factorization `P(X) = Π P(Xᵢ|parents)` · backdoor adjustment `P(y|do(t)) = Σ_z P(y|t,z)P(z)` · uplift `τ(x) = P(y|x,T=1) − P(y|x,T=0)`
- ⌨️ **Build · L2:** a small Bayesian network (`pgmpy`); estimate a treatment effect with and without adjusting for a confounder; two-model uplift (T-learner).
- 📊 **Measure · L2:** bias before vs after adjustment; Qini / uplift curve.
- 📈 **Improve · L3:** naive difference → adjusted → T-learner / causal forest idea.
- 🎤 **Interview · L3:** What is a confounder / collider? · do-operator in one sentence? · Uplift vs response model?
- ✅ **Done when:** you can draw the DAG for a real HR question.


---

## Chapter S2 — Unsupervised learning and optimization (Days 134–140)

> More clustering, NMF / ICA / manifolds, association rules, autoencoder anomaly detection, more time series, the optimization toolbox, AutoML and feature stores.

### Level 3 — Advanced

<a id="day-134"></a>
#### ☐ Day 134 — More clustering: spectral, mean-shift, OPTICS/HDBSCAN, BIRCH, k-medoids ☆
- 🧠 **Idea · L1:** clustering families beyond K-Means: graph-based (spectral), density-peak (mean-shift), variable-density (OPTICS/HDBSCAN), streaming (BIRCH), robust centres (k-medoids).
- ➗ **Equation · L1:** graph Laplacian `L = D − W` (cluster with its smallest eigenvectors) · mean-shift `x ← Σ K(x−xᵢ)xᵢ / Σ K(x−xᵢ)` · k-medoids picks real points as centres
- ⌨️ **Build · L2:** run all six on `moons`, `circles`, blobs with different densities; `hdbscan`.
- 📊 **Measure · L2:** silhouette, adjusted Rand index, run time.
- 📈 **Improve · L3:** K-Means → DBSCAN → HDBSCAN on variable-density data.
- 🎤 **Interview · L3:** When does spectral clustering win? · DBSCAN vs HDBSCAN? · Why medoids?
- ✅ **Done when:** a "which clustering method" decision table from your results.

<a id="day-135"></a>
#### ☐ Day 135 — Matrix factorization and manifolds: NMF, ICA, LSA, Isomap, LLE, MDS ☆
- 🧠 **Idea · L1:** more ways to find structure. **NMF** (parts-based, non-negative), **ICA** (independent sources), **LSA** (SVD on text), **Isomap / LLE / MDS** (unroll curved data using neighbours).
- ➗ **Equation · L1:** NMF `X ≈ WH`, `W,H ≥ 0` · ICA maximizes non-Gaussianity · LSA `X ≈ U_kΣ_kV_kᵀ` · Isomap = MDS on geodesic distances
- ⌨️ **Build · L2:** NMF topics on a text set; ICA un-mixing two audio signals; LSA search; Isomap on the Swiss roll.
- 📊 **Measure · L2:** reconstruction error; interpretability of components.
- 📈 **Improve · L3:** PCA → NMF (topics) → manifold method on curved data.
- 🎤 **Interview · L3:** PCA vs ICA vs NMF? · Why a manifold method? · What is the cocktail-party problem?
- ✅ **Done when:** an unrolled Swiss roll.

<a id="day-136"></a>
#### ☐ Day 136 — Association rules: Apriori and FP-Growth ☆
- 🧠 **Idea · L1:** "customers who buy A also buy B" (market basket). Use it on your **sales data**.
- ➗ **Equation · L1:** support `P(A∩B)` · confidence `P(B|A)` · lift `P(B|A)/P(B)` (> 1 = real link)
- ⌨️ **Build · L2:** Apriori from scratch on 20 baskets; `mlxtend` Apriori + FP-Growth on the sales table; filter by lift.
- 📊 **Measure · L2:** number of rules vs support threshold; top rules by lift.
- 📈 **Improve · L3:** raw rules → support / confidence filter → lift filter → business sense check.
- 🎤 **Interview · L3:** Support, confidence, lift? · Why is FP-Growth faster? · Why is high confidence not enough?
- ✅ **Done when:** 5 rules a manager could act on.

<a id="day-137"></a>
#### ☐ Day 137 — Autoencoders and one-class anomaly detection ☆
- 🧠 **Idea · L1:** an **autoencoder** squeezes data through a bottleneck and rebuilds it; rows it rebuilds badly are anomalies. **One-Class SVM** draws a boundary around "normal".
- ➗ **Equation · L1:** reconstruction error `‖x − x̂‖²` · One-Class SVM `min ½‖w‖² + (1/νn)Σξᵢ − ρ`
- ⌨️ **Build · L2:** PyTorch autoencoder on HRM payslips; `OneClassSVM`, `EllipticEnvelope`; compare with Isolation Forest (Day 39).
- 📊 **Measure · L2:** precision@k on injected anomalies.
- 📈 **Improve · L3:** Isolation Forest → autoencoder → ensemble of detectors.
- 🎤 **Interview · L3:** Why does an autoencoder detect anomalies? · Bottleneck size? · Detector ensembles?
- ✅ **Done when:** a table of 4 detectors on the same payslip data.

<a id="day-138"></a>
#### ☐ Day 138 — More time series: Holt-Winters, SARIMAX, VAR, state-space, foundation models ☆
- 🧠 **Idea · L1:** more forecasters. **Exponential smoothing** (level, trend, season), **SARIMAX** (with outside variables), **VAR** (several series that affect each other), **state-space** models, and pretrained **time-series foundation models** (zero-shot forecasting).
- ➗ **Equation · L1:** simple smoothing `ℓₜ = αyₜ + (1−α)ℓₜ₋₁` · Holt-Winters adds trend `bₜ` and season `sₜ` · VAR `yₜ = c + A₁yₜ₋₁ + εₜ`
- ⌨️ **Build · L2:** `ExponentialSmoothing`, `SARIMAX` with a holiday variable, `VAR`; a pretrained TS model (e.g. Chronos / TimesFM) zero-shot on your sales series.
- 📊 **Measure · L2:** backtest sMAPE for all; the best model per series.
- 📈 **Improve · L3:** one global model → per-series best → ensemble.
- 🎤 **Interview · L3:** ETS vs ARIMA? · When use VAR? · Are foundation models good for forecasting?
- ✅ **Done when:** a model-comparison table with a backtest.

<a id="day-139"></a>
#### ☐ Day 139 — Optimization toolbox ☆
- 🧠 **Idea · L1:** the maths of "find the best". **Convex** problems have one bottom. **Newton / L-BFGS** use curvature. **Lagrange / KKT** handle constraints (this is how SVM is solved). **Simulated annealing** escapes local minima.
- ➗ **Equation · L1:** Newton `w ← w − H⁻¹∇J` · Lagrangian `L(w,λ) = f(w) + λg(w)` · annealing accepts a worse move with probability `exp(−Δ/T)`
- ⌨️ **Build · L2:** Newton vs GD on logistic regression; `scipy.optimize` (L-BFGS, SLSQP); a constrained problem with Lagrange multipliers; simulated annealing on a toy puzzle.
- 📊 **Measure · L2:** iterations to converge; sensitivity to start point.
- 📈 **Improve · L3:** GD → momentum → Newton / L-BFGS.
- 🎤 **Interview · L3:** Why not Newton for deep nets? · What is a convex function? · What do KKT conditions say?
- ✅ **Done when:** you can explain why second-order methods are rare in deep learning.

<a id="day-140"></a>
#### ☐ Day 140 — AutoML and feature stores ☆
- 🧠 **Idea · L1:** let tools search models for you (AutoML) but understand what they do; share features between training and serving with a **feature store**.
- ➗ **Equation · L1:** none — search budget `trials × time/trial`; point-in-time correct joins prevent leakage.
- ⌨️ **Build · L2:** `FLAML` / `AutoGluon` on a tabular task vs your hand-built V4; a small `Feast` feature store; `Great Expectations` data checks.
- 📊 **Measure · L2:** score and time for AutoML vs your model.
- 📈 **Improve · L3:** AutoML baseline → your features + AutoML → ensemble.
- 🎤 **Interview · L3:** When is AutoML enough? · What is training–serving skew? · Why point-in-time joins?
- ✅ **Done when:** you can say where AutoML helps and where you still need engineering.


---

## Chapter S3 — Deep-learning extensions (Days 141–149)

> CNN architectures, VAE and contrastive learning, detection / segmentation, GANs, diffusion, graph neural networks, Mamba and Mixture-of-Experts, efficient models, training at scale.

### Level 3 — Advanced

<a id="day-141"></a>
#### ☐ Day 141 — CNN architectures in code: LeNet → ConvNeXt ☆
- 🧠 **Idea · L1:** read the history as ideas: depth (VGG), skip connections (ResNet), multi-scale (Inception), efficiency (MobileNet, EfficientNet), modernization (ConvNeXt).
- ➗ **Equation · L1:** depthwise-separable conv params `f²C_in + C_in·C_out` vs normal `f²C_in·C_out` · compound scaling `d=αᶲ, w=βᶲ, r=γᶲ`
- ⌨️ **Build · L2:** LeNet, a mini-VGG, a ResNet block, a depthwise-separable block in PyTorch; compare parameter counts with `torchvision` models.
- 📊 **Measure · L2:** accuracy / params / FLOPs / latency on CIFAR-10.
- 📈 **Improve · L3:** plain CNN → ResNet block → MobileNet block.
- 🎤 **Interview · L3:** Why do skip connections help? · What makes MobileNet cheap? · How are CNNs scaled?
- ✅ **Done when:** a table: model → params → accuracy → speed.

<a id="day-142"></a>
#### ☐ Day 142 — Autoencoders, VAEs and contrastive learning ☆
- 🧠 **Idea · L1:** learn representations **without labels**. VAE = autoencoder with a smooth latent space. **Contrastive** learning (SimCLR, CLIP, DINO) pulls together views of the same item and pushes others apart.
- ➗ **Equation · L1:** VAE `L = ‖x−x̂‖² + KL(q(z|x)‖N(0,I))` · reparametrization `z = μ + σ⊙ε` · InfoNCE `−log[exp(sim(zᵢ,zⱼ)/τ) / Σₖ exp(sim(zᵢ,zₖ)/τ)]`
- ⌨️ **Build · L2:** VAE on MNIST (sample new digits); a tiny SimCLR; CLIP zero-shot image classification.
- 📊 **Measure · L2:** reconstruction vs KL balance; linear-probe accuracy on learned features.
- 📈 **Improve · L3:** raw pixels → autoencoder features → contrastive features.
- 🎤 **Interview · L3:** Why the KL term? · What is the reparametrization trick? · How does CLIP link text and images?
- ✅ **Done when:** generated digits and a CLIP zero-shot demo.

<a id="day-143"></a>
#### ☐ Day 143 — Detection and segmentation deep dive ☆
- 🧠 **Idea · L1:** one-stage (YOLO), two-stage (Faster R-CNN), transformer (DETR) detectors; semantic (U-Net), instance (Mask R-CNN), promptable (SAM) segmentation.
- ➗ **Equation · L1:** IoU · GIoU · focal loss `−α(1−p)^γ log p` · Dice `2|A∩B|/(|A|+|B|)` · mAP@[.5:.95]
- ⌨️ **Build · L2:** fine-tune a YOLO model on a small custom set; U-Net on a toy segmentation set; SAM with point prompts.
- 📊 **Measure · L2:** mAP, per-class AP, Dice; error gallery (missed, duplicated, wrong class).
- 📈 **Improve · L3:** defaults → augmentation → larger input → tuned NMS threshold.
- 🎤 **Interview · L3:** One-stage vs two-stage? · Why focal loss? · What does NMS do?
- ✅ **Done when:** a detector fine-tuned on your own images.

<a id="day-144"></a>
#### ☐ Day 144 — The GAN family ☆
- 🧠 **Idea · L1:** a generator and a discriminator train against each other. Variants fix instability and add control: DCGAN, WGAN, StyleGAN, CycleGAN.
- ➗ **Equation · L1:** `min_G max_D E[log D(x)] + E[log(1−D(G(z)))]` · WGAN loss `E[D(x)] − E[D(G(z))]` with a Lipschitz constraint · cycle loss `‖F(G(x)) − x‖`
- ⌨️ **Build · L2:** DCGAN on MNIST / faces; WGAN-GP tweak; a CycleGAN demo (style translation).
- 📊 **Measure · L2:** FID score, mode collapse check, loss curves (they oscillate).
- 📈 **Improve · L3:** vanilla GAN → DCGAN → WGAN-GP.
- 🎤 **Interview · L3:** Why are GANs hard to train? · What is mode collapse? · GAN vs diffusion?
- ✅ **Done when:** a stable GAN run and a note on what you changed.

<a id="day-145"></a>
#### ☐ Day 145 — Diffusion models deep dive ☆
- 🧠 **Idea · L1:** add noise step by step; train a network to **predict the noise**; generate by removing noise. **Latent diffusion** does it in a compressed space; **ControlNet / LoRA / DreamBooth** add control and personalisation.
- ➗ **Equation · L1:** forward `x_t = √ᾱ_t·x₀ + √(1−ᾱ_t)·ε` · loss `E‖ε − ε_θ(x_t, t)‖²` · classifier-free guidance `ε̃ = ε(∅) + s·(ε(c) − ε(∅))`
- ⌨️ **Build · L2:** a tiny DDPM on MNIST; `diffusers` text-to-image, img2img, inpainting, super-resolution; a LoRA style fine-tune.
- 📊 **Measure · L2:** quality vs steps; effect of guidance scale; speed.
- 📈 **Improve · L3:** 1 000 steps → fewer-step sampler → latent model.
- 🎤 **Interview · L3:** Why predict noise? · What is guidance? · Diffusion vs GAN vs VAE?
- ✅ **Done when:** a tiny DDPM that draws digits.

<a id="day-146"></a>
#### ☐ Day 146 — Graph neural networks and knowledge graphs ☆
- 🧠 **Idea · L1:** data with links (people, transactions, molecules). A **GNN** lets each node gather messages from its neighbours.
- ➗ **Equation · L1:** GCN `H′ = σ(D̃^(−½) Ã D̃^(−½) H W)` · GraphSAGE aggregates neighbours · GAT weights neighbours by attention
- ⌨️ **Build · L2:** a GCN in PyTorch Geometric on Cora; node2vec embeddings; a small knowledge graph with `networkx` + a graph query.
- 📊 **Measure · L2:** node-classification accuracy; GNN vs MLP without edges.
- 📈 **Improve · L3:** MLP → GCN → GAT.
- 🎤 **Interview · L3:** What is message passing? · Over-smoothing? · Where are GNNs used (fraud, recommenders)?
- ✅ **Done when:** a GNN that beats an MLP on Cora.

<a id="day-147"></a>
#### ☐ Day 147 — State-space models (Mamba) and Mixture-of-Experts ☆
- 🧠 **Idea · L1:** attention is `O(n²)`. **State-space models** (S4, Mamba) read a sequence in `O(n)` with a smart hidden state. **Mixture-of-Experts** keeps many sub-networks but uses only a few per token.
- ➗ **Equation · L1:** SSM `hₜ = Āhₜ₋₁ + B̄xₜ`, `yₜ = Chₜ` · MoE `y = Σᵢ gᵢ(x)·Eᵢ(x)` with top-k gating + load-balancing loss
- ⌨️ **Build · L2:** a toy SSM scan; a small MoE layer in PyTorch with top-2 routing; read the Mamba and Switch-Transformer papers.
- 📊 **Measure · L2:** compute vs quality; expert load balance.
- 📈 **Improve · L3:** dense FFN → MoE with balancing loss.
- 🎤 **Interview · L3:** Why is attention quadratic? · How does MoE save compute? · When might an SSM beat a Transformer?
- ✅ **Done when:** a working top-2 MoE layer.

<a id="day-148"></a>
#### ☐ Day 148 — Efficient models: distillation, pruning, quantization ☆
- 🧠 **Idea · L1:** make models small and fast. **Distillation** (student copies teacher), **pruning** (remove weights), **quantization** (INT8 / 4-bit), export to **ONNX / TensorRT**.
- ➗ **Equation · L1:** distillation `L = α·CE(y,p_s) + (1−α)·T²·KL(p_t^T ‖ p_s^T)` · quantization `q = round(x/s) + z`
- ⌨️ **Build · L2:** distill a small MLP / DistilBERT; post-training INT8 quantization; export to ONNX and run with `onnxruntime`.
- 📊 **Measure · L2:** accuracy drop vs size vs latency.
- 📈 **Improve · L3:** FP32 → FP16 → INT8 → distilled + INT8.
- 🎤 **Interview · L3:** Distillation vs pruning vs quantization? · What is calibration for quantization? · Why ONNX?
- ✅ **Done when:** a model 4× smaller within 1 % accuracy.

<a id="day-149"></a>
#### ☐ Day 149 — Training at scale: GPUs, mixed precision, distributed training ☆
- 🧠 **Idea · L1:** big models need many GPUs. **Mixed precision** saves memory, **DDP** copies the model on each GPU, **FSDP / DeepSpeed ZeRO** shards it, **gradient checkpointing** trades compute for memory.
- ➗ **Equation · L1:** memory ≈ `params × (weights + grads + optimizer states)` ≈ `16 bytes/param` for Adam in mixed precision · effective batch `= micro_batch × accumulation × GPUs`
- ⌨️ **Build · L2:** `torch.autocast` + `GradScaler`; gradient accumulation; a 2-process DDP toy on CPU/GPU; read the FSDP docs; memory estimate for a 7 B model.
- 📊 **Measure · L2:** memory and speed with/without AMP; throughput scaling.
- 📈 **Improve · L3:** FP32 → AMP → + gradient checkpointing → + accumulation.
- 🎤 **Interview · L3:** DDP vs FSDP? · Why does Adam need so much memory? · What is gradient accumulation?
- ✅ **Done when:** you can estimate GPU memory for a model on paper.


---

## Chapter S4 — NLP and LLM extensions (Days 150–159)

> Classic NLP models, encoder family, tokenizers, LLM internals, PEFT variants, alignment and reasoning models, advanced RAG, benchmarks and judges, long context and caching, vision-language and speech.

### Level 3 — Advanced

<a id="day-150"></a>
#### ☐ Day 150 — Classic NLP models: n-gram LMs, CRF, HMM-POS, LDA topics, TextRank ☆
- 🧠 **Idea · L1:** the models before deep learning still teach a lot. **n-gram LM** (next word from counts), **CRF / HMM** (sequence labelling), **LDA** (Latent Dirichlet Allocation — topics), **TextRank** (keywords).
- ➗ **Equation · L1:** bigram `P(wₜ|wₜ₋₁) = count(wₜ₋₁wₜ)/count(wₜ₋₁)` · perplexity · LDA: document = mix of topics, topic = mix of words
- ⌨️ **Build · L2:** a bigram LM with smoothing; HMM POS tagger; `sklearn-crfsuite` NER; `gensim` LDA on HR complaints; TextRank keywords.
- 📊 **Measure · L2:** perplexity; tagging accuracy; topic coherence.
- 📈 **Improve · L3:** unigram → bigram + smoothing → trigram.
- 🎤 **Interview · L3:** What is perplexity? · CRF vs HMM? · How does LDA work (intuition)?
- ✅ **Done when:** readable topics from your own text.

<a id="day-151"></a>
#### ☐ Day 151 — The encoder family: RoBERTa, DeBERTa, sentence-transformers, ColBERT ☆
- 🧠 **Idea · L1:** better encoders and **embedding models** for search: RoBERTa (better pre-training), DeBERTa (disentangled attention), **sentence-transformers** (bi-encoders), **cross-encoders** (rerankers), **ColBERT** (late interaction).
- ➗ **Equation · L1:** bi-encoder score `cos(f(q), f(d))` · cross-encoder `score(q,d) = g([q;d])` · ColBERT `Σᵢ maxⱼ qᵢ·dⱼ`
- ⌨️ **Build · L2:** fine-tune a sentence-transformer with contrastive loss on HR Q&A pairs; add a cross-encoder reranker; compare recall@k.
- 📊 **Measure · L2:** recall@k, MRR, latency.
- 📈 **Improve · L3:** off-the-shelf embeddings → fine-tuned → + reranker.
- 🎤 **Interview · L3:** Bi-encoder vs cross-encoder? · Why is ColBERT accurate and still fast? · Hard negatives?
- ✅ **Done when:** recall@5 improves with a fine-tuned embedder.

<a id="day-152"></a>
#### ☐ Day 152 — Tokenizers deep dive ☆
- 🧠 **Idea · L1:** the tokenizer decides cost, speed and many LLM quirks. **BPE**, **WordPiece**, **Unigram**, **SentencePiece**, **byte-level** tokenizers.
- ➗ **Equation · L1:** BPE merges the most frequent pair · Unigram LM maximizes `Σ log P(token sequence)` · fertility `= tokens/words`
- ⌨️ **Build · L2:** train a BPE and a Unigram tokenizer with `tokenizers` / `sentencepiece` on your HR text; compare vocab sizes.
- 📊 **Measure · L2:** tokens per word for English vs another language; numbers and code handling.
- 📈 **Improve · L3:** char-level → BPE 8k → BPE 32k.
- 🎤 **Interview · L3:** Why subwords? · Why do LLMs struggle with spelling / counting letters? · Token cost across languages?
- ✅ **Done when:** a tokenizer you trained and a table of fertility.

<a id="day-153"></a>
#### ☐ Day 153 — LLM internals: RoPE, GQA, FlashAttention, KV-cache, speculative decoding ☆
- 🧠 **Idea · L1:** what makes modern LLMs fast and long-context. **RoPE** (rotary positions), **MQA / GQA** (share K,V heads), **FlashAttention** (tiled, no huge matrix), **KV-cache**, **speculative decoding** (small model drafts, big model verifies).
- ➗ **Equation · L1:** RoPE rotates `(q,k)` pairs by angle `m·θᵢ` · KV-cache memory `= 2 × layers × heads × d × seq × bytes` · speculative speed-up `≈ accepted tokens per verify`
- ⌨️ **Build · L2:** add RoPE and a KV-cache to your tiny GPT (Day 78–79); measure generation speed with and without cache; compute KV-cache size for a 7 B model.
- 📊 **Measure · L2:** tokens/second; memory vs context length.
- 📈 **Improve · L3:** no cache → KV-cache → GQA.
- 🎤 **Interview · L3:** Why does the KV-cache help? · What does GQA change? · How does FlashAttention save memory?
- ✅ **Done when:** your tiny GPT generates faster with a cache.

<a id="day-154"></a>
#### ☐ Day 154 — Parameter-efficient fine-tuning variants ☆
- 🧠 **Idea · L1:** more ways than LoRA: **prompt / prefix tuning** (learn soft prompts), **adapters**, **DoRA**, **QLoRA** details (NF4, double quantization, paged optimizers), **model merging**.
- ➗ **Equation · L1:** LoRA `W′ = W + (α/r)BA` · DoRA = magnitude × direction · prefix tuning prepends learnable vectors `P_k, P_v`
- ⌨️ **Build · L2:** compare LoRA, prefix tuning and an adapter on the same small task with `peft`; QLoRA run; merge two adapters.
- 📊 **Measure · L2:** accuracy, trainable params, memory, speed.
- 📈 **Improve · L3:** r = 4 → 16; target modules (attention only → all linear).
- 🎤 **Interview · L3:** LoRA vs adapters vs prefix tuning? · What is NF4? · Which layers to adapt?
- ✅ **Done when:** a comparison table of 3 PEFT methods.

<a id="day-155"></a>
#### ☐ Day 155 — Alignment methods and reasoning models ☆
- 🧠 **Idea · L1:** after SFT: **RLHF**, **DPO**, **KTO**, **ORPO**, **GRPO**, **RLVR**, constitutional methods. **Reasoning models** spend more tokens "thinking" (test-time compute) and are trained with verifiable rewards.
- ➗ **Equation · L1:** DPO `L = −log σ(β[log π(y_w|x)/π_ref(y_w|x) − log π(y_l|x)/π_ref(y_l|x)])` · GRPO advantage `Aᵢ = (rᵢ − mean(r))/std(r)` within a group
- ⌨️ **Build · L2:** a tiny DPO run with `trl` on a preference set; a GRPO-style loop on arithmetic problems with a verifiable reward; best-of-N and self-consistency.
- 📊 **Measure · L2:** win-rate vs the SFT model; accuracy vs thinking budget.
- 📈 **Improve · L3:** SFT → DPO → verifiable-reward RL.
- 🎤 **Interview · L3:** RLHF vs DPO? · What is a verifiable reward? · Why does test-time compute help?
- ✅ **Done when:** you can explain the 2024–2026 post-training pipeline end to end.

<a id="day-156"></a>
#### ☐ Day 156 — Advanced RAG ☆
- 🧠 **Idea · L1:** beyond chunk-and-retrieve: **HyDE** (embed a hypothetical answer), **multi-vector / parent-child** chunks, **GraphRAG**, **self-RAG / CRAG** (the model decides when to retrieve and checks results), **agentic RAG**, structured / tabular RAG.
- ➗ **Equation · L1:** HyDE `q′ = embed(LLM(q))` · RRF · context precision / recall
- ⌨️ **Build · L2:** add HyDE, parent-document retrieval and a retrieval-grader to your Day-90 assistant; a small GraphRAG on policy documents.
- 📊 **Measure · L2:** recall@k, answer accuracy, cost per question vs the Day-90 version.
- 📈 **Improve · L3:** plain RAG → hybrid + rerank → HyDE → graph / agentic.
- 🎤 **Interview · L3:** When does GraphRAG help? · Self-RAG in one sentence? · How do you evaluate retrieval?
- ✅ **Done when:** measured gain from at least one advanced technique.

<a id="day-157"></a>
#### ☐ Day 157 — LLM benchmarks, judges and human evaluation ☆
- 🧠 **Idea · L1:** know the public benchmarks (MMLU, HumanEval, GSM8K, SWE-bench) *and their limits* (contamination, saturation). Build **your own** eval set. LLM-as-judge has biases; calibrate against humans.
- ➗ **Equation · L1:** pass@k `= 1 − C(n−c, k)/C(n, k)` · Cohen's κ for judge–human agreement · win-rate with confidence interval
- ⌨️ **Build · L2:** run a small open model on a benchmark subset; build a 50-case eval for HR Q&A; a pairwise judge with position-swap; compute κ vs 20 human labels.
- 📊 **Measure · L2:** judge bias (position, length); agreement with humans.
- 📈 **Improve · L3:** single judge → swapped + rubric → human spot-check.
- 🎤 **Interview · L3:** What is data contamination? · Limits of LLM-as-judge? · pass@k?
- ✅ **Done when:** an eval harness you trust.

<a id="day-158"></a>
#### ☐ Day 158 — Long context, memory and caching ☆
- 🧠 **Idea · L1:** long context is not free. Compare **long-context stuffing vs retrieval**; use **prompt caching**, context **compression** and summarization; know "lost in the middle".
- ➗ **Equation · L1:** cost with cache `= miss_cost + hits × (hit_price)` · attention cost `O(n²)` · needle-in-a-haystack recall vs position
- ⌨️ **Build · L2:** a needle-in-a-haystack test at several lengths; prompt caching on a long policy document; map-reduce summarization.
- 📊 **Measure · L2:** accuracy vs position; cost and latency with/without caching.
- 📈 **Improve · L3:** stuff everything → retrieve → retrieve + cache.
- 🎤 **Interview · L3:** Long context vs RAG? · What is prompt caching? · Lost-in-the-middle?
- ✅ **Done when:** a decision rule "RAG vs long context" with numbers.

<a id="day-159"></a>
#### ☐ Day 159 — Vision-language models and speech ☆
- 🧠 **Idea · L1:** models that see and hear: **VLMs** (image encoder + LLM), **Whisper** (speech → text), **TTS**, **voice agents** (ASR → LLM → TTS with low latency).
- ➗ **Equation · L1:** word error rate `WER = (S + D + I)/N` · mel-spectrogram · VLM = `LLM([image tokens; text tokens])`
- ⌨️ **Build · L2:** ask a VLM about a payslip image / chart; Whisper transcription of a meeting; a text-to-speech reply; a minimal voice loop.
- 📊 **Measure · L2:** WER, end-to-end latency, OCR/field-extraction accuracy.
- 📈 **Improve · L3:** OCR + LLM → VLM direct → VLM + validation rules.
- 🎤 **Interview · L3:** How does a VLM read an image? · What is WER? · Where does voice-agent latency come from?
- ✅ **Done when:** a voice question answered over your HR data.


---

## Chapter S5 — Reinforcement-learning and agent extensions (Days 160–166)

> Bandits, the deep-RL family, model-based / offline / multi-agent RL, agent reasoning patterns, code and computer-use agents, agent systems, agent security.

### Level 3 — Advanced

<a id="day-160"></a>
#### ☐ Day 160 — Bandits, Monte-Carlo and TD(λ) ☆
- 🧠 **Idea · L1:** the foundations under deep RL. **Bandits** (explore vs exploit), **Monte-Carlo** returns, **TD(λ)** (between MC and one-step TD).
- ➗ **Equation · L1:** UCB `a = argmax[Q(a) + c√(ln t / N(a))]` · Thompson: sample from the posterior · TD(0) `V(s) ← V(s) + α[r + γV(s′) − V(s)]`
- ⌨️ **Build · L2:** ε-greedy vs UCB vs Thompson on a 10-armed bandit; contextual bandit for choosing a notification; MC vs TD on a random walk.
- 📊 **Measure · L2:** cumulative regret; learning curves.
- 📈 **Improve · L3:** ε-greedy → UCB → Thompson sampling.
- 🎤 **Interview · L3:** Explore vs exploit? · UCB vs Thompson? · MC vs TD?
- ✅ **Done when:** a regret plot for 3 strategies.

<a id="day-161"></a>
#### ☐ Day 161 — The deep-RL family: Double/Dueling DQN, Rainbow, A2C, DDPG, TD3, SAC, TRPO ☆
- 🧠 **Idea · L1:** fix DQN's problems (over-estimation, sample waste) and handle continuous actions. **Actor-critic** methods learn a policy and a value together.
- ➗ **Equation · L1:** Double DQN target `r + γ Q_target(s′, argmax_a Q(s′,a))` · A2C advantage `A = r + γV(s′) − V(s)` · SAC objective `E[r + αH(π)]`
- ⌨️ **Build · L2:** Double + Dueling DQN on CartPole; A2C; `stable-baselines3` SAC / TD3 on a continuous task (Pendulum).
- 📊 **Measure · L2:** reward curves over 3 seeds.
- 📈 **Improve · L3:** DQN → Double → Dueling → prioritized replay.
- 🎤 **Interview · L3:** Why does DQN over-estimate? · Actor vs critic? · Why SAC is popular?
- ✅ **Done when:** a seed-averaged comparison plot.

<a id="day-162"></a>
#### ☐ Day 162 — Model-based, offline, imitation and multi-agent RL ☆
- 🧠 **Idea · L1:** learn a **model** of the world (Dyna, MuZero idea); learn from **logged data** only (offline RL); copy an expert (**imitation**, inverse RL); many agents at once (**MARL**).
- ➗ **Equation · L1:** behaviour cloning `min E‖π(s) − a_expert‖²` · conservative Q-learning penalty · Nash equilibrium idea
- ⌨️ **Build · L2:** behaviour cloning on logged CartPole data; a tiny Dyna-Q; a two-agent grid game.
- 📊 **Measure · L2:** return vs the expert; effect of dataset size and coverage.
- 📈 **Improve · L3:** behaviour cloning → DAgger idea → offline RL.
- 🎤 **Interview · L3:** Why is offline RL hard? · Imitation vs RL? · What is distribution shift?
- ✅ **Done when:** an agent trained only from logs.

<a id="day-163"></a>
#### ☐ Day 163 — Agent reasoning patterns: Reflexion, Tree-of-Thoughts, self-consistency ☆
- 🧠 **Idea · L1:** make agents think better: **self-consistency** (sample many, vote), **Tree-of-Thoughts / LATS** (search over thoughts), **Reflexion** (learn from a written critique), planner–critic.
- ➗ **Equation · L1:** self-consistency `ŷ = argmax Σ 1[yᵢ = c]` over N samples · ToT = beam / best-first search over partial thoughts
- ⌨️ **Build · L2:** self-consistency on 30 maths / logic questions; a small ToT for a puzzle; a Reflexion retry loop on failing code tasks.
- 📊 **Measure · L2:** accuracy vs number of samples; cost per task.
- 📈 **Improve · L3:** single answer → self-consistency → ToT / Reflexion.
- 🎤 **Interview · L3:** When does more thinking not help? · Self-consistency vs ToT? · How does Reflexion learn?
- ✅ **Done when:** an accuracy-vs-cost curve.

<a id="day-164"></a>
#### ☐ Day 164 — Code agents and computer-use agents ☆
- 🧠 **Idea · L1:** agents that write and run code, edit repositories (SWE-agent style) or operate a browser / desktop. **Sandboxing** is mandatory.
- ➗ **Equation · L1:** none — measure pass rate on a task suite; timeouts + resource limits.
- ⌨️ **Build · L2:** a code-interpreter agent in a Docker sandbox that analyses a CSV; a repo-fixing agent on 5 small bugs; a browser-use demo with strict allow-lists.
- 📊 **Measure · L2:** tasks solved, steps, cost, unsafe actions blocked.
- 📈 **Improve · L3:** one-shot code → run-and-fix loop → tests as feedback.
- 🎤 **Interview · L3:** How do you sandbox generated code? · What is SWE-bench? · Risks of computer-use?
- ✅ **Done when:** an agent that fixes 3 of 5 bugs safely.

<a id="day-165"></a>
#### ☐ Day 165 — Agent systems: A2A, supervisor / swarm, durable workflows ☆
- 🧠 **Idea · L1:** production agents are *systems*: **agent-to-agent (A2A)** protocols, **supervisor** and **swarm** patterns, **durable workflows** (Temporal / LangGraph persistence) that survive crashes and wait for humans.
- ➗ **Equation · L1:** none — reliability `= P(all steps succeed)`; retry with back-off; idempotency keys.
- ⌨️ **Build · L2:** a supervisor with 3 specialist agents; a workflow with persistence + human approval; a simple A2A message exchange between two services.
- 📊 **Measure · L2:** end-to-end success, recovery after a forced crash.
- 📈 **Improve · L3:** one big agent → supervisor + specialists → durable workflow.
- 🎤 **Interview · L3:** Supervisor vs swarm? · Why durable execution? · What goes wrong with long-running agents?
- ✅ **Done when:** a workflow that resumes after you kill the process.

<a id="day-166"></a>
#### ☐ Day 166 — Agent security: OWASP LLM Top-10 ☆
- 🧠 **Idea · L1:** know the attacks: **prompt injection** (direct and indirect), data exfiltration, insecure tool use, excessive agency, supply-chain risks, denial-of-wallet.
- ➗ **Equation · L1:** attack success rate `= successful attacks/attempts` · blast radius = what the agent's credentials can touch.
- ⌨️ **Build · L2:** a red-team suite of 30 attacks against your HR agent; least-privilege tools, output filtering, allow-lists, secrets isolation, human approval for writes.
- 📊 **Measure · L2:** attack success rate before / after defences.
- 📈 **Improve · L3:** no defence → input/output filters → least privilege + approval.
- 🎤 **Interview · L3:** What is indirect prompt injection? · How do you limit blast radius? · Why can't you fully "filter" injections?
- ✅ **Done when:** attack success drops below 5 % with a documented list.


---

## Chapter S6 — Engineering and career (Days 167–180)

> Data engineering, serving at scale, Python performance, privacy and responsible AI, advanced recommenders, search and learning-to-rank, papers, Kaggle, coding interviews, open source, system design II, behavioural interview and the final gap audit.

### Level 3 — Advanced

<a id="day-167"></a>
#### ☐ Day 167 — Data engineering: Kafka, Airflow/Prefect, dbt ☆
- 🧠 **Idea · L1:** pipelines feed models. **Batch** (Airflow / Prefect DAGs), **streaming** (Kafka), **transformations** (dbt), data contracts and quality checks.
- ➗ **Equation · L1:** throughput / lag `= produced − consumed` · idempotent loads.
- ⌨️ **Build · L2:** an Airflow (or Prefect) DAG: extract → validate → transform → load; a Kafka producer / consumer demo; a dbt model on the sales table.
- 📊 **Measure · L2:** run time, failure and retry behaviour, data-quality test results.
- 📈 **Improve · L3:** cron script → DAG with retries → + data tests.
- 🎤 **Interview · L3:** Batch vs streaming? · What is idempotency? · How do you test data?
- ✅ **Done when:** a scheduled pipeline with a failing-data alert.

<a id="day-168"></a>
#### ☐ Day 168 — Serving at scale: vLLM, Triton, Ray Serve, Kubernetes ☆
- 🧠 **Idea · L1:** serve many users cheaply. **Continuous batching** and **paged attention** (vLLM), model servers (**Triton**, **Ray Serve**, **BentoML**), **autoscaling** and **Kubernetes** (pod, deployment, service, HPA).
- ➗ **Equation · L1:** capacity `= GPUs × tokens/s ÷ tokens per request` · utilisation · cost per 1 M tokens
- ⌨️ **Build · L2:** serve a small open model with vLLM; load-test throughput vs batch size; deploy a FastAPI model on a local Kubernetes (kind/minikube) with 2 replicas.
- 📊 **Measure · L2:** tokens/s, p95 latency, cost per 1 M tokens.
- 📈 **Improve · L3:** one request at a time → continuous batching → quantized model.
- 🎤 **Interview · L3:** Why continuous batching? · What does a Kubernetes Deployment do? · How to scale on GPU load?
- ✅ **Done when:** a throughput-vs-latency chart.

<a id="day-169"></a>
#### ☐ Day 169 — Python performance for ML engineers ☆
- 🧠 **Idea · L1:** slow code is a bug. **Profile first**, then vectorize (NumPy), use the right data structures, cache, parallelize (`multiprocessing`, `joblib`), compile hot loops (Numba), and avoid copies.
- ➗ **Equation · L1:** Amdahl `speedup ≤ 1/((1−p)+p/N)` · big-O of the operations you use.
- ⌨️ **Build · L2:** `cProfile` / `line_profiler` on your feature pipeline; loop → NumPy; Numba on a distance function; `joblib` parallel CV; memory with `tracemalloc`.
- 📊 **Measure · L2:** time and memory before / after each change.
- 📈 **Improve · L3:** loops → vectorized → Numba / parallel.
- 🎤 **Interview · L3:** How do you find the bottleneck? · Why is NumPy fast? · GIL and multiprocessing?
- ✅ **Done when:** a 10× speed-up with evidence.

<a id="day-170"></a>
#### ☐ Day 170 — Privacy and responsible AI ☆
- 🧠 **Idea · L1:** HR data is sensitive. Know **differential privacy**, **federated learning**, PII handling, **fairness metrics**, model cards / datasheets, and the rules (GDPR, EU AI Act awareness).
- ➗ **Equation · L1:** ε-DP `P(M(D)∈S) ≤ e^ε·P(M(D′)∈S)` · Laplace noise `b = Δf/ε` · equalized odds `TPR_a = TPR_b, FPR_a = FPR_b`
- ⌨️ **Build · L2:** add Laplace noise to a count query; a DP-SGD run with `opacus`; mask PII in logs; a fairness report with `fairlearn`; write a model card for the payslip detector.
- 📊 **Measure · L2:** accuracy vs ε; fairness gap before / after mitigation.
- 📈 **Improve · L3:** no protection → PII masking → DP / fairness mitigation.
- 🎤 **Interview · L3:** What does ε mean? · Federated vs centralized? · Which fairness metric when?
- ✅ **Done when:** a model card and a fairness report.

<a id="day-171"></a>
#### ☐ Day 171 — Recommenders, advanced ☆
- 🧠 **Idea · L1:** production recommenders use **two stages**: fast candidate retrieval (two-tower embeddings + ANN) then a ranking model; plus ALS for implicit feedback, bias / diversity / exploration.
- ➗ **Equation · L1:** two-tower score `s(u,i) = f(u)·g(i)` with in-batch softmax loss · ALS minimizes `Σ c_ui(p_ui − xᵤᵀyᵢ)² + λ(…)` · MMR diversity
- ⌨️ **Build · L2:** an ALS model (`implicit`); a two-tower model in PyTorch with FAISS retrieval; re-rank with a gradient-boosted model.
- 📊 **Measure · L2:** recall@k (retrieval), NDCG (ranking), diversity, coverage.
- 📈 **Improve · L3:** popularity → ALS → two-tower + ranker.
- 🎤 **Interview · L3:** Why two stages? · Explicit vs implicit feedback? · Feedback loops and popularity bias?
- ✅ **Done when:** a two-stage pipeline with metrics per stage.

<a id="day-172"></a>
#### ☐ Day 172 — Search and learning-to-rank ☆
- 🧠 **Idea · L1:** search = retrieval + ranking. **BM25** (keyword), dense retrieval, **learning-to-rank** (pointwise, pairwise, **LambdaMART**), query understanding.
- ➗ **Equation · L1:** BM25 `Σ IDF(t)·f(t,d)(k₁+1)/(f(t,d)+k₁(1−b+b·|d|/avgdl))` · pairwise loss `log(1+e^(−(sᵢ−sⱼ)))` · NDCG@k
- ⌨️ **Build · L2:** BM25 from scratch; Elasticsearch / OpenSearch or `rank-bm25`; LightGBM `lambdarank` on a small LTR set; hybrid BM25 + dense.
- 📊 **Measure · L2:** NDCG@10, MRR, recall@100.
- 📈 **Improve · L3:** BM25 → hybrid → + LambdaMART re-ranker.
- 🎤 **Interview · L3:** BM25 vs embeddings? · Pointwise vs pairwise vs listwise? · Why NDCG?
- ✅ **Done when:** a search system you can evaluate.

<a id="day-173"></a>
#### ☐ Day 173 — Reading and reproducing a paper ☆
- 🧠 **Idea · L1:** the fastest way to grow. Read in 3 passes (skim → structure → details), write the method as pseudo-code, then **reproduce one result**.
- ➗ **Equation · L1:** pick the paper's core equation and re-derive it by hand.
- ⌨️ **Build · L2:** reproduce a small result from *Attention Is All You Need*, *LoRA* or *ResNet* in a notebook with a fixed seed.
- 📊 **Measure · L2:** your number vs the paper's number; list what differs and why.
- 📈 **Improve · L3:** one-page summary → pseudo-code → working code → ablation.
- 🎤 **Interview · L3:** Explain a paper you read in 3 minutes. · How do you judge a paper's claims? · What is an ablation?
- ✅ **Done when:** a repo with a reproduced figure.

<a id="day-174"></a>
#### ☐ Day 174 — Kaggle workflow ☆
- 🧠 **Idea · L1:** practice against real leaderboards: **strong CV that matches the leaderboard**, feature work, ensembling, and reading the winning write-ups.
- ➗ **Equation · L1:** CV–LB gap `= |CV score − LB score|` (small = trustworthy validation).
- ⌨️ **Build · L2:** enter one tabular competition (e.g. Titanic → a current playground): baseline → feature engineering → LightGBM / CatBoost + CV → ensemble; read two top solutions.
- 📊 **Measure · L2:** CV vs public LB; improvement per idea.
- 📈 **Improve · L3:** baseline → features → tuned GBM → blend.
- 🎤 **Interview · L3:** How do you build a trustworthy CV? · What is leaderboard overfitting? · What did you learn from the winners?
- ✅ **Done when:** a submission in the top 30 % of a live playground.

<a id="day-175"></a>
#### ☐ Day 175 — Coding-interview pack I: arrays, hashing, two-pointers, stack, heap ☆
- 🧠 **Idea · L1:** AI-engineer interviews often include normal coding. Practice **Python** patterns and say the complexity out loud.
- ➗ **Equation · L1:** time / space complexity of each solution (`O(n)`, `O(n log n)` …).
- ⌨️ **Build · L2:** 12 problems: two-sum, sliding window, top-k with a heap, valid parentheses, intervals, hash-map counting, binary search.
- 📊 **Measure · L2:** solve time per problem; mistakes log.
- 📈 **Improve · L3:** brute force → optimal → clean code with tests.
- 🎤 **Interview · L3:** explain each solution and its trade-offs aloud.
- ✅ **Done when:** 12 problems solved in ≤ 25 minutes each.

<a id="day-176"></a>
#### ☐ Day 176 — Coding-interview pack II: trees, graphs, DP and "ML from scratch" ☆
- 🧠 **Idea · L1:** the second half: recursion, BFS / DFS, dynamic programming, and the ML-coding questions (implement K-Means, logistic regression, attention, softmax, AUC from scratch).
- ➗ **Equation · L1:** DP recurrence for each problem · attention `softmax(QKᵀ/√d)V` in 10 lines.
- ⌨️ **Build · L2:** 8 graph / tree / DP problems; then from memory: K-Means, logistic GD, softmax + cross-entropy, ROC-AUC, scaled dot-product attention (NumPy only).
- 📊 **Measure · L2:** time per problem; correctness vs sklearn / PyTorch.
- 📈 **Improve · L3:** first attempt → optimized → vectorized.
- 🎤 **Interview · L3:** whiteboard two ML-coding questions aloud.
- ✅ **Done when:** all five ML-from-scratch pieces run without notes.

<a id="day-177"></a>
#### ☐ Day 177 — Open source and writing in public ☆
- 🧠 **Idea · L1:** visible work gets interviews. Contribute a small fix to an open-source AI library and publish one technical blog post.
- ➗ **Equation · L1:** none — measure: merged PRs, post readers.
- ⌨️ **Build · L2:** find a "good first issue" (scikit-learn, Hugging Face, LangChain, LlamaIndex …), open a PR with a test; write a 1 000-word post about a project's V1 → V4 ladder.
- 📊 **Measure · L2:** review feedback; reader feedback.
- 📈 **Improve · L3:** draft → peer review → published.
- 🎤 **Interview · L3:** Tell the story of your PR / post in 2 minutes.
- ✅ **Done when:** one PR opened and one post live.

<a id="day-178"></a>
#### ☐ Day 178 — ML system design II (ranking, search, fraud at scale) ☆
- 🧠 **Idea · L1:** harder designs: news-feed ranking, search ranking, ads CTR, real-time fraud, LLM gateway with routing / caching / fallbacks.
- ➗ **Equation · L1:** back-of-envelope QPS, storage, GPU cost; latency budget per stage.
- ⌨️ **Build · L2:** 3 full designs with diagrams, data flow, metrics (offline + online), failure modes, rollout (shadow → canary → A/B).
- 📊 **Measure · L2:** score each with your Day-112 checklist; get one design reviewed.
- 📈 **Improve · L3:** V1 → add numbers → add trade-offs.
- 🎤 **Interview · L3:** "Design a real-time fraud system." (45 minutes, recorded)
- ✅ **Done when:** 3 designs in a portfolio folder.

<a id="day-179"></a>
#### ☐ Day 179 — Behavioural interview, résumé and salary ☆
- 🧠 **Idea · L1:** the non-technical half. STAR stories, a one-page résumé with **numbers** (V1 → V4 gains, latency, cost), LinkedIn headline, offers and negotiation.
- ➗ **Equation · L1:** impact statement `did X using Y, which improved Z by N %`.
- ⌨️ **Build · L2:** 8 STAR stories (conflict, failure, ownership, ambiguity…); résumé v1 → v2; practise "tell me about yourself" in 90 seconds.
- 📊 **Measure · L2:** a friend / peer scores clarity; every bullet has a number.
- 📈 **Improve · L3:** résumé v1 → v2 → tailored per job.
- 🎤 **Interview · L3:** answer 10 behavioural questions aloud.
- ✅ **Done when:** a résumé you are proud of and 8 rehearsed stories.

<a id="day-180"></a>
#### ☐ Day 180 — Final gap audit and your 12-month plan ☆
- 🧠 **Idea · L1:** close the loop. Re-check every topic against Appendix D, list what is still weak, and plan the next year: specialize (one deep area), compete (Kaggle), publish (blog / paper), and ship (production project).
- ➗ **Equation · L1:** none — confidence score 1–5 per topic.
- ⌨️ **Build · L2:** score every row of the gap audit; pick 3 weak areas; make a 12-month calendar with monthly goals and one flagship project.
- 📊 **Measure · L2:** average confidence; number of topics ≥ 4.
- 📈 **Improve · L3:** re-study the lowest 5 topics for one week.
- 🎤 **Interview · L3:** a final 60-minute mock covering theory, coding and system design.
- ✅ **Done when:** a 12-month plan on one page. **You are an AI engineer.** 🎓


---

### ✅ Part XIII cheat card — pick your next topic
| Your goal | Start with shelf days |
|---|---|
| Stronger statistics / uncertainty | 123, 124, 127, 128, 132 |
| Better tabular ML | 121, 122, 126, 138, 140 |
| Computer-vision / generative image work | 141–145 |
| LLM engineer | 150–158 |
| Agent engineer | 163–166 |
| Platform / MLOps engineer | 148, 149, 167–170 |
| Interview in 4 weeks | 173, 175, 176, 178, 179 |

[📖 Table of contents](README.md) · [← previous part](part12_design_interview_capstone.md) · [Appendices](appendix.md)
