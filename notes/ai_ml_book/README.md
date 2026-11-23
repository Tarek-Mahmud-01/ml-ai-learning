# 📘 The AI & ML Engineer Book — 134 core days + 62 shelf days

> **For:** a learner who wants to become an advanced **AI / ML Engineer** — with **Supervised, Unsupervised, Deep Learning, NLP, Reinforcement Learning, Generative AI, Agentic AI** and **Software Engineering with AI/ML**.
> **How it is built:** like a book. **Parts** = categories (Supervised, Unsupervised, …). **Chapters** = one algorithm family. **Levels** = Beginner → Intermediate → Advanced *inside every chapter*. The **Day 1–134 schedule** at the bottom tells you what to read each day.
> **Pace:** 3–4 hours a day. Core path = Days 1–134 (job-ready). Shelf = Days 135–196 (optional, "be the best").
> **Old plans** are archived in [../old_plans/](../old_plans/). **Your class notes** (.docx) are in [../course_notes/](../course_notes/). **Libraries:** install each one when its Part arrives (`pip install` as you go).

---

## 🧭 How to read this book

### The three levels (inside every chapter, and inside every day)
| Level | Name | What you do | Day blocks |
|---|---|---|---|
| **L1** | Beginner | Understand the idea in simple words. Write the **equation** and name every symbol. Do a tiny example **by hand**. | 🧠 Idea · ➗ Equation |
| **L2** | Intermediate | **Build it twice** — from scratch (NumPy), then with the library. Measure **performance** and look at the **errors**. | ⌨️ Build · 📊 Measure |
| **L3** | Advanced | **Improve** it step by step (V1 → V4), tune, handle edge cases, and answer **interview** questions. | 📈 Improve · 🎤 Interview |

