# 📘 The AI & ML Engineer Book — 120 core days + 60 shelf days

> **For:** a learner who wants to become an advanced **AI / ML Engineer** — with **Supervised, Unsupervised, Deep Learning, NLP, Reinforcement Learning, Generative AI, Agentic AI** and **Software Engineering with AI/ML**.
> **How it is built:** like a book. **Parts** = categories (Supervised, Unsupervised, …). **Chapters** = one algorithm family. **Levels** = Beginner → Intermediate → Advanced *inside every chapter*. The **Day 1–120 schedule** at the bottom tells you what to read each day.
> **Pace:** 3–4 hours a day. Core path = Days 1–120 (job-ready). Shelf = Days 121–180 (optional, "be the best").
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
`★` core (Days 1–120) · `☆` shelf (Days 121–180) · `L1 / L2 / L3` level · `CP` checkpoint · 📘 = your class notes cover it.

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
| **PART IX — Generative AI and Large Language Models** | [part9_generative_ai.md](part9_generative_ai.md) | Ch 40 — How LLMs work + a tiny GPT (D77–79)<br>Ch 41 — Using LLMs: APIs and prompt engineering (D80–81)<br>Ch 42 — Retrieval-Augmented Generation (RAG) (D82–85)<br>Ch 43 — Fine-tuning LLMs (D86–87)<br>Ch 44 — Image, audio and multimodal generation (D88)<br>Ch 45 — Safety, evaluation, cost and the GenAI project (D89–90) | 77–90 |
| **PART X — Agentic AI** | [part10_agentic_ai.md](part10_agentic_ai.md) | Ch 46 — Agent fundamentals: tool calling, planning, memory (D91–93)<br>Ch 47 — Frameworks and protocols: LangChain, LangGraph, MCP (D94–95)<br>Ch 48 — Multi-agent systems (D96)<br>Ch 49 — Agent evaluation, guardrails and safety (D97)<br>Ch 50 — Build: the HRM payslip agent and an end-to-end agent (D98–99) | 91–99 |
| **PART XI — Software Engineering with AI/ML (MLOps)** | [part11_software_engineering_mlops.md](part11_software_engineering_mlops.md) | Ch 51 — Serving a model and securing the API (D100–101)<br>Ch 52 — Data and storage for AI apps (D102)<br>Ch 53 — Packaging and delivery: Docker, Git, CI/CD, testing (D103–105)<br>Ch 54 — Async work, MLOps and monitoring (D106–108)<br>Ch 55 — Big data and cloud (D109–111) | 100–111 |
| **PART XII — System Design, Interview and Capstone** | [part12_design_interview_capstone.md](part12_design_interview_capstone.md) | Ch 56 — ML and LLM system design (D112–113)<br>Ch 57 — Capstone: Intelligent HRM Assistant (D114–118)<br>Ch 58 — Interview and portfolio (D119–120) | 112–120 |
| **PART XIII — Advanced Shelf ☆ (optional, Days 121–180)** | [part13_advanced_shelf.md](part13_advanced_shelf.md) | Ch S1 — Classical and statistical machine learning (Days 121–133) (D121–133)<br>Ch S2 — Unsupervised learning and optimization (Days 134–140) (D134–140)<br>Ch S3 — Deep-learning extensions (Days 141–149) (D141–149)<br>Ch S4 — NLP and LLM extensions (Days 150–159) (D150–159)<br>Ch S5 — Reinforcement-learning and agent extensions (Days 160–166) (D160–166)<br>Ch S6 — Engineering and career (Days 167–180) (D167–180) | 121–180 |
| **Appendices** (math map · data-prep map · algorithm cheat-sheet · gap audit · trackers · resources) | [appendix.md](appendix.md) | A–F | — |

---

## 🗓️ Day 1–180 schedule

