# PART IV — Unsupervised Learning

[📖 Table of contents](README.md) · [← previous part](part3_supervised_classification.md) · [next part →](part5_evaluation_special_ml.md) · [Appendices](appendix.md)


> **Days 34–39 · Category: unsupervised learning — find structure with no labels · Levels: 1 → 3 in every chapter**
> **You will be able to:** group rows (K-Means, hierarchical, DBSCAN, Gaussian mixtures), compress and visualize data (PCA, LDA, t-SNE, UMAP), choose features, and find anomalies (Isolation Forest, LOF) — the engine of your HRM payslip detector.
> **Math you meet here (just-in-time):** centroid and SSE (Day 34) · Gaussian mixture, EM (35) · eigenvalues, covariance matrix, SVD (36) · explained variance (37) · mutual information, VIF (38).
> **Your class notes used:** *Classification vs Clustering, K-Means, PCA* (in *Distance Metrics*) · *High vs low dimensionality, Feature selection vs extraction*.

---

## Chapter 18 — Clustering

> **You will learn:** how K-Means, hierarchical, DBSCAN and Gaussian mixtures work, and how to pick a method from the *shape* of the data.
> ⚠️ **Common mistakes:** no scaling · choosing k by eye only · running K-Means on moon-shaped data · treating cluster labels as ground truth.

### Level 1 — Beginner: K-Means
<a id="day-34"></a>
#### ☐ Day 34 — K-Means
- 🧮 **New math today (just-in-time):** centroid (mean of a group), within-cluster sum of squares (SSE), silhouette score.
- 🧠 **Idea · L1:** find k group centres; assign each point to the nearest centre; move centres; repeat.
- ➗ **Equation · L1:** `J = Σₖ Σ_{x∈Cₖ} ‖x − μₖ‖²` · update `μₖ = mean of Cₖ` · silhouette `s = (b − a)/max(a, b)`
- ⌨️ **Build · L2:** Lloyd's algorithm from scratch; k-means++ start; elbow plot + silhouette; customer segmentation on sales data.
- 📊 **Measure · L2:** inertia, silhouette, stability across seeds.
- 📈 **Improve · L3:** random start → k-means++ → scaled features → best k.
- 🎤 **Interview · L3:** How to choose k? · Weaknesses of K-means? · Why scale features?
- ✅ **Done when:** you can explain why K-means fails on moons.


### Level 2–3 — Intermediate to Advanced: density, hierarchy and mixtures
<a id="day-35"></a>
#### ☐ Day 35 — Hierarchical, DBSCAN, Gaussian Mixture
- 🧮 **New math today (just-in-time):** Gaussian mixture model and the EM algorithm; density (ε-neighbourhood).
- 🧠 **Idea · L1:** other ways to group: build a tree of merges; or by **density**; or soft assignments with Gaussians.
- ➗ **Equation · L1:** linkage (single / complete / ward) · DBSCAN: core point has ≥ `minPts` neighbours within `ε` · GMM `p(x) = Σₖ πₖ·N(x|μₖ, Σₖ)` (fit with EM)
- ⌨️ **Build · L2:** dendrogram; DBSCAN on moons; `GaussianMixture`; compare on blobs / moons / circles.
- 📊 **Measure · L2:** silhouette, adjusted Rand index (if labels exist), noise points found.
- 📈 **Improve · L3:** K-means → DBSCAN (tuned ε) → GMM; pick by data shape.
- 🎤 **Interview · L3:** When DBSCAN over K-means? · Hard vs soft clustering? · What does EM do?
- ✅ **Done when:** you can choose a clustering method from a scatter plot.


## Chapter 19 — Dimensionality reduction and feature selection

> **You will learn:** the linear algebra behind PCA, PCA from scratch, LDA vs PCA, t-SNE / UMAP for pictures, and feature selection vs extraction.
> ⚠️ **Common mistakes:** PCA without centering / scaling · using t-SNE distances as real distances · fitting PCA on train + test together.

### Level 1 — Beginner: eigenvectors and SVD
<a id="day-36"></a>
#### ☐ Day 36 — Eigenvectors, covariance matrix & SVD (the maths behind PCA)
- 🧮 **New math today (just-in-time):** eigenvalues and eigenvectors · covariance matrix · singular value decomposition.
- 🧠 **Idea · L1:** a matrix stretches space. **Eigenvectors** = directions that are only stretched, not turned. **SVD** splits any matrix into rotate–scale–rotate and tells you the most important directions.
- ➗ **Equation · L1:** `A v = λ v` · `A = U Σ Vᵀ` · covariance `C = XᵀX/(n−1)` (X centred)
- ⌨️ **Build · L2:** `np.linalg.eig` on a 2×2 (check by hand). SVD of a small image. Rank-k approximation `A_k`.
- 📊 **Measure · L2:** reconstruction error `‖A − A_k‖` vs k. Plot it.
- 📈 **Improve · L3:** k=1 → k=5 → k=20 → choose k that keeps 95 % of the energy.
- 🎤 **Interview · L3:** Eigenvector in plain words? · How is SVD related to PCA? · Why centre the data first?
- ✅ **Done when:** you can compress an image and report the error.