Every day ends with **✅ Done when…** — a check you can really test. Days that bring a new maths idea add one line: **🧮 New math today (just-in-time)**. There is **no separate maths block**: you meet each maths idea on the day an algorithm first needs it. The [Math map](appendix.md#a-math-map) shows where each idea lives.

### The algorithm card (answer these 10 lines for every algorithm)
`Idea · Equation · Assumptions · From-scratch code · Library code · Metric · Typical errors · How to improve (ladder) · Use / don't use · 3 interview questions`

### Rules
1. **Never skip L2 and L3.** Knowing the equation is not enough — you must also know *how the model fails* and *how to fix it*.
2. **Baseline first.** Every project starts with the dumb score (Day 1).
3. **Fit scalers / encoders / imputers on the train set only** (data leakage is the #1 interview trap).
4. **Log every score** in `plan120/results_log.md` (template in the [Appendix](appendix.md#e-trackers)). "V1 → V4" is your proof.
5. **Each chapter group ends with a checkpoint:** mini-project + 20 interview questions + wrap the model in a small FastAPI function with a test.
6. **Stuck > 30 minutes?** Write down exactly what is unclear, move on, return tomorrow.
7. Code in `plan120/dayNNN_topic.py`, one git commit per day: `Day N: topic`.

### Legend
`★` core (Days 1–134) · `☆` shelf (Days 135–196) · `L1 / L2 / L3` level · `CP` checkpoint · 📘 = your class notes cover it.

### Datasets (offline, built into scikit-learn) and your own data
`load_diabetes` (regression) · `load_breast_cancer` (binary) · `load_wine`, `load_digits` (multi-class) · `make_moons`, `make_blobs` (clusters) · **your own:** `data/` sales data and the HRM payslip data in `hrm_detective/` and `hrm_app/`.

---

## 📚 Table of contents

| Part (category) | File | Chapters | Days |
|---|---|---|---|
| **PART I — Start Here: the ML workflow, your first look at data, correlation** | [part1_start_here.md](part1_start_here.md) | Ch 1 — The ML workflow: baseline, split, metric, error (D1)<br>Ch 2 — First look at data: EDA and descriptive statistics (D2)<br>Ch 3 — Correlation: do two columns move together? (D3) | 1–3 |
| **PART II — Supervised Learning (a): Regression** | [part2_supervised_regression.md](part2_supervised_regression.md) | Ch 4 — Linear regression: from one line to many features (D4–8)<br>Ch 5 — Preparing data for regression (D9–11)<br>Ch 6 — Measuring a regression model and bias–variance (D12–13)<br>Ch 7 — Regularization, polynomial features and the checkpoint (D14–15) | 4–15 |
| **PART III — Supervised Learning (b): Classification** | [part3_supervised_classification.md](part3_supervised_classification.md) | Ch 8 — Logistic regression and softmax (D16–19)<br>Ch 9 — Classification metrics, imbalance and thresholds (D20–22)<br>Ch 10 — K-Nearest Neighbours and distance metrics (D23)<br>Ch 11 — Generative classifiers: Naive Bayes, LDA, QDA (D24)<br>Ch 12 — Support vector machines (SVC and SVR) (D25)<br>Ch 13 — Choosing between models (shoot-out) (D26)<br>Ch 14 — Decision trees (D27–28)<br>Ch 15 — Bagging, Random Forest and Extra Trees (D29)<br>Ch 16 — Boosting: AdaBoost → Gradient Boosting → XGBoost / LightGBM / CatBoost (D30–32)<br>Ch 17 — Stacking, voting and blending (D33) | 16–33 |
| **PART IV — Unsupervised Learning** | [part4_unsupervised.md](part4_unsupervised.md) | Ch 18 — Clustering (D34–35)<br>Ch 19 — Dimensionality reduction and feature selection (D36–38)<br>Ch 20 — Anomaly detection (D39) | 34–39 |
| **PART V — Evaluate, Tune & Special ML** | [part5_evaluation_special_ml.md](part5_evaluation_special_ml.md) | Ch 21 — Cross-validation and honest evaluation (D40)<br>Ch 22 — Hyper-parameter tuning (D41)<br>Ch 23 — Explainability, error analysis and fairness (D42)<br>Ch 24 — Time series (D43–44)<br>Ch 25 — Recommender systems (D45)<br>Ch 26 — A/B testing and causal thinking (D46)<br>Ch 27 — Classical-ML mock interview (D47) | 40–47 |
| **PART VI — Deep Learning and Computer Vision** | [part6_deep_learning_vision.md](part6_deep_learning_vision.md) | Ch 28 — Neural-network foundations (by hand) (D48–52)<br>Ch 29 — PyTorch and the training loop (D53–54)<br>Ch 30 — Training better: optimizers, regularization, debugging (D55–57)<br>Ch 31 — Keras / TensorFlow and tabular deep learning (D58–59)<br>Ch 32 — Computer vision (D60–62) | 48–62 |
| **PART VII — Natural Language Processing (NLP)** | [part7_nlp.md](part7_nlp.md) | Ch 33 — Text basics: cleaning, bag-of-words, TF-IDF, vector space (D63–64)<br>Ch 34 — Word embeddings (D65)<br>Ch 35 — Sequence models: RNN, LSTM, GRU, seq2seq, attention (D66–68)<br>Ch 36 — Transformers, BERT and fine-tuning (D69–73) | 63–73 |
| **PART VIII — Reinforcement Learning** | [part8_reinforcement_learning.md](part8_reinforcement_learning.md) | Ch 37 — RL basics: MDP, Bellman, Q-learning (D74)<br>Ch 38 — Deep RL: DQN, policy gradient, PPO (D75)<br>Ch 39 — RL for language models (D76) | 74–76 |
| **PART IX — Generative AI and Large Language Models: foundations** | [part9_generative_ai.md](part9_generative_ai.md) | Ch 40 — How LLMs work + a tiny GPT (D77–79)<br>Ch 41 — Using LLMs: APIs and prompt engineering (D80–81) | 77–81 |
| **PART X — Embeddings, Vector Databases, Retrievers and Augmentation (RAG)** | [part10_embeddings_vector_retrieval_rag.md](part10_embeddings_vector_retrieval_rag.md) | Ch 42 — Vectorization and embeddings (D82–83)<br>Ch 43 — Vector databases (D84–86)<br>Ch 44 — Retrievers (D87–89)<br>Ch 45 — Augmentation and generation (RAG) (D90–93) | 82–93 |
| **PART XI — Customizing and Shipping Generative AI: fine-tuning, image / audio generation, safety** | [part11_llm_customization.md](part11_llm_customization.md) | Ch 46 — Fine-tuning LLMs (D94–95)<br>Ch 47 — Image, audio and multimodal generation (D96)<br>Ch 48 — Safety, evaluation, cost and the GenAI project (D97–98) | 94–98 |
| **PART XII — Agentic AI** | [part12_agentic_ai.md](part12_agentic_ai.md) | Ch 49 — Agent fundamentals: tool calling, planning, memory (D99–101)<br>Ch 50 — Frameworks and protocols: LangChain, LangGraph, MCP (D102–103)<br>Ch 51 — Agent evaluation, guardrails and safety (D104)<br>Ch 52 — Multi-agent systems (D105–109)<br>Ch 53 — Build: the HRM payslip agent and an end-to-end agent (D110–111) | 99–111 |
| **PART XIII — Software Engineering with AI/ML (MLOps)** | [part13_software_engineering_mlops.md](part13_software_engineering_mlops.md) | Ch 54 — Serving a model and securing the API (D112–113)<br>Ch 55 — Production Python for AI projects (D114)<br>Ch 56 — Data and storage for AI apps (D115)<br>Ch 57 — Packaging and delivery: Docker, Git, CI/CD, testing (D116–118)<br>Ch 58 — Async work and caching (D119)<br>Ch 59 — Front-end for AI apps (D120)<br>Ch 60 — Experiment tracking, reproducibility and monitoring (D121–122)<br>Ch 61 — Big data and cloud (D123–125) | 112–125 |
| **PART XIV — System Design, Interview and Capstone** | [part14_design_interview_capstone.md](part14_design_interview_capstone.md) | Ch 62 — ML and LLM system design (D126–127)<br>Ch 63 — Capstone: Intelligent HRM Assistant (D128–132)<br>Ch 64 — Interview and portfolio (D133–134) | 126–134 |
| **PART XV — Advanced Shelf ☆ (optional, Days 135–196)** | [part15_advanced_shelf.md](part15_advanced_shelf.md) | Ch S1 — Classical and statistical machine learning (D135–147)<br>Ch S2 — Unsupervised learning and optimization (D148–154)<br>Ch S3 — Deep-learning extensions (D155–163)<br>Ch S4 — NLP and LLM extensions (D164–173)<br>Ch S5 — Reinforcement-learning and agent extensions (D174–180)<br>Ch S6 — Engineering and career (D181–196) | 135–196 |
| **Appendices** (math map · data-prep map · algorithm cheat-sheet · gap audit · trackers · resources) | [appendix.md](appendix.md) | A–F | — |

---

## 🗓️ Day 1–196 schedule

**Core path = Days 1–134.** Shelf ☆ = Days 135–196 (optional). Click a day to open it.

| Day | Part | Chapter | Level | Topic |
|---|---|---|---|---|
| [1](part1_start_here.md#day-1) | I · Start Here | 1 · The ML workflow: baseline, split, metric, error | L1–3 | Setup + the ML workflow (baseline, split, metric, error) |
| [2](part1_start_here.md#day-2) | I · Start Here | 2 · First look at data: EDA and descriptive statistics | L1–3 | First look at data: EDA + descriptive statistics |
| [3](part1_start_here.md#day-3) | I · Start Here | 3 · Correlation: do two columns move together? | L1–3 | Correlation & covariance (Pearson r) — *your notes: Correlation* |
| [4](part2_supervised_regression.md#day-4) | II · Supervised Learning (a) | 4 · Linear regression: from one line to many features | L1 | Simple linear regression: the line & the residual — *your notes: Pandas + Simple Linear Regression + Residuals* |
| [5](part2_supervised_regression.md#day-5) | II · Supervised Learning (a) | 4 · Linear regression: from one line to many features | L1 | Cost function + derivatives — *your notes: Loss Functions, Partial Derivatives & GD* |
| [6](part2_supervised_regression.md#day-6) | II · Supervised Learning (a) | 4 · Linear regression: from one line to many features | L2 | Gradient descent for linear regression — *your notes: Gradient Descent* |
| [7](part2_supervised_regression.md#day-7) | II · Supervised Learning (a) | 4 · Linear regression: from one line to many features | L2 | Vectors & matrices ➜ multiple regression and the normal equation |
| [8](part2_supervised_regression.md#day-8) | II · Supervised Learning (a) | 4 · Linear regression: from one line to many features | L3 | Assumptions, statsmodels and p-values — *your notes: Linear Regression* |
| [9](part2_supervised_regression.md#day-9) | II · Supervised Learning (a) | 5 · Preparing data for regression | L1 | Missing values & outliers |
| [10](part2_supervised_regression.md#day-10) | II · Supervised Learning (a) | 5 · Preparing data for regression | L2 | Encoding (7 types) — *your notes: Encoding* |
| [11](part2_supervised_regression.md#day-11) | II · Supervised Learning (a) | 5 · Preparing data for regression | L3 | Scaling & transformation (5 types) — *your notes: Transformation* |
| [12](part2_supervised_regression.md#day-12) | II · Supervised Learning (a) | 6 · Measuring a regression model and bias–variance | L1–2 | Regression metrics |
| [13](part2_supervised_regression.md#day-13) | II · Supervised Learning (a) | 6 · Measuring a regression model and bias–variance | L3 | Overfitting, underfitting & bias–variance — *your notes: Bias-Variance* |
| [14](part2_supervised_regression.md#day-14) | II · Supervised Learning (a) | 7 · Regularization, polynomial features and the checkpoint | L1–3 | Regularization (Ridge, Lasso, ElasticNet) + polynomial features |
| [15](part2_supervised_regression.md#day-15) | II · Supervised Learning (a) | 7 · Regularization, polynomial features and the checkpoint | CP | Regression checkpoint: pipeline + "Price predictor" |
| [16](part3_supervised_classification.md#day-16) | III · Supervised Learning (b) | 8 · Logistic regression and softmax | L1 | Probability, Bayes and distributions — and what "classification" means |
| [17](part3_supervised_classification.md#day-17) | III · Supervised Learning (b) | 8 · Logistic regression and softmax | L1 | Logistic regression I: odds, log-odds and the sigmoid |
| [18](part3_supervised_classification.md#day-18) | III · Supervised Learning (b) | 8 · Logistic regression and softmax | L2 | Logistic regression II: likelihood, log loss and training from scratch |
| [19](part3_supervised_classification.md#day-19) | III · Supervised Learning (b) | 8 · Logistic regression and softmax | L3 | Multi-class: softmax |
| [20](part3_supervised_classification.md#day-20) | III · Supervised Learning (b) | 9 · Classification metrics, imbalance and thresholds | L1 | Classification metrics |
| [21](part3_supervised_classification.md#day-21) | III · Supervised Learning (b) | 9 · Classification metrics, imbalance and thresholds | L2 | Imbalanced data & data leakage |
| [22](part3_supervised_classification.md#day-22) | III · Supervised Learning (b) | 9 · Classification metrics, imbalance and thresholds | L3 | Thresholds & calibration |
| [23](part3_supervised_classification.md#day-23) | III · Supervised Learning (b) | 10 · K-Nearest Neighbours and distance metrics | L1–3 | K-Nearest Neighbours and distance metrics — *your notes: Distance Metrics* |
| [24](part3_supervised_classification.md#day-24) | III · Supervised Learning (b) | 11 · Generative classifiers: Naive Bayes, LDA, QDA | L1–3 | Generative classifiers: Naive Bayes, LDA and QDA |
| [25](part3_supervised_classification.md#day-25) | III · Supervised Learning (b) | 12 · Support vector machines (SVC and SVR) | L1–3 | Support vector machines (SVC) and support vector regression (SVR) |
| [26](part3_supervised_classification.md#day-26) | III · Supervised Learning (b) | 13 · Choosing between models (shoot-out) | L1–3 | Model shoot-out |
| [27](part3_supervised_classification.md#day-27) | III · Supervised Learning (b) | 14 · Decision trees | L1 | Decision tree: how a split is chosen — *your notes: Decision Tree* |
| [28](part3_supervised_classification.md#day-28) | III · Supervised Learning (b) | 14 · Decision trees | L2–3 | Tree from scratch, overfitting & pruning |
| [29](part3_supervised_classification.md#day-29) | III · Supervised Learning (b) | 15 · Bagging, Random Forest and Extra Trees | L1–3 | Bagging, Random Forest & Extra Trees — *your notes: Random Forest* |
| [30](part3_supervised_classification.md#day-30) | III · Supervised Learning (b) | 16 · Boosting: AdaBoost → Gradient Boosting → XGBoost / LightGBM / CatBoost | L1 | AdaBoost |
| [31](part3_supervised_classification.md#day-31) | III · Supervised Learning (b) | 16 · Boosting: AdaBoost → Gradient Boosting → XGBoost / LightGBM / CatBoost | L2 | Gradient Boosting |
| [32](part3_supervised_classification.md#day-32) | III · Supervised Learning (b) | 16 · Boosting: AdaBoost → Gradient Boosting → XGBoost / LightGBM / CatBoost | L3 | XGBoost, LightGBM, CatBoost (+ HistGradientBoosting) |
| [33](part3_supervised_classification.md#day-33) | III · Supervised Learning (b) | 17 · Stacking, voting and blending | L1–3 | Stacking, voting, blending |
| [34](part4_unsupervised.md#day-34) | IV · Unsupervised Learning | 18 · Clustering | L1 | K-Means |
| [35](part4_unsupervised.md#day-35) | IV · Unsupervised Learning | 18 · Clustering | L2–3 | Hierarchical, DBSCAN, Gaussian Mixture |
| [36](part4_unsupervised.md#day-36) | IV · Unsupervised Learning | 19 · Dimensionality reduction and feature selection | L1 | Eigenvectors, covariance matrix & SVD (the maths behind PCA) |
| [37](part4_unsupervised.md#day-37) | IV · Unsupervised Learning | 19 · Dimensionality reduction and feature selection | L2 | PCA from scratch + LDA vs PCA + t-SNE / UMAP |
| [38](part4_unsupervised.md#day-38) | IV · Unsupervised Learning | 19 · Dimensionality reduction and feature selection | L3 | Feature selection vs feature extraction |
| [39](part4_unsupervised.md#day-39) | IV · Unsupervised Learning | 20 · Anomaly detection | L1–3 | Anomaly detection |
| [40](part5_evaluation_special_ml.md#day-40) | V · Evaluate, Tune & Special ML | 21 · Cross-validation and honest evaluation | L1–3 | Cross-validation & honest evaluation |
| [41](part5_evaluation_special_ml.md#day-41) | V · Evaluate, Tune & Special ML | 22 · Hyper-parameter tuning | L1–3 | Hyper-parameter tuning |
| [42](part5_evaluation_special_ml.md#day-42) | V · Evaluate, Tune & Special ML | 23 · Explainability, error analysis and fairness | L1–3 | Explainability, error analysis, fairness |
| [43](part5_evaluation_special_ml.md#day-43) | V · Evaluate, Tune & Special ML | 24 · Time series | L1–2 | Time series I: trend, seasonality, ACF/PACF and ARIMA |
| [44](part5_evaluation_special_ml.md#day-44) | V · Evaluate, Tune & Special ML | 24 · Time series | L3 | Time series II: lag features, boosting, Prophet and backtesting |
| [45](part5_evaluation_special_ml.md#day-45) | V · Evaluate, Tune & Special ML | 25 · Recommender systems | L1–3 | Recommender systems |
| [46](part5_evaluation_special_ml.md#day-46) | V · Evaluate, Tune & Special ML | 26 · A/B testing and causal thinking | L1–3 | A/B tests and causal thinking |
| [47](part5_evaluation_special_ml.md#day-47) | V · Evaluate, Tune & Special ML | 27 · Classical-ML mock interview | CP | Classical-ML mock interview (Parts II–V checkpoint) |
| [48](part6_deep_learning_vision.md#day-48) | VI · Deep Learning and Computer Vision | 28 · Neural-network foundations (by hand) | L1 | The neuron & the perceptron |
| [49](part6_deep_learning_vision.md#day-49) | VI · Deep Learning and Computer Vision | 28 · Neural-network foundations (by hand) | L1 | Multi-layer network: forward pass & activations |
| [50](part6_deep_learning_vision.md#day-50) | VI · Deep Learning and Computer Vision | 28 · Neural-network foundations (by hand) | L2 | Loss functions — *your notes: Loss Functions* |
| [51](part6_deep_learning_vision.md#day-51) | VI · Deep Learning and Computer Vision | 28 · Neural-network foundations (by hand) | L2 | Backpropagation by hand |
| [52](part6_deep_learning_vision.md#day-52) | VI · Deep Learning and Computer Vision | 28 · Neural-network foundations (by hand) | L3 | Neural network from scratch (NumPy) |
| [53](part6_deep_learning_vision.md#day-53) | VI · Deep Learning and Computer Vision | 29 · PyTorch and the training loop | L1–2 | PyTorch basics |
| [54](part6_deep_learning_vision.md#day-54) | VI · Deep Learning and Computer Vision | 29 · PyTorch and the training loop | L3 | The training loop & MNIST |
| [55](part6_deep_learning_vision.md#day-55) | VI · Deep Learning and Computer Vision | 30 · Training better: optimizers, regularization, debugging | L1 | Optimizers & learning-rate schedules |
| [56](part6_deep_learning_vision.md#day-56) | VI · Deep Learning and Computer Vision | 30 · Training better: optimizers, regularization, debugging | L2 | Regularization in deep learning |
| [57](part6_deep_learning_vision.md#day-57) | VI · Deep Learning and Computer Vision | 30 · Training better: optimizers, regularization, debugging | L3 | Debugging training & experiment logs |
| [58](part6_deep_learning_vision.md#day-58) | VI · Deep Learning and Computer Vision | 31 · Keras / TensorFlow and tabular deep learning | L2 | TensorFlow / Keras (same model, second framework) |
| [59](part6_deep_learning_vision.md#day-59) | VI · Deep Learning and Computer Vision | 31 · Keras / TensorFlow and tabular deep learning | L3 | Tabular deep learning vs boosting |
| [60](part6_deep_learning_vision.md#day-60) | VI · Deep Learning and Computer Vision | 32 · Computer vision | L1 | Convolution & the CNN |
| [61](part6_deep_learning_vision.md#day-61) | VI · Deep Learning and Computer Vision | 32 · Computer vision | L2 | CIFAR-10, augmentation & transfer learning |
| [62](part6_deep_learning_vision.md#day-62) | VI · Deep Learning and Computer Vision | 32 · Computer vision | L3 | Detection, segmentation, ViT |
| [63](part7_nlp.md#day-63) | VII · Natural Language Processing (NLP) | 33 · Text basics: cleaning, bag-of-words, TF-IDF, vector space | L1 | Text preprocessing |
| [64](part7_nlp.md#day-64) | VII · Natural Language Processing (NLP) | 33 · Text basics: cleaning, bag-of-words, TF-IDF, vector space | L2–3 | Bag-of-words, TF-IDF & classic text classification |
| [65](part7_nlp.md#day-65) | VII · Natural Language Processing (NLP) | 34 · Word embeddings | L1–3 | Word embeddings: Word2Vec, GloVe, FastText |
| [66](part7_nlp.md#day-66) | VII · Natural Language Processing (NLP) | 35 · Sequence models: RNN, LSTM, GRU, seq2seq, attention | L1 | Recurrent neural networks |
| [67](part7_nlp.md#day-67) | VII · Natural Language Processing (NLP) | 35 · Sequence models: RNN, LSTM, GRU, seq2seq, attention | L2 | LSTM & GRU |
| [68](part7_nlp.md#day-68) | VII · Natural Language Processing (NLP) | 35 · Sequence models: RNN, LSTM, GRU, seq2seq, attention | L3 | Sequence-to-sequence & attention |
| [69](part7_nlp.md#day-69) | VII · Natural Language Processing (NLP) | 36 · Transformers, BERT and fine-tuning | L1–2 | Self-attention & the Transformer (from scratch) |
| [70](part7_nlp.md#day-70) | VII · Natural Language Processing (NLP) | 36 · Transformers, BERT and fine-tuning | L2 | BERT, GPT, T5 & Hugging Face |
| [71](part7_nlp.md#day-71) | VII · Natural Language Processing (NLP) | 36 · Transformers, BERT and fine-tuning | L3 | Fine-tune BERT |
| [72](part7_nlp.md#day-72) | VII · Natural Language Processing (NLP) | 36 · Transformers, BERT and fine-tuning | L3 | NER, QA, summarization, translation & NLP metrics |
| [73](part7_nlp.md#day-73) | VII · Natural Language Processing (NLP) | 36 · Transformers, BERT and fine-tuning | L3 | NLP project |
| [74](part8_reinforcement_learning.md#day-74) | VIII · Reinforcement Learning | 37 · RL basics: MDP, Bellman, Q-learning | L1–3 | MDP, Bellman equation & Q-learning |
| [75](part8_reinforcement_learning.md#day-75) | VIII · Reinforcement Learning | 38 · Deep RL: DQN, policy gradient, PPO | L1–3 | DQN, policy gradient, PPO |
| [76](part8_reinforcement_learning.md#day-76) | VIII · Reinforcement Learning | 39 · RL for language models | L1–3 | RL for language models |
| [77](part9_generative_ai.md#day-77) | IX · Generative AI and Large Language Models | 40 · How LLMs work + a tiny GPT | L1 | How an LLM really works |
| [78](part9_generative_ai.md#day-78) | IX · Generative AI and Large Language Models | 40 · How LLMs work + a tiny GPT | L2 | Tiny GPT, part 1: attention block |
| [79](part9_generative_ai.md#day-79) | IX · Generative AI and Large Language Models | 40 · How LLMs work + a tiny GPT | L3 | Tiny GPT, part 2: train, sample, decode |
| [80](part9_generative_ai.md#day-80) | IX · Generative AI and Large Language Models | 41 · Using LLMs: APIs and prompt engineering | L1–2 | LLM APIs and local models: messages, streaming, cost |
| [81](part9_generative_ai.md#day-81) | IX · Generative AI and Large Language Models | 41 · Using LLMs: APIs and prompt engineering | L3 | Prompt engineering & structured output |
| [82](part10_embeddings_vector_retrieval_rag.md#day-82) | X · Embeddings, Vector Databases, Retrievers and Augmentation (RAG) | 42 · Vectorization and embeddings | L1 | Vectorization: from words to vectors (the ladder) |
| [83](part10_embeddings_vector_retrieval_rag.md#day-83) | X · Embeddings, Vector Databases, Retrievers and Augmentation (RAG) | 42 · Vectorization and embeddings | L2–3 | Embedding models: how they are trained, chosen and fine-tuned |
| [84](part10_embeddings_vector_retrieval_rag.md#day-84) | X · Embeddings, Vector Databases, Retrievers and Augmentation (RAG) | 43 · Vector databases | L1 | Vector search from scratch: exact nearest neighbours |
| [85](part10_embeddings_vector_retrieval_rag.md#day-85) | X · Embeddings, Vector Databases, Retrievers and Augmentation (RAG) | 43 · Vector databases | L2 | Approximate nearest-neighbour (ANN) indexes: IVF, PQ, HNSW |
| [86](part10_embeddings_vector_retrieval_rag.md#day-86) | X · Embeddings, Vector Databases, Retrievers and Augmentation (RAG) | 43 · Vector databases | L3 | Vector databases: products, filtering and operations (FAISS, Chroma, pgvector, Qdrant) |
| [87](part10_embeddings_vector_retrieval_rag.md#day-87) | X · Embeddings, Vector Databases, Retrievers and Augmentation (RAG) | 44 · Retrievers | L1 | Ingestion: parsing and chunking documents |
| [88](part10_embeddings_vector_retrieval_rag.md#day-88) | X · Embeddings, Vector Databases, Retrievers and Augmentation (RAG) | 44 · Retrievers | L2 | Retrievers: sparse (BM25), dense and hybrid — and how to measure them |
| [89](part10_embeddings_vector_retrieval_rag.md#day-89) | X · Embeddings, Vector Databases, Retrievers and Augmentation (RAG) | 44 · Retrievers | L3 | Improving retrieval: query transformation, MMR and reranking |
| [90](part10_embeddings_vector_retrieval_rag.md#day-90) | X · Embeddings, Vector Databases, Retrievers and Augmentation (RAG) | 45 · Augmentation and generation (RAG) | L1 | Augmentation: building the prompt from retrieved context (RAG v1) |
| [91](part10_embeddings_vector_retrieval_rag.md#day-91) | X · Embeddings, Vector Databases, Retrievers and Augmentation (RAG) | 45 · Augmentation and generation (RAG) | L2 | Cited and conversational RAG |
| [92](part10_embeddings_vector_retrieval_rag.md#day-92) | X · Embeddings, Vector Databases, Retrievers and Augmentation (RAG) | 45 · Augmentation and generation (RAG) | L3 | RAG evaluation: retrieval vs generation |
| [93](part10_embeddings_vector_retrieval_rag.md#day-93) | X · Embeddings, Vector Databases, Retrievers and Augmentation (RAG) | 45 · Augmentation and generation (RAG) | L3 | Production RAG (checkpoint) |
| [94](part11_llm_customization.md#day-94) | XI · Customizing and Shipping Generative AI | 46 · Fine-tuning LLMs | L1–2 | Fine-tuning theory: SFT, LoRA, QLoRA |
| [95](part11_llm_customization.md#day-95) | XI · Customizing and Shipping Generative AI | 46 · Fine-tuning LLMs | L3 | LoRA fine-tuning project |
| [96](part11_llm_customization.md#day-96) | XI · Customizing and Shipping Generative AI | 47 · Image, audio and multimodal generation | L1–3 | Image generation, multimodal & speech |
| [97](part11_llm_customization.md#day-97) | XI · Customizing and Shipping Generative AI | 48 · Safety, evaluation, cost and the GenAI project | L2 | LLM safety, evaluation, cost & latency |
| [98](part11_llm_customization.md#day-98) | XI · Customizing and Shipping Generative AI | 48 · Safety, evaluation, cost and the GenAI project | L3 | GenAI project |
| [99](part12_agentic_ai.md#day-99) | XII · Agentic AI | 49 · Agent fundamentals: tool calling, planning, memory | L1 | Tool calling & the agent loop (no framework) |
| [100](part12_agentic_ai.md#day-100) | XII · Agentic AI | 49 · Agent fundamentals: tool calling, planning, memory | L2 | ReAct, planning & task decomposition |
| [101](part12_agentic_ai.md#day-101) | XII · Agentic AI | 49 · Agent fundamentals: tool calling, planning, memory | L3 | Memory & context engineering |
| [102](part12_agentic_ai.md#day-102) | XII · Agentic AI | 50 · Frameworks and protocols: LangChain, LangGraph, MCP | L2 | LangChain & LangGraph |
| [103](part12_agentic_ai.md#day-103) | XII · Agentic AI | 50 · Frameworks and protocols: LangChain, LangGraph, MCP | L3 | MCP: Model Context Protocol |
| [104](part12_agentic_ai.md#day-104) | XII · Agentic AI | 51 · Agent evaluation, guardrails and safety | L1–3 | Agent evaluation, guardrails & safety |
| [105](part12_agentic_ai.md#day-105) | XII · Agentic AI | 52 · Multi-agent systems | L1 | Multi-agent I: when to use it, and which architecture |
| [106](part12_agentic_ai.md#day-106) | XII · Agentic AI | 52 · Multi-agent systems | L2 | Multi-agent II: communication, shared state and contracts |
| [107](part12_agentic_ai.md#day-107) | XII · Agentic AI | 52 · Multi-agent systems | L2 | Multi-agent III: frameworks side by side (LangGraph, CrewAI, AutoGen, agent SDKs) |
| [108](part12_agentic_ai.md#day-108) | XII · Agentic AI | 52 · Multi-agent systems | L3 | Multi-agent IV: reliability, cost control and security |
| [109](part12_agentic_ai.md#day-109) | XII · Agentic AI | 52 · Multi-agent systems | L3 | Multi-agent project (checkpoint): the HR assistant crew |
| [110](part12_agentic_ai.md#day-110) | XII · Agentic AI | 53 · Build: the HRM payslip agent and an end-to-end agent | L3 | Build: the HRM payslip agent |
| [111](part12_agentic_ai.md#day-111) | XII · Agentic AI | 53 · Build: the HRM payslip agent and an end-to-end agent | L3 | Agent project |
| [112](part13_software_engineering_mlops.md#day-112) | XIII · Software Engineering with AI/ML (MLOps) | 54 · Serving a model and securing the API | L1–2 | Serve a model with FastAPI |
| [113](part13_software_engineering_mlops.md#day-113) | XIII · Software Engineering with AI/ML (MLOps) | 54 · Serving a model and securing the API | L3 | API security: auth, rate limits, secrets |
| [114](part13_software_engineering_mlops.md#day-114) | XIII · Software Engineering with AI/ML (MLOps) | 55 · Production Python for AI projects | L1–3 | Production Python for AI projects |
| [115](part13_software_engineering_mlops.md#day-115) | XIII · Software Engineering with AI/ML (MLOps) | 56 · Data and storage for AI apps | L1–3 | Databases inside AI apps (PostgreSQL, pgvector) |
| [116](part13_software_engineering_mlops.md#day-116) | XIII · Software Engineering with AI/ML (MLOps) | 57 · Packaging and delivery: Docker, Git, CI/CD, testing | L1 | Docker & docker-compose |
| [117](part13_software_engineering_mlops.md#day-117) | XIII · Software Engineering with AI/ML (MLOps) | 57 · Packaging and delivery: Docker, Git, CI/CD, testing | L2 | Git workflow & CI/CD |
| [118](part13_software_engineering_mlops.md#day-118) | XIII · Software Engineering with AI/ML (MLOps) | 57 · Packaging and delivery: Docker, Git, CI/CD, testing | L3 | Testing ML & LLM code |
| [119](part13_software_engineering_mlops.md#day-119) | XIII · Software Engineering with AI/ML (MLOps) | 58 · Async work and caching | L1–2 | Async work: Redis, Celery, caching |
| [120](part13_software_engineering_mlops.md#day-120) | XIII · Software Engineering with AI/ML (MLOps) | 59 · Front-end for AI apps | L1–3 | Front-end for AI apps: a streaming chat UI |
| [121](part13_software_engineering_mlops.md#day-121) | XIII · Software Engineering with AI/ML (MLOps) | 60 · Experiment tracking, reproducibility and monitoring | L2 | MLflow, DVC & reproducibility |
| [122](part13_software_engineering_mlops.md#day-122) | XIII · Software Engineering with AI/ML (MLOps) | 60 · Experiment tracking, reproducibility and monitoring | L3 | Monitoring, drift & LLM tracing |
| [123](part13_software_engineering_mlops.md#day-123) | XIII · Software Engineering with AI/ML (MLOps) | 61 · Big data and cloud | L2 | PySpark, part 1 |
| [124](part13_software_engineering_mlops.md#day-124) | XIII · Software Engineering with AI/ML (MLOps) | 61 · Big data and cloud | L2 | PySpark, part 2 |
| [125](part13_software_engineering_mlops.md#day-125) | XIII · Software Engineering with AI/ML (MLOps) | 61 · Big data and cloud | L3 | Cloud deploy |
| [126](part14_design_interview_capstone.md#day-126) | XIV · System Design, Interview and Capstone | 62 · ML and LLM system design | L1–2 | ML system design, part 1 |
| [127](part14_design_interview_capstone.md#day-127) | XIV · System Design, Interview and Capstone | 62 · ML and LLM system design | L3 | ML / LLM system design, part 2 + the design doc |
| [128](part14_design_interview_capstone.md#day-128) | XIV · System Design, Interview and Capstone | 63 · Capstone: Intelligent HRM Assistant | L1 | Capstone design: **Intelligent HRM Assistant** |
| [129](part14_design_interview_capstone.md#day-129) | XIV · System Design, Interview and Capstone | 63 · Capstone: Intelligent HRM Assistant | L2 | Capstone build 1: model + RAG |
| [130](part14_design_interview_capstone.md#day-130) | XIV · System Design, Interview and Capstone | 63 · Capstone: Intelligent HRM Assistant | L2 | Capstone build 2: agent + API + UI |
| [131](part14_design_interview_capstone.md#day-131) | XIV · System Design, Interview and Capstone | 63 · Capstone: Intelligent HRM Assistant | L3 | Capstone build 3: ship it |
| [132](part14_design_interview_capstone.md#day-132) | XIV · System Design, Interview and Capstone | 63 · Capstone: Intelligent HRM Assistant | L3 | Polish & document |
| [133](part14_design_interview_capstone.md#day-133) | XIV · System Design, Interview and Capstone | 64 · Interview and portfolio | L3 | Full mock interview |
| [134](part14_design_interview_capstone.md#day-134) | XIV · System Design, Interview and Capstone | 64 · Interview and portfolio | L3 | Portfolio & **gap audit** |
| [135](part15_advanced_shelf.md#day-135) | XV · Advanced Shelf ☆ | S1 · Classical and statistical machine learning | L3 | ☆ Robust & quantile regression |
| [136](part15_advanced_shelf.md#day-136) | XV · Advanced Shelf ☆ | S1 · Classical and statistical machine learning | L3 | ☆ Generalized linear models (GLM) and GAMs |
| [137](part15_advanced_shelf.md#day-137) | XV · Advanced Shelf ☆ | S1 · Classical and statistical machine learning | L3 | ☆ Bayesian linear regression (MLE vs MAP vs full Bayes) |
| [138](part15_advanced_shelf.md#day-138) | XV · Advanced Shelf ☆ | S1 · Classical and statistical machine learning | L3 | ☆ Gaussian processes |
| [139](part15_advanced_shelf.md#day-139) | XV · Advanced Shelf ☆ | S1 · Classical and statistical machine learning | L3 | ☆ Kernel ridge regression and kernel PCA |
| [140](part15_advanced_shelf.md#day-140) | XV · Advanced Shelf ☆ | S1 · Classical and statistical machine learning | L3 | ☆ Ordinal, multi-label and cost-sensitive classification |
| [141](part15_advanced_shelf.md#day-141) | XV · Advanced Shelf ☆ | S1 · Classical and statistical machine learning | L3 | ☆ Conformal prediction: honest uncertainty |
| [142](part15_advanced_shelf.md#day-142) | XV · Advanced Shelf ☆ | S1 · Classical and statistical machine learning | L3 | ☆ Survival analysis (employee attrition, churn) |
| [143](part15_advanced_shelf.md#day-143) | XV · Advanced Shelf ☆ | S1 · Classical and statistical machine learning | L3 | ☆ Semi-supervised and active learning |
| [144](part15_advanced_shelf.md#day-144) | XV · Advanced Shelf ☆ | S1 · Classical and statistical machine learning | L3 | ☆ Online / streaming learning and concept drift |
| [145](part15_advanced_shelf.md#day-145) | XV · Advanced Shelf ☆ | S1 · Classical and statistical machine learning | L3 | ☆ Hidden Markov models and Kalman filters |
| [146](part15_advanced_shelf.md#day-146) | XV · Advanced Shelf ☆ | S1 · Classical and statistical machine learning | L3 | ☆ MCMC and variational inference |
| [147](part15_advanced_shelf.md#day-147) | XV · Advanced Shelf ☆ | S1 · Classical and statistical machine learning | L3 | ☆ Bayesian networks, causal graphs and uplift |
| [148](part15_advanced_shelf.md#day-148) | XV · Advanced Shelf ☆ | S2 · Unsupervised learning and optimization | L3 | ☆ More clustering: spectral, mean-shift, OPTICS/HDBSCAN, BIRCH, k-medoids |
| [149](part15_advanced_shelf.md#day-149) | XV · Advanced Shelf ☆ | S2 · Unsupervised learning and optimization | L3 | ☆ Matrix factorization and manifolds: NMF, ICA, LSA, Isomap, LLE, MDS |
| [150](part15_advanced_shelf.md#day-150) | XV · Advanced Shelf ☆ | S2 · Unsupervised learning and optimization | L3 | ☆ Association rules: Apriori and FP-Growth |
| [151](part15_advanced_shelf.md#day-151) | XV · Advanced Shelf ☆ | S2 · Unsupervised learning and optimization | L3 | ☆ Autoencoders and one-class anomaly detection |
| [152](part15_advanced_shelf.md#day-152) | XV · Advanced Shelf ☆ | S2 · Unsupervised learning and optimization | L3 | ☆ More time series: Holt-Winters, SARIMAX, VAR, state-space, foundation models |
| [153](part15_advanced_shelf.md#day-153) | XV · Advanced Shelf ☆ | S2 · Unsupervised learning and optimization | L3 | ☆ Optimization toolbox |
| [154](part15_advanced_shelf.md#day-154) | XV · Advanced Shelf ☆ | S2 · Unsupervised learning and optimization | L3 | ☆ AutoML and feature stores |
| [155](part15_advanced_shelf.md#day-155) | XV · Advanced Shelf ☆ | S3 · Deep-learning extensions | L3 | ☆ CNN architectures in code: LeNet → ConvNeXt |
| [156](part15_advanced_shelf.md#day-156) | XV · Advanced Shelf ☆ | S3 · Deep-learning extensions | L3 | ☆ Autoencoders, VAEs and contrastive learning |
| [157](part15_advanced_shelf.md#day-157) | XV · Advanced Shelf ☆ | S3 · Deep-learning extensions | L3 | ☆ Detection and segmentation deep dive |
| [158](part15_advanced_shelf.md#day-158) | XV · Advanced Shelf ☆ | S3 · Deep-learning extensions | L3 | ☆ The GAN family |
| [159](part15_advanced_shelf.md#day-159) | XV · Advanced Shelf ☆ | S3 · Deep-learning extensions | L3 | ☆ Diffusion models deep dive |
| [160](part15_advanced_shelf.md#day-160) | XV · Advanced Shelf ☆ | S3 · Deep-learning extensions | L3 | ☆ Graph neural networks and knowledge graphs |
| [161](part15_advanced_shelf.md#day-161) | XV · Advanced Shelf ☆ | S3 · Deep-learning extensions | L3 | ☆ State-space models (Mamba) and Mixture-of-Experts |
| [162](part15_advanced_shelf.md#day-162) | XV · Advanced Shelf ☆ | S3 · Deep-learning extensions | L3 | ☆ Efficient models: distillation, pruning, quantization |
| [163](part15_advanced_shelf.md#day-163) | XV · Advanced Shelf ☆ | S3 · Deep-learning extensions | L3 | ☆ Training at scale: GPUs, mixed precision, distributed training |
| [164](part15_advanced_shelf.md#day-164) | XV · Advanced Shelf ☆ | S4 · NLP and LLM extensions | L3 | ☆ Classic NLP models: n-gram LMs, CRF, HMM-POS, LDA topics, TextRank |
| [165](part15_advanced_shelf.md#day-165) | XV · Advanced Shelf ☆ | S4 · NLP and LLM extensions | L3 | ☆ The encoder family: RoBERTa, DeBERTa, sentence-transformers, ColBERT |
| [166](part15_advanced_shelf.md#day-166) | XV · Advanced Shelf ☆ | S4 · NLP and LLM extensions | L3 | ☆ Tokenizers deep dive |
| [167](part15_advanced_shelf.md#day-167) | XV · Advanced Shelf ☆ | S4 · NLP and LLM extensions | L3 | ☆ LLM internals: RoPE, GQA, FlashAttention, KV-cache, speculative decoding |
| [168](part15_advanced_shelf.md#day-168) | XV · Advanced Shelf ☆ | S4 · NLP and LLM extensions | L3 | ☆ Parameter-efficient fine-tuning variants |
| [169](part15_advanced_shelf.md#day-169) | XV · Advanced Shelf ☆ | S4 · NLP and LLM extensions | L3 | ☆ Alignment methods and reasoning models |
| [170](part15_advanced_shelf.md#day-170) | XV · Advanced Shelf ☆ | S4 · NLP and LLM extensions | L3 | ☆ Advanced RAG |
| [171](part15_advanced_shelf.md#day-171) | XV · Advanced Shelf ☆ | S4 · NLP and LLM extensions | L3 | ☆ LLM benchmarks, judges and human evaluation |
| [172](part15_advanced_shelf.md#day-172) | XV · Advanced Shelf ☆ | S4 · NLP and LLM extensions | L3 | ☆ Long context, memory and caching |
| [173](part15_advanced_shelf.md#day-173) | XV · Advanced Shelf ☆ | S4 · NLP and LLM extensions | L3 | ☆ Vision-language models and speech |
| [174](part15_advanced_shelf.md#day-174) | XV · Advanced Shelf ☆ | S5 · Reinforcement-learning and agent extensions | L3 | ☆ Bandits, Monte-Carlo and TD(λ) |
| [175](part15_advanced_shelf.md#day-175) | XV · Advanced Shelf ☆ | S5 · Reinforcement-learning and agent extensions | L3 | ☆ The deep-RL family: Double/Dueling DQN, Rainbow, A2C, DDPG, TD3, SAC, TRPO |
| [176](part15_advanced_shelf.md#day-176) | XV · Advanced Shelf ☆ | S5 · Reinforcement-learning and agent extensions | L3 | ☆ Model-based, offline, imitation and multi-agent RL |
| [177](part15_advanced_shelf.md#day-177) | XV · Advanced Shelf ☆ | S5 · Reinforcement-learning and agent extensions | L3 | ☆ Agent reasoning patterns: Reflexion, Tree-of-Thoughts, self-consistency |
| [178](part15_advanced_shelf.md#day-178) | XV · Advanced Shelf ☆ | S5 · Reinforcement-learning and agent extensions | L3 | ☆ Code agents and computer-use agents |
| [179](part15_advanced_shelf.md#day-179) | XV · Advanced Shelf ☆ | S5 · Reinforcement-learning and agent extensions | L3 | ☆ Durable workflows and A2A at scale |
| [180](part15_advanced_shelf.md#day-180) | XV · Advanced Shelf ☆ | S5 · Reinforcement-learning and agent extensions | L3 | ☆ Agent security: OWASP LLM Top-10 |
| [181](part15_advanced_shelf.md#day-181) | XV · Advanced Shelf ☆ | S6 · Engineering and career | L3 | ☆ Data engineering: Kafka, Airflow/Prefect, dbt |
| [182](part15_advanced_shelf.md#day-182) | XV · Advanced Shelf ☆ | S6 · Engineering and career | L3 | ☆ Serving at scale: vLLM, Triton, Ray Serve, Kubernetes |
| [183](part15_advanced_shelf.md#day-183) | XV · Advanced Shelf ☆ | S6 · Engineering and career | L3 | ☆ Python performance for ML engineers |
| [184](part15_advanced_shelf.md#day-184) | XV · Advanced Shelf ☆ | S6 · Engineering and career | L3 | ☆ Privacy and responsible AI |
| [185](part15_advanced_shelf.md#day-185) | XV · Advanced Shelf ☆ | S6 · Engineering and career | L3 | ☆ Recommenders, advanced |
| [186](part15_advanced_shelf.md#day-186) | XV · Advanced Shelf ☆ | S6 · Engineering and career | L3 | ☆ Search and learning-to-rank |
| [187](part15_advanced_shelf.md#day-187) | XV · Advanced Shelf ☆ | S6 · Engineering and career | L3 | ☆ Reading and reproducing a paper |
| [188](part15_advanced_shelf.md#day-188) | XV · Advanced Shelf ☆ | S6 · Engineering and career | L3 | ☆ Kaggle workflow |
| [189](part15_advanced_shelf.md#day-189) | XV · Advanced Shelf ☆ | S6 · Engineering and career | L3 | ☆ Coding-interview pack I: arrays, hashing, two-pointers, stack, heap |
| [190](part15_advanced_shelf.md#day-190) | XV · Advanced Shelf ☆ | S6 · Engineering and career | L3 | ☆ Coding-interview pack II: trees, graphs, DP and "ML from scratch" |
| [191](part15_advanced_shelf.md#day-191) | XV · Advanced Shelf ☆ | S6 · Engineering and career | L3 | ☆ Open source and writing in public |
| [192](part15_advanced_shelf.md#day-192) | XV · Advanced Shelf ☆ | S6 · Engineering and career | L3 | ☆ ML system design II (ranking, search, fraud at scale) |
| [193](part15_advanced_shelf.md#day-193) | XV · Advanced Shelf ☆ | S6 · Engineering and career | L3 | ☆ Behavioural interview, résumé and salary |
| [194](part15_advanced_shelf.md#day-194) | XV · Advanced Shelf ☆ | S6 · Engineering and career | L3 | ☆ Cloud for AI engineers: AWS, GCP and Azure |
| [195](part15_advanced_shelf.md#day-195) | XV · Advanced Shelf ☆ | S6 · Engineering and career | L3 | ☆ Infrastructure as code and FinOps |
| [196](part15_advanced_shelf.md#day-196) | XV · Advanced Shelf ☆ | S6 · Engineering and career | L3 | ☆ Final gap audit and your 12-month plan |

---

## ✅ Progress
Tick days inside each Part file (`☐` → `☑`). Part-level tracker: [Appendix E](appendix.md#e-trackers).

