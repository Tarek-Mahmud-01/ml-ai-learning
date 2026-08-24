# 🏛️ Becoming a Strong AI/ML Engineer — Complete, No-Gaps Curriculum

> **Goal:** become a **strong** AI/ML engineer — deep, solid foundations, *no gaps*. Not a fast
> job-rush; real understanding. Jobs come naturally once you are strong.
> **You:** beginner in ML/AI, but a real software engineer (3 years FastAPI/backend). We use that
> strength, but we do **not** skip the fundamentals.
> **Style:** depth-first. **No black boxes** — where it builds intuition, you implement the idea
> *by hand* before using a library.
> **Pace:** take the time each chapter needs. Master it, then move on. Order matters — go 1 → 20.

**Companion notes (reuse, don't duplicate):**
- Deep theory per topic → [advanced_ai_roadmap.md](advanced_ai_roadmap.md)
- Exact libraries + install order → [tools_and_libraries.md](tools_and_libraries.md)
- A day-by-day schedule option → [daily_plan_advanced.md](daily_plan_advanced.md)

---

## 📐 How every chapter is built (consistent structure)
Every chapter below follows the **same 8 parts**, so it reads like a real course:

1. **🎯 Why this matters** — plain-language motivation.
2. **📖 Concepts to master** — the full, numbered list of sub-topics (this is the "no gaps" part).
3. **🏋️ Training focus** — what the chapter teaches about *training a model* (when relevant).
4. **📊 Evaluation / accuracy focus** — how you *measure success* here (when relevant).
5. **🧰 Tools & libraries** — what you install/use.
6. **✅ Practice** — small exercises (checkboxes).
7. **🚀 Chapter project** — build something and be able to explain it.
8. **🔑 Checkpoint** — "you can now …".

**The strong-engineer rule:** never move to the next chapter until you can *explain the current
one to someone else* and you finished its 🚀 project.

---
---

# PART A — Foundations

## 📘 Chapter 1 — The AI landscape (your mental map)
**🎯 Why this matters:** you must know *what* you're learning and how the pieces fit before you
touch code. This prevents confusion for the rest of the journey.
**📖 Concepts to master:**
1. **AI vs Machine Learning vs Deep Learning vs Data Science** — how they nest inside each other.
2. **What "learning from data" means** — a model finds patterns instead of you writing rules.
3. **The 4 types of ML:**
   - **Supervised** (labeled data → predict) — regression & classification.
   - **Unsupervised** (no labels → find structure) — clustering, dimensionality reduction.
   - **Reinforcement** (agent + environment + reward → learn by trial).
   - **Semi-supervised / self-supervised** (a little/无 labels) — the idea behind modern LLMs.
4. **The ML project lifecycle:** frame the problem → collect/clean data → choose a model →
   **train** → **evaluate (accuracy)** → tune → deploy → monitor → retrain.
5. **Where each job/topic in this file sits** on that map.
**🧰 Tools & libraries:** none yet — paper, notes, diagrams.
**✅ Practice:**
- [ ] Draw the AI ⊃ ML ⊃ DL diagram from memory.
- [ ] For 5 real problems (spam filter, price predictor, game bot, customer groups, chatbot),
  label which *type* of ML each is.
**🚀 Chapter project:** Write a 1-page note in your own words: "What is ML, its 4 types, and the
lifecycle" — with one example of each type from your HRM/work life.
**🔑 Checkpoint:** You can explain the 4 types of ML and the full ML lifecycle without notes.

---

## 📗 Chapter 2 — Python & the data toolkit
**🎯 Why this matters:** all ML work runs on numpy/pandas. Strong data-handling = strong ML.
**📖 Concepts to master:**
1. **numpy** — arrays, shapes, broadcasting, vectorization (why loops are slow).
2. **pandas** — DataFrame, Series, selecting, filtering, `groupby`, `merge`, missing data.
3. **Visualization** — matplotlib basics + seaborn (histograms, scatter, box, heatmap).
4. **Environments** — `venv`, installing packages, Jupyter notebooks, **Google Colab** (free GPU
   later).
5. **Git hygiene for ML** — ignore data/models, never commit secrets.
**🏋️ Training focus:** none yet — but clean data is the input to every model you'll train.
**🧰 Tools & libraries:** python 3.12, numpy, pandas, matplotlib, seaborn, jupyter, git.
**✅ Practice:**
- [ ] Load a CSV, remove nulls & duplicates, fix dtypes.
- [ ] `groupby` a column and compute averages.
- [ ] Make a histogram, a scatter plot, and a correlation heatmap.
**🚀 Chapter project:** A **"data profiler"** notebook: give it any CSV → it prints shape, missing
%, dtypes, and auto-plots every column. Reusable forever.
**🔑 Checkpoint:** You can load, clean, explore, and visualize any tabular dataset comfortably.

---

## 📙 Chapter 3 — The math you actually need
**🎯 Why this matters:** you don't need a math degree, but a strong engineer can *read* what a
model does and *debug* it. This is the difference between copy-paste and understanding.
**📖 Concepts to master:**
1. **Linear algebra** — vectors, matrices, dot product, matrix multiply *(a model layer IS a
   matrix multiply)*.
2. **Calculus** — derivative, slope, chain rule, partial derivatives, **gradient** *(this IS how
   models learn)*.
3. **Probability** — events, conditional probability, **Bayes' theorem**, expectation.
4. **Statistics** — mean, variance, std, distributions (normal, etc.), correlation vs causation.
5. **Key ML math** — **cross-entropy** & **mean-squared-error** (the two losses you'll meet most).
**🏋️ Training focus:** the **gradient** is the engine of training — you'll use it in Ch 7 & 14.
**🧰 Tools & libraries:** numpy, matplotlib, **3Blue1Brown** (YouTube) for intuition.
**✅ Practice:**
- [ ] Multiply two matrices by hand, verify with numpy.
- [ ] Plot a curve `y=x²` and its derivative `2x`.
- [ ] Compute a simple Bayes' theorem problem by hand.
**🚀 Chapter project:** **Gradient descent from scratch in pure NumPy** — fit a straight line to
data by computing gradients and updating weights in a loop. Plot the line improving.
**🔑 Checkpoint:** You can explain "what a gradient is and why we subtract it" in plain words.

---
---

# PART B — Core Machine Learning (build the strong base)

## 📕 Chapter 4 — Data preprocessing & feature engineering
**🎯 Why this matters:** real data is messy. **80% of ML work is data.** Good features beat fancy
models — this is where strong engineers win.
**📖 Concepts to master:**
1. **Missing values** — drop vs impute (mean/median/mode/model-based).
2. **Outliers** — detect (IQR, z-score) and handle.
3. **Encoding categoricals** — one-hot, label, target encoding.
4. **Scaling** — normalization vs standardization, and *why* models need it.
5. **Feature engineering** — creating useful new columns (dates → day/hour, ratios, bins).
6. **Feature selection** — correlation, importance, removing useless/redundant features.
7. **Data leakage** — the #1 beginner bug (info from the future/target sneaking into training).
8. **sklearn `Pipeline` & `ColumnTransformer`** — do all steps safely, no leakage.
**🏋️ Training focus:** these transforms must be *fit on train only*, then applied to test.
**📊 Evaluation focus:** leakage makes accuracy look great but fail in the real world — beware.
**🧰 Tools & libraries:** pandas, scikit-learn (`preprocessing`, `pipeline`, `impute`).
**✅ Practice:**
- [ ] Build one `Pipeline`: impute → encode → scale → (placeholder) model.
- [ ] Create 3 new engineered features from a raw dataset.
- [ ] Spot and fix a deliberate leakage example.
**🚀 Chapter project:** Take a raw messy dataset → produce a clean, fully-preprocessed feature
table via a single reusable sklearn `Pipeline`.
**🔑 Checkpoint:** You can turn raw messy data into model-ready features without leakage.

---

## 📈 Chapter 5 — Regression (predicting numbers)
**🎯 Why this matters:** predicting a *number* (price, salary, demand) is one half of supervised
learning. Simple, foundational, everywhere.
**📖 Concepts to master:**
1. **Linear regression** — the line of best fit, coefficients, intercept.
2. **Polynomial regression** — fitting curves.
3. **Regularized regression** — **Ridge (L2)** and **Lasso (L1)**, and *why* they fight
   overfitting.
4. Assumptions & when regression fails.
**🏋️ Training focus:** the model is *trained* by minimizing squared error (links back to Ch 3).
**📊 Evaluation / accuracy focus (regression metrics):** **MAE**, **MSE**, **RMSE**, **R²** —
what each means and when to use which.
**🧰 Tools & libraries:** scikit-learn (`LinearRegression`, `Ridge`, `Lasso`), matplotlib.
**✅ Practice:**
- [ ] Fit linear regression; read the coefficients.
- [ ] Compare MAE / RMSE / R² on the same model.
- [ ] Show Ridge/Lasso reducing overfitting vs plain linear.
**🚀 Chapter project:** Predict a real number (e.g. house price or salary) end-to-end; report all
4 regression metrics and explain them.
**🔑 Checkpoint:** You can build a regression model and correctly interpret MAE/MSE/RMSE/R².

---

## 📉 Chapter 6 — Classification (predicting categories)
**🎯 Why this matters:** predicting a *class* (spam/not, fraud/not, which-group) is the other half
of supervised learning — and the most common business ML.
**📖 Concepts to master:**
1. **Logistic regression** — classification via probability (the sigmoid).
2. **k-Nearest Neighbors (kNN)** — predict by closest examples.
3. **Support Vector Machines (SVM)** — the max-margin idea, kernels.
4. **Naive Bayes** — probability-based, great for text.
5. **Decision trees** — human-readable if/else splits.
6. **Binary vs multi-class vs multi-label.**
**🏋️ Training focus:** how each learns; probability outputs vs hard labels.
**📊 Evaluation focus:** intro to the confusion matrix & accuracy (full depth in Ch 8).
**🧰 Tools & libraries:** scikit-learn (`LogisticRegression`, `KNeighborsClassifier`, `SVC`,
`GaussianNB`, `DecisionTreeClassifier`).
**✅ Practice:**
- [ ] Train all 5 classifiers on one dataset and compare accuracy.
- [ ] Visualize a decision tree's splits.
**🚀 Chapter project:** A classifier on a real dataset (e.g. will an employee be flagged? / churn)
— try several models and pick the best (proper comparison in Ch 8).
**🔑 Checkpoint:** You know the main classification algorithms and when each fits.

---

## ⭐ Chapter 7 — Model Training deep-dive *(the heart of "strong")*
**🎯 Why this matters:** **this is how models actually learn.** Understand this and every model
— from linear regression to GPT — stops being magic.
**📖 Concepts to master:**
1. **Loss/cost functions** — what "wrong" means numerically (MSE for regression, **cross-entropy**
   for classification).
2. **Gradient descent** — how the model reduces loss step by step. Variants: **batch**,
   **stochastic (SGD)**, **mini-batch**.
3. **Learning rate** — too big (diverges) vs too small (crawls); the key knob.
4. **Epochs & batch size** — one pass over data vs chunks; what they control.
5. **Train / validation / test split** — why three sets, and what each is for.
6. **Overfitting vs underfitting** — memorizing vs not learning; how to recognize each.
7. **Bias–variance tradeoff** — the core mental model of model error.
8. **Regularization** — L1/L2, dropout (preview), early stopping — how to *stop* overfitting.
9. **Learning curves** — reading training vs validation loss to diagnose problems.
**🏋️ Training focus:** the whole chapter *is* the training focus — the engine under everything.
**📊 Evaluation focus:** validation loss is your early warning for overfitting.
**🧰 Tools & libraries:** numpy (from scratch), scikit-learn, matplotlib (plot loss curves).
**✅ Practice:**
- [ ] **Implement gradient descent by hand** (extend Ch 3) and plot loss going down.
- [ ] Change the learning rate and *watch* training diverge / crawl / converge.
- [ ] Deliberately overfit a model, then fix it with regularization; show the learning curves.
**🚀 Chapter project:** A notebook that **teaches training visually** — sliders/plots for learning
rate, epochs, and regularization, showing loss curves and over/underfitting live.
**🔑 Checkpoint:** You can explain loss, gradient descent, learning rate, and the bias–variance
tradeoff, and *diagnose* over/underfitting from a learning curve.

---

## ⭐ Chapter 8 — Model Evaluation & Accuracy deep-dive *(the heart of "strong")*
**🎯 Why this matters:** you asked for this. **Knowing if a model is actually good** is a
top-level skill. Beginners trust "accuracy" and get burned — strong engineers don't.
**📖 Concepts to master:**
1. **Why plain accuracy lies** — the imbalanced-data trap (99% accuracy that's useless).
2. **Confusion matrix** — TP, FP, TN, FN — the foundation of all classification metrics.
3. **Precision, Recall, F1** — what each protects against; when to prefer which.
4. **ROC curve & AUC**, **Precision-Recall curve** — threshold-independent quality.
5. **Threshold tuning** — moving the decision line to trade precision vs recall.
6. **Cross-validation** — k-fold; why a single split can fool you.
7. **Regression metrics recap** — MAE/MSE/RMSE/R² (from Ch 5) in context.
8. **Imbalanced data** — resampling (SMOTE/undersampling), class weights.
9. **Learning curves & validation curves** — over/underfitting seen through evaluation.
**📊 Evaluation focus:** the entire chapter — this is your "is it good?" toolkit.
**🧰 Tools & libraries:** scikit-learn (`metrics`, `model_selection`), matplotlib, imbalanced-learn.
**✅ Practice:**
- [ ] Build a confusion matrix by hand from predictions, then verify with sklearn.
- [ ] On an **imbalanced** dataset, show accuracy is misleading but F1/recall reveal the truth.
- [ ] Plot an ROC curve and read the AUC.
- [ ] Run 5-fold cross-validation and compare to a single split.
**🚀 Chapter project:** An **"evaluation report" tool**: given a model + test data, output the
confusion matrix, precision/recall/F1, ROC-AUC, and a plain-English verdict.
**🔑 Checkpoint:** You never trust accuracy alone again — you can choose and explain the right
metric for any problem.

---

## 🌲 Chapter 9 — Ensemble methods (combine models to win)
**🎯 Why this matters:** ensembles dominate **tabular** ML competitions and real business data.
**📖 Concepts to master:**
1. **Bagging** → **Random Forest** (many trees vote).
2. **Boosting** → **Gradient Boosting**, **XGBoost**, **LightGBM** (trees fix each other's errors).
3. **Stacking** — combine different model types.
4. **When ensembles beat single models** (and their cost).
**🏋️ Training focus:** boosting trains sequentially; watch overfitting and learning rate again.
**📊 Evaluation focus:** feature importance from ensembles; compare with Ch 8 metrics.
**🧰 Tools & libraries:** scikit-learn, **xgboost**, **lightgbm**.
**✅ Practice:**
- [ ] Beat a single tree with a Random Forest, then with XGBoost.
- [ ] Read feature importances and explain the top features.
**🚀 Chapter project:** Take your Ch 6 classifier and maximize it with XGBoost/LightGBM + tuning;
prove the improvement with proper metrics.
**🔑 Checkpoint:** You can build and tune strong ensemble models for tabular data.

---

## 🧩 Chapter 10 — Unsupervised learning (find structure, no labels)
**🎯 Why this matters:** most real-world data has no labels. Clustering, compression, and anomaly
detection are everywhere (including your HRM anomaly work).
**📖 Concepts to master:**
1. **Clustering** — **k-means**, hierarchical, **DBSCAN**; choosing k (elbow, silhouette).
2. **Dimensionality reduction** — **PCA** (and a peek at t-SNE/UMAP for visualization).
3. **Anomaly / outlier detection** — **Isolation Forest** (you used this in HRM).
4. Evaluating unsupervised results (harder — silhouette score, domain checks).
**📊 Evaluation focus:** no labels means you judge with internal scores + human sense.
**🧰 Tools & libraries:** scikit-learn (`cluster`, `decomposition`, `ensemble`).
**✅ Practice:**
- [ ] Cluster customers/employees into groups; describe each group.
- [ ] Reduce many features to 2 with PCA and plot them.
- [ ] Flag anomalies with Isolation Forest.
**🚀 Chapter project:** Segment a real dataset into meaningful groups (or re-do HRM anomaly
detection) and explain what the clusters/anomalies mean.
**🔑 Checkpoint:** You can cluster, reduce dimensions, and detect anomalies without labels.

---

## 🎛️ Chapter 11 — Hyperparameter tuning & model selection
**🎯 Why this matters:** the difference between an okay model and a great one is often good tuning
— done *without* fooling yourself.
**📖 Concepts to master:**
1. **Parameters vs hyperparameters** — learned vs set-by-you.
2. **Grid search**, **random search**, **Bayesian optimization** (Optuna).
3. **Validation strategy** — nested CV; keeping the test set untouched.
4. **Leakage in tuning** — a subtle strong-engineer trap.
**🏋️ Training focus:** tuning controls training behavior (depth, learning rate, regularization).
**📊 Evaluation focus:** always tune against validation, judge final on the held-out test set.
**🧰 Tools & libraries:** scikit-learn (`GridSearchCV`, `RandomizedSearchCV`), **Optuna**.
**✅ Practice:**
- [ ] Grid-search an XGBoost model; report the best params.
- [ ] Compare grid vs random vs Optuna on the same model.
**🚀 Chapter project:** Systematically tune one model from Ch 9 and show a documented, honest
improvement (no test-set leakage).
**🔑 Checkpoint:** You can tune models properly and avoid tricking yourself.

---

## 🕰️ Chapter 12 — Specialized ML (time series, recommenders, RL)
**🎯 Why this matters:** these are huge, distinct problem types every strong engineer should know
— and they don't fit the plain "rows of features" mold.
**📖 Concepts to master:**
1. **Time-series forecasting** — trend, seasonality, lag features, train/test *by time* (no
   shuffling!); classic (ARIMA/Prophet) vs ML approaches. *(Ties to your sales-forecast work.)*
2. **Recommendation systems** — collaborative filtering, content-based, matrix factorization,
   the cold-start problem.
3. **Reinforcement learning (intro)** — agent, environment, state, action, **reward**;
   exploration vs exploitation; the **Q-learning** idea. *(This is also the RLHF behind LLMs.)*
**📊 Evaluation focus:** time-series backtesting; ranking metrics for recommenders (precision@k).
**🧰 Tools & libraries:** statsmodels/**Prophet**, scikit-learn, **surprise/implicit** (recsys),
**Gymnasium** (RL sandbox).
**✅ Practice:**
- [ ] Forecast a time series with proper time-based splitting.
- [ ] Build a tiny "movies/products you may like" recommender.
- [ ] Train a Q-learning agent on a simple Gym environment (e.g. FrozenLake).
**🚀 Chapter project:** Pick ONE (forecast, recommender, or RL agent) and build it end-to-end with
correct evaluation.
**🔑 Checkpoint:** You understand time series, recommenders, and the core RL loop.

---

## ⚖️ Chapter 13 — Interpretability & responsible AI
**🎯 Why this matters:** a strong engineer can **explain** and **trust** their models — required
in real jobs (finance, HR, health) and for catching hidden bias.
**📖 Concepts to master:**
1. **Feature importance** — global explanations.
2. **SHAP** and **LIME** — per-prediction explanations ("why did the model say this?").
3. **Bias & fairness** — where unfairness enters, how to detect it.
4. **ML ethics & model cards** — documenting limits and intended use.
**📊 Evaluation focus:** fairness metrics alongside accuracy — a model can be accurate *and* unfair.
**🧰 Tools & libraries:** **shap**, **lime**, scikit-learn.
**✅ Practice:**
- [ ] Explain 3 individual predictions with SHAP.
- [ ] Check a model for bias across a sensitive group.
**🚀 Chapter project:** Add an **explanation layer** to any earlier model — for each prediction,
show *why* (SHAP), and write a short model card.
**🔑 Checkpoint:** You can explain any model's decisions and reason about its fairness.

---
---

# PART C — Deep Learning

## 🔥 Chapter 14 — Neural network foundations (PyTorch **and** TensorFlow/Keras)
**🎯 Why this matters:** deep learning powers vision, language, and generative AI. Understand the
neuron and the training loop and the rest becomes approachable. You learn **both** major
frameworks so no path is closed.
**📖 Concepts to master:**
1. Neurons, layers, **activation functions** (ReLU, sigmoid, softmax).
2. The **training loop**: forward pass → loss → **backpropagation** → optimizer step.
3. Optimizers: SGD → Momentum → **Adam**; learning-rate scheduling.
4. Regularization for nets: **dropout**, **batch norm**, early stopping.
5. **PyTorch**: `Tensor`, `autograd`, `nn.Module`, `DataLoader`, manual loop.
6. **TensorFlow / Keras 3**: `Sequential`, `model.compile`, `model.fit` — the high-level way.
7. Using a **GPU** (Google Colab free tier).
**🏋️ Training focus:** everything from Ch 7 now in a neural net — same ideas, bigger model.
**📊 Evaluation focus:** train vs validation curves; the same metrics from Ch 8 apply.
**🧰 Tools & libraries:** **PyTorch** (+torchvision), **TensorFlow/Keras 3**, tqdm, Colab.
**✅ Practice:**
- [ ] **Neural net from scratch in NumPy** (implement backprop yourself) on MNIST.
- [ ] Rebuild it in **PyTorch** (feel the difference).
- [ ] Rebuild it again in **Keras** (compare the APIs).
**🚀 Chapter project:** The same classifier built three ways (NumPy / PyTorch / Keras); write up
what each layer of abstraction gave you.
**🔑 Checkpoint:** You can write a training loop in PyTorch **and** a `model.fit()` in Keras, and
explain backprop.

---

## 👁️ Chapter 15 — Computer Vision (CNNs & transfer learning)
**🎯 Why this matters:** images are a core AI domain, and **transfer learning** (reusing pretrained
models) is the most practical DL skill.
**📖 Concepts to master:**
1. **Convolutions**, filters, **pooling**, feature maps.
2. Architectures: LeNet → **ResNet** (residual connections) → a peek at **ViT**.
3. **Transfer learning / fine-tuning** pretrained models.
4. **Data augmentation** and image preprocessing.
**🏋️ Training focus:** freezing vs fine-tuning layers; small data + pretrained weights.
**📊 Evaluation focus:** top-k accuracy, per-class confusion for images.
**🧰 Tools & libraries:** PyTorch+torchvision, `keras.applications`, Gradio (demo).
**✅ Practice:**
- [ ] Train a small CNN on CIFAR-10.
- [ ] Fine-tune a pretrained ResNet on a custom set (receipts/IDs/products).
**🚀 Chapter project:** A working image classifier or document/ID extractor, with a simple demo UI.
**🔑 Checkpoint:** You can fine-tune a pretrained vision model on your own images.

---

## 📝 Chapter 16 — NLP & Transformers
**🎯 Why this matters:** language is where AI is exploding. The **Transformer** is THE architecture
behind all modern AI — you must understand attention.
**📖 Concepts to master:**
1. Text → numbers: **tokenization**, **embeddings** (word2vec intuition).
2. **RNNs / LSTMs** — sequence models (and why transformers replaced them).
3. **The Transformer**: **self-attention**, multi-head attention, positional encoding.
4. **Hugging Face** ecosystem: `transformers`, `datasets`, the `Trainer`, the Model Hub.
**🏋️ Training focus:** fine-tuning a pretrained transformer on your own text.
**📊 Evaluation focus:** accuracy/F1 for text classification; perplexity idea for generation.
**🧰 Tools & libraries:** Hugging Face `transformers`+`datasets`+`tokenizers`, PyTorch.
**✅ Practice:**
- [ ] Fine-tune **BERT** for sentiment/text classification.
- [ ] Generate text with a small GPT-style model.
**🚀 Chapter project:** Fine-tune a transformer for a text task and (optionally) publish it to the
Hugging Face Hub with a demo.
**🔑 Checkpoint:** You can explain self-attention and fine-tune a Hugging Face model.

---
---

# PART D — Generative AI / LLMs

## 🤖 Chapter 17 — LLMs & Generative AI
**🎯 Why this matters:** the current frontier — and where your backend/agent experience makes you
strong. You already built a tool-calling agent in `hrm_app/`; here you understand it fully.
**📖 Concepts to master:**
1. **How LLMs work** — pretraining, fine-tuning, **RLHF** (note the RL link to Ch 12), tokens,
   **context windows**, temperature.
2. **Prompt engineering** as a discipline — system prompts, few-shot, structured output.
3. **RAG (Retrieval-Augmented Generation)** — chunking, **embeddings**, **vector DBs**
   (Chroma/FAISS/**pgvector**), retrieval, **reranking**, **citations**, reducing hallucination.
4. **AI agents** — **tool-calling / function-calling**, ReAct loops, memory, **multi-agent**,
   guardrails.
5. **Fine-tuning vs RAG** — when to use which; **LoRA / PEFT**, quantization.
6. **Evaluating LLM apps** — evals, cost, latency, safety.
**📊 Evaluation focus:** LLM evals are different — correctness, groundedness, and human judgment.
**🧰 Tools & libraries:** **Anthropic SDK (Claude)**, OpenAI SDK, **Ollama** (local, free),
LangChain/LlamaIndex, sentence-transformers, Chroma/FAISS/pgvector, `peft`.
**✅ Practice:**
- [ ] Force reliable **structured JSON** output from an LLM.
- [ ] Build a **minimal RAG**: a few PDFs → embeddings → vector DB → answer with sources.
- [ ] Give an LLM **one tool** and let it call it.
- [ ] **LoRA fine-tune** a small open model on a tiny dataset.
**🚀 Chapter project:** A **RAG assistant** over your own documents *or* harden your `hrm_app/`
agent into a clean, well-explained tool-using agent.
**🔑 Checkpoint:** You can build a RAG app and a tool-using agent, and explain fine-tune vs retrieve.

---
---

# PART E — Production & Practice

## ⚙️ Chapter 18 — MLOps & production
**🎯 Why this matters:** a model in a notebook helps no one. Shipping, serving, and operating
models is where your FastAPI/backend strength shines.
**📖 Concepts to master:**
1. **Serving with FastAPI** — `/predict`, `/chat`, streaming (SSE), auth, rate limits.
2. **Docker** — containerize model + API.
3. **CI/CD** — GitHub Actions (test → build → deploy).
4. **Experiment tracking** — MLflow / Weights & Biases.
5. **Versioning** — model & data (DVC), model registry idea.
6. **Monitoring** — latency, errors, **data/model drift**, retraining triggers.
7. **Deployment** — Hugging Face Spaces / Render / Modal / cloud VM.
**🏋️ Training focus:** reproducible training runs, tracked and versioned.
**📊 Evaluation focus:** monitoring metrics *in production* (drift = your accuracy decaying live).
**🧰 Tools & libraries:** FastAPI, Uvicorn, Docker, GitHub Actions, MLflow/wandb, DVC, pytest.
**✅ Practice:**
- [ ] Serve a saved model via FastAPI `/predict`.
- [ ] Dockerize it; run the container.
- [ ] Track 5 training runs and compare in MLflow/W&B.
**🚀 Chapter project:** Take any earlier model → **containerized, deployed, monitored** live URL.
**🔑 Checkpoint:** You can move a model from notebook → deployed, monitored service.

---

## 🗄️ Chapter 19 — Data & scaling essentials
**🎯 Why this matters:** AI runs on data plumbing. A strong engineer speaks data fluently.
**📖 Concepts to master:**
1. **SQL for ML** — joins, aggregations, window functions.
2. **Data pipelines / ETL** basics; **batch vs streaming**.
3. **Feature stores** (concept), data validation.
4. **Vector databases at scale** — indexing, filtering, hybrid search (**pgvector**).
**🧰 Tools & libraries:** PostgreSQL (+pgvector), SQLAlchemy *(you know it)*, DuckDB, an
orchestration tool concept (Airflow/Prefect — awareness).
**✅ Practice:**
- [ ] Answer 5 analytics questions with pure SQL.
- [ ] Store & query embeddings in pgvector.
**🚀 Chapter project:** A small **ETL → feature table → model** flow: raw data in, model-ready
features out, consumed by an earlier model.
**🔑 Checkpoint:** You can model data, write real SQL, and run a vector DB.

---

## 🏆 Chapter 20 — Projects & mastery (put it all together)
**🎯 Why this matters:** strength is proven by **building**. Each project *combines* earlier
chapters so the knowledge locks in.
**📖 Progressive projects (build in order, each explainable):**
1. **Tabular predictor + FastAPI** (Ch 4–9, 18) — full classical-ML service.
2. **Deep-learning model deployed** (Ch 14–16, 18) — vision or text.
3. **RAG assistant** (Ch 16–19) — chat over documents with citations.
4. **Tool-using AI agent** (Ch 17) — evolve your `hrm_app/` agent.
5. **🏆 Capstone — "Intelligent HRM Assistant"** — upload payslip/attendance → **anomaly model**
   flags issues (Ch 10) → **RAG-LLM explains each flag in plain English per policy** (Ch 17) → an
   **agent** can act → served via **FastAPI + UI + Docker**, deployed, with **evals** (Ch 18).
   One project spanning classical ML + deep learning + LLM/RAG/agents + production.
**🔑 Checkpoint:** You can design, build, evaluate, deploy, and *explain* a complete AI system.

---
---

## ✅ Skills mastery tracker
- [ ] Ch 1 — AI landscape (types of ML, lifecycle)
- [ ] Ch 2 — Python & data toolkit
- [ ] Ch 3 — Math (gradients, probability, stats)
- [ ] Ch 4 — Preprocessing & feature engineering
- [ ] Ch 5 — Regression (+ MAE/MSE/RMSE/R²)
- [ ] Ch 6 — Classification
- [ ] Ch 7 — ⭐ Model Training deep-dive
- [ ] Ch 8 — ⭐ Evaluation & Accuracy deep-dive
- [ ] Ch 9 — Ensembles (XGBoost/LightGBM)
- [ ] Ch 10 — Unsupervised / clustering / PCA / anomaly
- [ ] Ch 11 — Hyperparameter tuning
- [ ] Ch 12 — Time series / recommenders / RL
- [ ] Ch 13 — Interpretability & responsible AI
- [ ] Ch 14 — Neural networks (PyTorch **+** Keras)
- [ ] Ch 15 — Computer Vision
- [ ] Ch 16 — NLP & Transformers
- [ ] Ch 17 — LLMs & Generative AI
- [ ] Ch 18 — MLOps & production
- [ ] Ch 19 — Data & scaling essentials
- [ ] Ch 20 — Projects & capstone

---

## 📖 Reference resources
- **Math intuition:** 3Blue1Brown — *Essence of Linear Algebra* + *Neural Networks* (YouTube).
- **Machine learning:** Andrew Ng's ML / Deep Learning Specialization · scikit-learn user guide.
- **Deep learning:** [d2l.ai](https://d2l.ai) (free book) · **Karpathy "Zero to Hero"** (build GPT
  from scratch) · **fast.ai** *Practical Deep Learning for Coders*.
- **TensorFlow/Keras:** keras.io guides · TensorFlow tutorials.
- **NLP/LLMs:** **Hugging Face** free course · **Anthropic Claude docs** · LangChain/LlamaIndex docs.
- **Paper:** *Attention Is All You Need* (skim after Ch 16 theory).
- **Your own notes:** [advanced_ai_roadmap.md](advanced_ai_roadmap.md) (theory depth) ·
  [tools_and_libraries.md](tools_and_libraries.md) (install order per stage).

---

> **Golden rule of a strong engineer:** don't just watch or read. For **every chapter**, master
> the concepts, do the ✅ practice, finish the 🚀 project, and be able to **explain it to someone
> else**. Depth first — that is what makes you strong. 🏛️