### Level 2 — Intermediate: PCA, LDA, t-SNE, UMAP
<a id="day-37"></a>
#### ☐ Day 37 — PCA from scratch + LDA vs PCA + t-SNE / UMAP
- 🧮 **New math today (just-in-time):** explained variance ratio · between-class and within-class scatter (LDA).
- 🧠 **Idea · L1:** PCA = rotate the data so the first axis has the most variance. Keep the top axes. t-SNE / UMAP = pictures that keep neighbours together.
- ➗ **Equation · L1:** centre `X`; `C = XᵀX/(n−1)`; eigenvectors `W`; project `Z = XW_k`; explained variance ratio `λᵢ/Σλ` · t-SNE minimizes `KL(P‖Q)`
- ⌨️ **Build · L2:** PCA with `np.linalg.eigh`, compare sklearn; reconstruct; scree plot; `LinearDiscriminantAnalysis` as a *supervised* reducer — compare class separation with PCA; t-SNE / UMAP on `digits`.
- 📊 **Measure · L2:** accuracy of a classifier on PCA features vs k.
- 📈 **Improve · L3:** raw → scaled → PCA 95 % → (compare) t-SNE only for plots.
- 🎤 **Interview · L3:** What does PCA maximize? · PCA vs LDA? · Why not use t-SNE for features? · How many components?
- ✅ **Done when:** your PCA = sklearn PCA (up to sign).


### Level 3 — Advanced: choosing features
<a id="day-38"></a>
#### ☐ Day 38 — Feature selection vs feature extraction
- 🧮 **New math today (just-in-time):** mutual information · variance inflation factor (VIF) · chi-square for features.
- 🧠 **Idea · L1:** too many features = slow, noisy, overfit (the *curse of dimensionality*). **Selection** keeps some columns (filter / wrapper / embedded). **Extraction** builds new ones (PCA, LDA — Day 37). Your class notes: *High vs low dimensionality*.
- ➗ **Equation · L1:** mutual information `I(X;Y) = ΣΣ p(x,y) log[p(x,y)/(p(x)p(y))]` · `VIF = 1/(1 − R²)` · Lasso penalty `λΣ|wⱼ|` · variance threshold `Var(x) < t`
- ⌨️ **Build · L2:** filters (correlation, mutual info, chi², variance threshold); wrapper (RFE, forward/backward); embedded (Lasso, tree importance, permutation importance).
- 📊 **Measure · L2:** score vs number of features (plot); stability of the chosen set across CV folds.
- 📈 **Improve · L3:** all features → filter → RFE → embedded; keep the smallest set within 1 % of the best score.
- 🎤 **Interview · L3:** Selection vs extraction? · Filter vs wrapper vs embedded? · What is multicollinearity? · Why select features *inside* CV?
- ✅ **Done when:** you removed ≥ 30 % of features with no score loss.


## Chapter 20 — Anomaly detection

> **You will learn:** Isolation Forest, Local Outlier Factor, One-Class SVM idea, evaluating detectors with no labels.
> ⚠️ **Common mistakes:** evaluating with accuracy · ignoring false alarms (the real cost) · trusting `contamination` blindly.

### Levels 1 → 3 (inside the day) — Checkpoint C
<a id="day-39"></a>
#### ☐ Day 39 — Anomaly detection
- 🧠 **Idea · L1:** find the rare and strange rows. Your **HRM payslip detector** is exactly this.
- ➗ **Equation · L1:** Isolation Forest score `s(x,n) = 2^(−E[h(x)]/c(n))` (short path = anomaly) · LOF = local density ratio · z-score
- ⌨️ **Build · L2:** Isolation Forest, LOF, One-Class SVM on HRM payslips (reuse `hrm_detective/`); inject known anomalies to test.
- 📊 **Measure · L2:** precision@k, recall of injected anomalies; look at false alarms.
- 📈 **Improve · L3:** z-score → Isolation Forest → tuned contamination → add rule-based checks.
- 🎤 **Interview · L3:** Supervised vs unsupervised anomaly detection? · How do you evaluate with no labels? · Contamination parameter?
- ✅ **Checkpoint:** **"Payslip anomaly service"** + FastAPI + test + 20 questions (Days 34–39).


---

### ✅ Part IV cheat card — which clustering / reduction method?
| Method | Needs k? | Cluster shape | Handles noise? | Scales to big data? | Use when |
|---|---|---|---|---|---|
| K-Means | yes | round, similar size | no | **yes** | quick segmentation |
| Hierarchical | no (cut the tree) | any (linkage) | no | no (`O(n²)`) | small data, dendrogram |
| DBSCAN | no (needs ε, minPts) | any | **yes** | medium | arbitrary shapes + outliers |
| Gaussian mixture | yes | ellipses | no | medium | soft membership |
| PCA | components | — (linear) | — | **yes** | compress, de-noise |
| LDA (as reduction) | ≤ classes − 1 | — (supervised) | — | yes | best class separation |
| t-SNE / UMAP | 2–3 dims | — (non-linear) | — | medium | **pictures only** |

[📖 Table of contents](README.md) · [← previous part](part3_supervised_classification.md) · [next part →](part5_evaluation_special_ml.md) · [Appendices](appendix.md)