**Core path = Days 1–120.** Shelf ☆ = Days 121–180 (optional). Click a day to open it.

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
| [80](part9_generative_ai.md#day-80) | IX · Generative AI and Large Language Models | 41 · Using LLMs: APIs and prompt engineering | L1–2 | LLM APIs: messages, streaming, cost |
| [81](part9_generative_ai.md#day-81) | IX · Generative AI and Large Language Models | 41 · Using LLMs: APIs and prompt engineering | L3 | Prompt engineering & structured output |
| [82](part9_generative_ai.md#day-82) | IX · Generative AI and Large Language Models | 42 · Retrieval-Augmented Generation (RAG) | L1 | Embeddings & vector databases |
| [83](part9_generative_ai.md#day-83) | IX · Generative AI and Large Language Models | 42 · Retrieval-Augmented Generation (RAG) | L2 | RAG, version 1 |
| [84](part9_generative_ai.md#day-84) | IX · Generative AI and Large Language Models | 42 · Retrieval-Augmented Generation (RAG) | L2 | RAG, version 2: hybrid search, rerank, citations |
| [85](part9_generative_ai.md#day-85) | IX · Generative AI and Large Language Models | 42 · Retrieval-Augmented Generation (RAG) | L3 | RAG evaluation & improvement |
| [86](part9_generative_ai.md#day-86) | IX · Generative AI and Large Language Models | 43 · Fine-tuning LLMs | L1–2 | Fine-tuning theory: SFT, LoRA, QLoRA |
| [87](part9_generative_ai.md#day-87) | IX · Generative AI and Large Language Models | 43 · Fine-tuning LLMs | L3 | LoRA fine-tuning project |
| [88](part9_generative_ai.md#day-88) | IX · Generative AI and Large Language Models | 44 · Image, audio and multimodal generation | L1–3 | Image generation, multimodal & speech |
| [89](part9_generative_ai.md#day-89) | IX · Generative AI and Large Language Models | 45 · Safety, evaluation, cost and the GenAI project | L2 | LLM safety, evaluation, cost & latency |
| [90](part9_generative_ai.md#day-90) | IX · Generative AI and Large Language Models | 45 · Safety, evaluation, cost and the GenAI project | L3 | GenAI project |
| [91](part10_agentic_ai.md#day-91) | X · Agentic AI | 46 · Agent fundamentals: tool calling, planning, memory | L1 | Tool calling & the agent loop (no framework) |
| [92](part10_agentic_ai.md#day-92) | X · Agentic AI | 46 · Agent fundamentals: tool calling, planning, memory | L2 | ReAct, planning & task decomposition |
| [93](part10_agentic_ai.md#day-93) | X · Agentic AI | 46 · Agent fundamentals: tool calling, planning, memory | L3 | Memory & context engineering |
| [94](part10_agentic_ai.md#day-94) | X · Agentic AI | 47 · Frameworks and protocols: LangChain, LangGraph, MCP | L2 | LangChain & LangGraph |
| [95](part10_agentic_ai.md#day-95) | X · Agentic AI | 47 · Frameworks and protocols: LangChain, LangGraph, MCP | L3 | MCP: Model Context Protocol |
| [96](part10_agentic_ai.md#day-96) | X · Agentic AI | 48 · Multi-agent systems | L1–3 | Multi-agent systems |
| [97](part10_agentic_ai.md#day-97) | X · Agentic AI | 49 · Agent evaluation, guardrails and safety | L1–3 | Agent evaluation, guardrails & safety |
| [98](part10_agentic_ai.md#day-98) | X · Agentic AI | 50 · Build: the HRM payslip agent and an end-to-end agent | L3 | Build: the HRM payslip agent |
| [99](part10_agentic_ai.md#day-99) | X · Agentic AI | 50 · Build: the HRM payslip agent and an end-to-end agent | L3 | Agent project |
| [100](part11_software_engineering_mlops.md#day-100) | XI · Software Engineering with AI/ML (MLOps) | 51 · Serving a model and securing the API | L1–2 | Serve a model with FastAPI |
| [101](part11_software_engineering_mlops.md#day-101) | XI · Software Engineering with AI/ML (MLOps) | 51 · Serving a model and securing the API | L3 | API security: auth, rate limits, secrets |
| [102](part11_software_engineering_mlops.md#day-102) | XI · Software Engineering with AI/ML (MLOps) | 52 · Data and storage for AI apps | L1–3 | Databases inside AI apps (PostgreSQL, pgvector) |
| [103](part11_software_engineering_mlops.md#day-103) | XI · Software Engineering with AI/ML (MLOps) | 53 · Packaging and delivery: Docker, Git, CI/CD, testing | L1 | Docker & docker-compose |
| [104](part11_software_engineering_mlops.md#day-104) | XI · Software Engineering with AI/ML (MLOps) | 53 · Packaging and delivery: Docker, Git, CI/CD, testing | L2 | Git workflow & CI/CD |
| [105](part11_software_engineering_mlops.md#day-105) | XI · Software Engineering with AI/ML (MLOps) | 53 · Packaging and delivery: Docker, Git, CI/CD, testing | L3 | Testing ML & LLM code |
| [106](part11_software_engineering_mlops.md#day-106) | XI · Software Engineering with AI/ML (MLOps) | 54 · Async work, MLOps and monitoring | L1–2 | Async work: Redis, Celery, caching |
| [107](part11_software_engineering_mlops.md#day-107) | XI · Software Engineering with AI/ML (MLOps) | 54 · Async work, MLOps and monitoring | L2 | MLflow, DVC & reproducibility |
| [108](part11_software_engineering_mlops.md#day-108) | XI · Software Engineering with AI/ML (MLOps) | 54 · Async work, MLOps and monitoring | L3 | Monitoring, drift & LLM tracing |
| [109](part11_software_engineering_mlops.md#day-109) | XI · Software Engineering with AI/ML (MLOps) | 55 · Big data and cloud | L2 | PySpark, part 1 |
| [110](part11_software_engineering_mlops.md#day-110) | XI · Software Engineering with AI/ML (MLOps) | 55 · Big data and cloud | L2 | PySpark, part 2 |
| [111](part11_software_engineering_mlops.md#day-111) | XI · Software Engineering with AI/ML (MLOps) | 55 · Big data and cloud | L3 | Cloud deploy |
| [112](part12_design_interview_capstone.md#day-112) | XII · System Design, Interview and Capstone | 56 · ML and LLM system design | L1–2 | ML system design, part 1 |
| [113](part12_design_interview_capstone.md#day-113) | XII · System Design, Interview and Capstone | 56 · ML and LLM system design | L3 | ML / LLM system design, part 2 + the design doc |
| [114](part12_design_interview_capstone.md#day-114) | XII · System Design, Interview and Capstone | 57 · Capstone: Intelligent HRM Assistant | L1 | Capstone design: **Intelligent HRM Assistant** |
| [115](part12_design_interview_capstone.md#day-115) | XII · System Design, Interview and Capstone | 57 · Capstone: Intelligent HRM Assistant | L2 | Capstone build 1: model + RAG |
| [116](part12_design_interview_capstone.md#day-116) | XII · System Design, Interview and Capstone | 57 · Capstone: Intelligent HRM Assistant | L2 | Capstone build 2: agent + API + UI |
| [117](part12_design_interview_capstone.md#day-117) | XII · System Design, Interview and Capstone | 57 · Capstone: Intelligent HRM Assistant | L3 | Capstone build 3: ship it |
| [118](part12_design_interview_capstone.md#day-118) | XII · System Design, Interview and Capstone | 57 · Capstone: Intelligent HRM Assistant | L3 | Polish & document |
| [119](part12_design_interview_capstone.md#day-119) | XII · System Design, Interview and Capstone | 58 · Interview and portfolio | L3 | Full mock interview |
| [120](part12_design_interview_capstone.md#day-120) | XII · System Design, Interview and Capstone | 58 · Interview and portfolio | L3 | Portfolio & **gap audit** |
| [121](part13_advanced_shelf.md#day-121) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S1 · Classical and statistical machine learning (Days 121–133) | L3 | ☆ Robust & quantile regression ☆ |
| [122](part13_advanced_shelf.md#day-122) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S1 · Classical and statistical machine learning (Days 121–133) | L3 | ☆ Generalized linear models (GLM) and GAMs ☆ |
| [123](part13_advanced_shelf.md#day-123) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S1 · Classical and statistical machine learning (Days 121–133) | L3 | ☆ Bayesian linear regression (MLE vs MAP vs full Bayes) ☆ |
| [124](part13_advanced_shelf.md#day-124) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S1 · Classical and statistical machine learning (Days 121–133) | L3 | ☆ Gaussian processes ☆ |
| [125](part13_advanced_shelf.md#day-125) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S1 · Classical and statistical machine learning (Days 121–133) | L3 | ☆ Kernel ridge regression and kernel PCA ☆ |
| [126](part13_advanced_shelf.md#day-126) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S1 · Classical and statistical machine learning (Days 121–133) | L3 | ☆ Ordinal, multi-label and cost-sensitive classification ☆ |
| [127](part13_advanced_shelf.md#day-127) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S1 · Classical and statistical machine learning (Days 121–133) | L3 | ☆ Conformal prediction: honest uncertainty ☆ |
| [128](part13_advanced_shelf.md#day-128) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S1 · Classical and statistical machine learning (Days 121–133) | L3 | ☆ Survival analysis (employee attrition, churn) ☆ |
| [129](part13_advanced_shelf.md#day-129) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S1 · Classical and statistical machine learning (Days 121–133) | L3 | ☆ Semi-supervised and active learning ☆ |
| [130](part13_advanced_shelf.md#day-130) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S1 · Classical and statistical machine learning (Days 121–133) | L3 | ☆ Online / streaming learning and concept drift ☆ |
| [131](part13_advanced_shelf.md#day-131) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S1 · Classical and statistical machine learning (Days 121–133) | L3 | ☆ Hidden Markov models and Kalman filters ☆ |
| [132](part13_advanced_shelf.md#day-132) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S1 · Classical and statistical machine learning (Days 121–133) | L3 | ☆ MCMC and variational inference ☆ |
| [133](part13_advanced_shelf.md#day-133) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S1 · Classical and statistical machine learning (Days 121–133) | L3 | ☆ Bayesian networks, causal graphs and uplift ☆ |
| [134](part13_advanced_shelf.md#day-134) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S2 · Unsupervised learning and optimization (Days 134–140) | L3 | ☆ More clustering: spectral, mean-shift, OPTICS/HDBSCAN, BIRCH, k-medoids ☆ |
| [135](part13_advanced_shelf.md#day-135) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S2 · Unsupervised learning and optimization (Days 134–140) | L3 | ☆ Matrix factorization and manifolds: NMF, ICA, LSA, Isomap, LLE, MDS ☆ |
| [136](part13_advanced_shelf.md#day-136) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S2 · Unsupervised learning and optimization (Days 134–140) | L3 | ☆ Association rules: Apriori and FP-Growth ☆ |
| [137](part13_advanced_shelf.md#day-137) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S2 · Unsupervised learning and optimization (Days 134–140) | L3 | ☆ Autoencoders and one-class anomaly detection ☆ |
| [138](part13_advanced_shelf.md#day-138) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S2 · Unsupervised learning and optimization (Days 134–140) | L3 | ☆ More time series: Holt-Winters, SARIMAX, VAR, state-space, foundation models ☆ |
| [139](part13_advanced_shelf.md#day-139) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S2 · Unsupervised learning and optimization (Days 134–140) | L3 | ☆ Optimization toolbox ☆ |
| [140](part13_advanced_shelf.md#day-140) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S2 · Unsupervised learning and optimization (Days 134–140) | L3 | ☆ AutoML and feature stores ☆ |
| [141](part13_advanced_shelf.md#day-141) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S3 · Deep-learning extensions (Days 141–149) | L3 | ☆ CNN architectures in code: LeNet → ConvNeXt ☆ |
| [142](part13_advanced_shelf.md#day-142) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S3 · Deep-learning extensions (Days 141–149) | L3 | ☆ Autoencoders, VAEs and contrastive learning ☆ |
| [143](part13_advanced_shelf.md#day-143) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S3 · Deep-learning extensions (Days 141–149) | L3 | ☆ Detection and segmentation deep dive ☆ |
| [144](part13_advanced_shelf.md#day-144) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S3 · Deep-learning extensions (Days 141–149) | L3 | ☆ The GAN family ☆ |
| [145](part13_advanced_shelf.md#day-145) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S3 · Deep-learning extensions (Days 141–149) | L3 | ☆ Diffusion models deep dive ☆ |
| [146](part13_advanced_shelf.md#day-146) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S3 · Deep-learning extensions (Days 141–149) | L3 | ☆ Graph neural networks and knowledge graphs ☆ |
| [147](part13_advanced_shelf.md#day-147) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S3 · Deep-learning extensions (Days 141–149) | L3 | ☆ State-space models (Mamba) and Mixture-of-Experts ☆ |
| [148](part13_advanced_shelf.md#day-148) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S3 · Deep-learning extensions (Days 141–149) | L3 | ☆ Efficient models: distillation, pruning, quantization ☆ |
| [149](part13_advanced_shelf.md#day-149) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S3 · Deep-learning extensions (Days 141–149) | L3 | ☆ Training at scale: GPUs, mixed precision, distributed training ☆ |
| [150](part13_advanced_shelf.md#day-150) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S4 · NLP and LLM extensions (Days 150–159) | L3 | ☆ Classic NLP models: n-gram LMs, CRF, HMM-POS, LDA topics, TextRank ☆ |
| [151](part13_advanced_shelf.md#day-151) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S4 · NLP and LLM extensions (Days 150–159) | L3 | ☆ The encoder family: RoBERTa, DeBERTa, sentence-transformers, ColBERT ☆ |
| [152](part13_advanced_shelf.md#day-152) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S4 · NLP and LLM extensions (Days 150–159) | L3 | ☆ Tokenizers deep dive ☆ |
| [153](part13_advanced_shelf.md#day-153) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S4 · NLP and LLM extensions (Days 150–159) | L3 | ☆ LLM internals: RoPE, GQA, FlashAttention, KV-cache, speculative decoding ☆ |
| [154](part13_advanced_shelf.md#day-154) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S4 · NLP and LLM extensions (Days 150–159) | L3 | ☆ Parameter-efficient fine-tuning variants ☆ |
| [155](part13_advanced_shelf.md#day-155) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S4 · NLP and LLM extensions (Days 150–159) | L3 | ☆ Alignment methods and reasoning models ☆ |
| [156](part13_advanced_shelf.md#day-156) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S4 · NLP and LLM extensions (Days 150–159) | L3 | ☆ Advanced RAG ☆ |
| [157](part13_advanced_shelf.md#day-157) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S4 · NLP and LLM extensions (Days 150–159) | L3 | ☆ LLM benchmarks, judges and human evaluation ☆ |
| [158](part13_advanced_shelf.md#day-158) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S4 · NLP and LLM extensions (Days 150–159) | L3 | ☆ Long context, memory and caching ☆ |
| [159](part13_advanced_shelf.md#day-159) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S4 · NLP and LLM extensions (Days 150–159) | L3 | ☆ Vision-language models and speech ☆ |
| [160](part13_advanced_shelf.md#day-160) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S5 · Reinforcement-learning and agent extensions (Days 160–166) | L3 | ☆ Bandits, Monte-Carlo and TD(λ) ☆ |
| [161](part13_advanced_shelf.md#day-161) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S5 · Reinforcement-learning and agent extensions (Days 160–166) | L3 | ☆ The deep-RL family: Double/Dueling DQN, Rainbow, A2C, DDPG, TD3, SAC, TRPO ☆ |
| [162](part13_advanced_shelf.md#day-162) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S5 · Reinforcement-learning and agent extensions (Days 160–166) | L3 | ☆ Model-based, offline, imitation and multi-agent RL ☆ |
| [163](part13_advanced_shelf.md#day-163) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S5 · Reinforcement-learning and agent extensions (Days 160–166) | L3 | ☆ Agent reasoning patterns: Reflexion, Tree-of-Thoughts, self-consistency ☆ |
| [164](part13_advanced_shelf.md#day-164) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S5 · Reinforcement-learning and agent extensions (Days 160–166) | L3 | ☆ Code agents and computer-use agents ☆ |
| [165](part13_advanced_shelf.md#day-165) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S5 · Reinforcement-learning and agent extensions (Days 160–166) | L3 | ☆ Agent systems: A2A, supervisor / swarm, durable workflows ☆ |
| [166](part13_advanced_shelf.md#day-166) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S5 · Reinforcement-learning and agent extensions (Days 160–166) | L3 | ☆ Agent security: OWASP LLM Top-10 ☆ |
| [167](part13_advanced_shelf.md#day-167) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S6 · Engineering and career (Days 167–180) | L3 | ☆ Data engineering: Kafka, Airflow/Prefect, dbt ☆ |
| [168](part13_advanced_shelf.md#day-168) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S6 · Engineering and career (Days 167–180) | L3 | ☆ Serving at scale: vLLM, Triton, Ray Serve, Kubernetes ☆ |
| [169](part13_advanced_shelf.md#day-169) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S6 · Engineering and career (Days 167–180) | L3 | ☆ Python performance for ML engineers ☆ |
| [170](part13_advanced_shelf.md#day-170) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S6 · Engineering and career (Days 167–180) | L3 | ☆ Privacy and responsible AI ☆ |
| [171](part13_advanced_shelf.md#day-171) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S6 · Engineering and career (Days 167–180) | L3 | ☆ Recommenders, advanced ☆ |
| [172](part13_advanced_shelf.md#day-172) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S6 · Engineering and career (Days 167–180) | L3 | ☆ Search and learning-to-rank ☆ |
| [173](part13_advanced_shelf.md#day-173) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S6 · Engineering and career (Days 167–180) | L3 | ☆ Reading and reproducing a paper ☆ |
| [174](part13_advanced_shelf.md#day-174) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S6 · Engineering and career (Days 167–180) | L3 | ☆ Kaggle workflow ☆ |
| [175](part13_advanced_shelf.md#day-175) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S6 · Engineering and career (Days 167–180) | L3 | ☆ Coding-interview pack I: arrays, hashing, two-pointers, stack, heap ☆ |
| [176](part13_advanced_shelf.md#day-176) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S6 · Engineering and career (Days 167–180) | L3 | ☆ Coding-interview pack II: trees, graphs, DP and "ML from scratch" ☆ |
| [177](part13_advanced_shelf.md#day-177) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S6 · Engineering and career (Days 167–180) | L3 | ☆ Open source and writing in public ☆ |
| [178](part13_advanced_shelf.md#day-178) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S6 · Engineering and career (Days 167–180) | L3 | ☆ ML system design II (ranking, search, fraud at scale) ☆ |
| [179](part13_advanced_shelf.md#day-179) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S6 · Engineering and career (Days 167–180) | L3 | ☆ Behavioural interview, résumé and salary ☆ |
| [180](part13_advanced_shelf.md#day-180) | XIII · Advanced Shelf ☆ (optional, Days 121–180) | S6 · Engineering and career (Days 167–180) | L3 | ☆ Final gap audit and your 12-month plan ☆ |

---

## ✅ Progress
Tick days inside each Part file (`☐` → `☑`). Part-level tracker: [Appendix E](appendix.md#e-trackers).

