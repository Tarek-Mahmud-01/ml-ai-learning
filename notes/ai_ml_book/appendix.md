# 📎 Appendices

[← Table of contents](README.md)

---

## A. Math map
Every maths idea is taught on the day an algorithm first needs it. Use this table to find it again.

| Maths idea | First taught | Used again in |
|---|---|---|
| Error, RMSE | [Day 1](part1_start_here.md#day-1) | everywhere |
| Mean, median, variance, std, IQR, z-score, skewness, CLT, sampling | [Day 2](part1_start_here.md#day-2) | 8, 29, 40 |
| Covariance, Pearson / Spearman correlation | [Day 3](part1_start_here.md#day-3) | 14, 38 |
| Derivative, chain rule, partial derivative | [Day 5](part2_supervised_regression.md#day-5) | 6, 18, 31, 51 |
| Gradient, learning rate, momentum | [Day 6](part2_supervised_regression.md#day-6) | 18, 31, 55 |
| Vectors, dot product, norms, matrices, inverse, Gaussian elimination | [Day 7](part2_supervised_regression.md#day-7) | 14, 25, 36, 49, 69 |
| Hypothesis tests, p-value, standard error, confidence interval, t / F / z / chi-square / ANOVA | [Day 8](part2_supervised_regression.md#day-8) | 41, 46 |
| L1 / L2 penalties | [Day 14](part2_supervised_regression.md#day-14) | 38, 56 |
| Probability rules, Bayes, distributions, combinatorics, LLN, Markov idea | [Day 16](part3_supervised_classification.md#day-16) | 24, 29, 74 |
| Odds, log-odds, sigmoid | [Day 17](part3_supervised_classification.md#day-17) | 18, 49 |
| MLE, entropy, cross-entropy, KL | [Day 18](part3_supervised_classification.md#day-18) | 19, 27, 50, 88 |
| Softmax | [Day 19](part3_supervised_classification.md#day-19) | 50, 65, 69 |
| Distance metrics (Euclidean, Manhattan, Minkowski, cosine) | [Day 23](part3_supervised_classification.md#day-23) | 34, 64, 82 |
| Margin, hinge loss, kernels, ε-loss | [Day 25](part3_supervised_classification.md#day-25) | 50 |
| Entropy / Gini / information gain | [Day 27](part3_supervised_classification.md#day-27) | 28–32 |
| Variance of an average (bagging) | [Day 29](part3_supervised_classification.md#day-29) | 31 |
| Second derivative (Hessian) | [Day 32](part3_supervised_classification.md#day-32) | shelf 139 |
| Centroid, SSE, silhouette | [Day 34](part4_unsupervised.md#day-34) | 35 |
| Gaussian mixture, EM | [Day 35](part4_unsupervised.md#day-35) | shelf 132 |
| Eigenvalues, SVD, covariance matrix | [Day 36](part4_unsupervised.md#day-36) | 37, 69 |
| Explained variance | [Day 37](part4_unsupervised.md#day-37) | 38 |
| Mutual information, VIF | [Day 38](part4_unsupervised.md#day-38) | 14 |
| Shapley values | [Day 42](part5_evaluation_special_ml.md#day-42) | — |
| Autocorrelation, stationarity | [Day 43](part5_evaluation_special_ml.md#day-43) | 44 |
| Matrix factorization, NDCG | [Day 45](part5_evaluation_special_ml.md#day-45) | shelf 171 |
| Power, sample size | [Day 46](part5_evaluation_special_ml.md#day-46) | — |
| Backpropagation (matrix chain rule) | [Day 51](part6_deep_learning_vision.md#day-51) | 52–57, 66, 69 |
| Adam / momentum moments | [Day 55](part6_deep_learning_vision.md#day-55) | 149 |
| Convolution | [Day 60](part6_deep_learning_vision.md#day-60) | 62 |
| TF-IDF | [Day 64](part7_nlp.md#day-64) | 84 |
| Scaled dot-product attention | [Day 69](part7_nlp.md#day-69) | 78, 153 |
| Bellman equation, policy gradient | [Day 74](part8_reinforcement_learning.md#day-74) | 75, 76 |
| ELBO, diffusion noise | [Day 88](part9_generative_ai.md#day-88) | shelf 132, 142, 145 |

## B. Data-preparation toolbox map
| Topic | Day |
|---|---|
| First look, data types, quality checklist | [2](part1_start_here.md#day-2) |
| Missing values, outliers | [9](part2_supervised_regression.md#day-9) |
| Encoding: label, one-hot, ordinal, binary, frequency, mean / target, embedding | [10](part2_supervised_regression.md#day-10) |
| Scaling: min-max, standard, robust, max-abs, log, power; binning | [11](part2_supervised_regression.md#day-11) |
| Feature creation: polynomial, interaction, date-time, ratios | [14](part2_supervised_regression.md#day-14), [44](part5_evaluation_special_ml.md#day-44) |
| Pipelines and `ColumnTransformer` | [15](part2_supervised_regression.md#day-15) |
| Imbalanced data: weights, SMOTE, Tomek; data leakage | [21](part3_supervised_classification.md#day-21) |
| Feature selection and extraction | [38](part4_unsupervised.md#day-38), [37](part4_unsupervised.md#day-37) |

## C. Algorithm cheat-sheet (fill the last two columns yourself as you study)
| Algorithm | Core equation / loss | Key hyper-parameters | Main metric | How it fails | How to improve | Day |
|---|---|---|---|---|---|---|
| Linear regression | `ŷ = Xw`, MSE | — | RMSE, R² | non-linear data, outliers, collinearity | features, regularization, robust loss | 4–8 |
| Ridge / Lasso / ElasticNet | `J + λΣw²` / `J + λΣ\|w\|` | `λ`, `ρ` | RMSE (CV) | too much shrinkage | tune λ by CV | 14 |
| Logistic regression | sigmoid, log loss | `C` | F1, PR-AUC, log loss | non-linear boundary | features, scaling, `C`, threshold | 17–19 |
| KNN | nearest-neighbour vote | `k`, metric | F1 | high dimensions, unscaled data | scale, tune k, weights | 23 |
| Naive Bayes | `P(c)ΠP(xᵢ\|c)` | `α` (smoothing) | F1 | dependent features | smoothing, better features | 24 |
| LDA / QDA | Gaussian class densities | shrinkage | accuracy | non-Gaussian classes | QDA, regularize covariance | 24 |
| SVM / SVR | hinge / ε-loss | `C`, `γ`, kernel | F1 / RMSE | big data, unscaled | scale, tune (C, γ) | 25 |
| Decision tree | entropy / Gini | depth, leaf size, `ccp_alpha` | F1 | overfits | prune, limit depth | 27–28 |
| Random Forest / Extra Trees | bagging + random features | trees, `max_features`, leaf size | F1, OOB | big, slower | tune max_features, leaf size | 29 |
| AdaBoost | weighted errors | rounds, learning rate | F1 | noisy labels | fewer rounds, lower rate | 30 |
| Gradient boosting | fit residuals | trees, `ν`, depth, subsample | F1, RMSE | overfits late trees | early stopping, small ν | 31 |
| XGBoost / LightGBM / CatBoost | 2nd-order boosting + regularization | `lr`, depth, subsample, colsample, λ | F1, RMSE | many knobs | Optuna + early stopping | 32 |
| Stacking | meta-learner on OOF predictions | base models | CV score | leakage if not OOF | diverse base models | 33 |
| K-Means | SSE | `k`, init | silhouette | non-round clusters | k-means++, scaling, choose k | 34 |
| DBSCAN / GMM / hierarchical | density / EM / linkage | `ε`, minPts / components / linkage | silhouette, ARI | varying density, shapes | tune ε, use HDBSCAN | 35 |
| PCA / LDA / t-SNE / UMAP | eigenvectors / class scatter / KL | components, perplexity | explained variance | scaling, non-linear data | scale, choose components by variance | 36–37 |
| Isolation Forest / LOF | path length / local density | contamination, neighbours | precision@k | false alarms | combine rules + model | 39 |
| ARIMA / lag + GBM / Prophet | AR + MA / lag features | (p,d,q), lags | sMAPE (backtest) | non-stationary data | differencing, features, backtest | 43–44 |
| Neural network (MLP) | cross-entropy / MSE + backprop | layers, width, lr, dropout | val loss / F1 | overfit, vanishing gradients | regularize, schedules, init | 48–59 |
| CNN | convolution + pooling | filters, depth | accuracy / mAP | small data | augmentation, transfer learning | 60–62 |
| RNN / LSTM / GRU | gated recurrence | hidden size, layers | F1 | long dependencies | attention, pretrained embeddings | 66–67 |
| Transformer / BERT | `softmax(QKᵀ/√d)V` | layers, heads, lr | F1 | padding / length issues | fine-tune, tuned LR, distill | 69–71 |
| Q-learning / DQN / PPO | Bellman / clipped policy gradient | α, γ, ε, clip | return | instability, reward hacking | replay, target net, more seeds | 74–76 |
| RAG | retrieve → generate | chunk size, k, reranker | recall@k, faithfulness | wrong chunk, hallucination | hybrid + rerank + citations | 82–85 |
| LoRA | `W + (α/r)BA` | `r`, α, target modules | task score | bad data, forgetting | clean data, tune r | 86–87 |
| Agent (ReAct / LangGraph) | loop of tool calls | tools, `max_steps` | task success | loops, unsafe actions | tracing, evals, guardrails | 91–99 |

## D. Gap audit — every topic from your roadmap docs → the day that covers it
Tick a row when you can explain it **and** have built it.

| Topic (from your docs) | Day(s) | ☐ |
|---|---|---|
| Python, OOP, error handling (you know it — used daily) | all | ☐ |
| NumPy · Pandas · Polars · Matplotlib · Seaborn · Plotly · SciPy · Jupyter | 1, 2, 7 | ☐ |
| Descriptive stats · sampling · CLT · LLN · random variables | 2, 16 | ☐ |
| Inferential stats: hypothesis tests, CI, t / z / chi-square / ANOVA | 8 | ☐ |
| Probability, Bayes, distributions (Normal, Binomial, Poisson, Uniform, Exponential), combinatorics, Markov chains (idea) | 16 | ☐ |
| Correlation vs causation | 3, 46 | ☐ |
| Linear algebra: vectors, matrices, norms, Gaussian elimination, eigenvalues / eigenvectors, SVD | 7, 36 | ☐ |
| Calculus, partial derivatives, gradient descent and variants, convex / non-convex optimization | 5, 6, 55, shelf 139 | ☐ |
| EDA · missing values · outliers · data cleaning | 2, 9 | ☐ |
| Feature scaling (min-max, standard, robust, max-abs, log, power) · binning | 11 | ☐ |
| Encoding (label, one-hot, ordinal, binary, frequency, mean / target, embedding) | 10 | ☐ |
| Feature creation, selection, extraction · high vs low dimensionality | 14, 37, 38 | ☐ |
| Linear / simple / multiple / polynomial / quadratic regression · residuals · cost functions | 4–7, 14 | ☐ |
| Ridge · Lasso · ElasticNet · regularization | 14 | ☐ |
| RSS · SST · RSE · R² · MAE · MSE · RMSE · adjusted R² | 12 | ☐ |
| Overfitting · underfitting · bias–variance · generalization | 13 | ☐ |
| Logistic regression · softmax | 17–19 | ☐ |
| Confusion matrix · accuracy · precision · recall · F1 · ROC-AUC | 20 | ☐ |
| Imbalanced data (over / under-sampling, SMOTE) · data leakage | 21 | ☐ |
| KNN · distance metrics | 23 | ☐ |
| Naive Bayes · LDA / QDA | 24 | ☐ |
| SVM · SVR | 25 | ☐ |
| Decision tree · pruning (pre / post) · alpha | 27, 28 | ☐ |
| Random Forest · Extra Trees · row sampling · feature sampling | 29 | ☐ |
| AdaBoost · GBM · XGBoost · LightGBM · CatBoost · bagging · boosting · stacking · voting | 30–33 | ☐ |
| K-Means · hierarchical · DBSCAN · GMM | 34, 35 | ☐ |
| PCA · LDA (reduction) · t-SNE · UMAP | 36, 37 | ☐ |
| Anomaly detection | 39 | ☐ |
| Cross-validation (K-Fold, Stratified, Group, LOOCV, TimeSeriesSplit) | 40 | ☐ |
| Grid / random search · Bayesian optimization · Optuna · genetic algorithm | 41 | ☐ |
| Explainability (SHAP, LIME, permutation) · fairness | 42 | ☐ |
| Time series: trend, seasonality, ACF / PACF, AR, MA, ARIMA, Prophet, moving average | 43, 44 | ☐ |
| Recommenders · A/B tests · causal thinking | 45, 46 | ☐ |
| Perceptron · ANN · activations · losses · backprop | 48–52 | ☐ |
| Optimizers · regularization · initialization · debugging training | 55–57 | ☐ |
| PyTorch · TensorFlow / Keras | 53, 54, 58 | ☐ |
| OpenCV · HOG / SIFT · CNN · VGG / ResNet / MobileNet · transfer learning | 60, 61 | ☐ |
| YOLO · Faster R-CNN · U-Net · Mask R-CNN · ViT | 62, shelf 143 | ☐ |
| Tokenization · stemming · lemmatization · stop-words · POS · NER · WordNet | 63 | ☐ |
| Bag-of-words · TF-IDF · Vector Space Model · text classification · topic modelling | 64, shelf 150 | ☐ |
| Word2Vec · GloVe · FastText | 65 | ☐ |
| RNN · LSTM · GRU · seq2seq · attention | 66–68 | ☐ |
| Transformers · BERT · GPT · T5 · Hugging Face · fine-tuning | 69–71 | ☐ |
| NER · QA · summarization · translation · BLEU / ROUGE | 72 | ☐ |
| Reinforcement learning: MDP, Bellman, Q-learning, SARSA, DQN, PPO, actor-critic | 74, 75 | ☐ |
| RLHF · DPO · GRPO | 76, shelf 155 | ☐ |
| LLM fundamentals · tiny GPT · decoding | 77–79 | ☐ |
| LLM APIs · prompt engineering · structured output | 80, 81 | ☐ |
| Embeddings · vector DBs (FAISS, Chroma, pgvector, Pinecone, Weaviate) · RAG · RAG evaluation | 82–85 | ☐ |
| Fine-tuning: SFT · LoRA · QLoRA · PEFT | 86, 87 | ☐ |
| VAE · GAN (StyleGAN, CycleGAN) · diffusion · super-resolution · inpainting · style transfer · DreamBooth · speech | 88, shelf 142, 144, 145, 159 | ☐ |
| LLM safety · evals · cost · latency | 89, 90 | ☐ |
| Agents: tool calling · ReAct · planning · memory | 91–93 | ☐ |
| LangChain · LlamaIndex · LangGraph · MCP | 94, 95 | ☐ |
| AutoGPT · BabyAGI · CrewAI · AutoGen · multi-agent | 96 | ☐ |
| Agent evals · guardrails · security | 97, shelf 166 | ☐ |
| FastAPI model serving · REST · validation · latency · TorchServe / TF Serving (awareness) | 100 | ☐ |
| Auth (JWT) · rate limiting · CORS · secrets | 101 | ☐ |
| PostgreSQL · pgvector · MongoDB · ORM | 102 | ☐ |
| Docker · docker-compose | 103 | ☐ |
| Git / GitHub · GitHub Actions CI/CD | 104 | ☐ |
| Testing ML / LLM code | 105 | ☐ |
| Redis · Celery · caching · async | 106 | ☐ |
| MLflow · DVC · model registry · reproducibility | 107 | ☐ |
| Monitoring · drift · LLM tracing | 108 | ☐ |
| Spark / PySpark · Dask · Parquet · ETL | 109, 110 | ☐ |
| Cloud (Render / Railway / HF Spaces / AWS / SageMaker / Vertex AI / Azure ML) · Kubernetes awareness · data warehouses (BigQuery / Snowflake — awareness) | 111, shelf 168 | ☐ |
| ML system design · design docs | 112, 113, shelf 178 | ☐ |
| Ethics and privacy · responsible AI | 42, shelf 170 | ☐ |
| Kaggle · open source · knowledge sharing (LinkedIn / blog) · portfolio · interviews | 120, shelf 174, 177, 179 | ☐ |

**Skipped on purpose (with reasons):** Django / DRF (same ideas as FastAPI) · Java / C++ (optional in the roadmaps; shelf Day 169 covers Python performance) · Hadoop / Kubeflow (awareness only — Spark and Kubernetes cover the ideas) · Power BI / Tableau (BI tools — learn when a job needs them) · R language (optional) · basic SQL (you have 5 years of experience).

## E. Trackers

### Results log (`plan120/results_log.md`)
| Day | Task | Version | Change made | Metric | Score | Note |
|---|---|---|---|---|---|---|
| 1 | diabetes regression | V1 | mean baseline | RMSE | … | score to beat |
| 14 | diabetes regression | V4 | poly + ElasticNet (tuned) | RMSE | … | best |

### Interview tracker
| Part | 20 questions done | Mock done | Weak topics to redo |
|---|---|---|---|
| I Start here | ☐ | — | |
| II Regression | ☐ (Day 15) | — | |
| III Classification | ☐ (Days 22, 26, 33) | — | |
| IV Unsupervised | ☐ (Day 39) | — | |
| V Evaluate & special ML | ☐ (Day 42) | ☐ Day 47 (50 Qs) | |
| VI Deep learning & CV | ☐ (Days 59, 62) | — | |
| VII NLP | ☐ (Day 73) | — | |
| VIII RL | ☐ (Day 76) | — | |
| IX Generative AI | ☐ (Day 90) | — | |
| X Agentic AI | ☐ (Day 99) | — | |
| XI Software engineering | ☐ (Day 111) | — | |
| XII Final | — | ☐ Day 119 (60 min) | |

### Progress tracker
☐ Part I (1–3) · ☐ II (4–15) · ☐ III (16–33) · ☐ IV (34–39) · ☐ V (40–47) · ☐ VI (48–62) · ☐ VII (63–73) · ☐ VIII (74–76) · ☐ IX (77–90) · ☐ X (91–99) · ☐ XI (100–111) · ☐ XII (112–120) · ☐ XIII shelf (121–180)

## F. Company habits and resources

**Company habits (build them from Day 1)**
1. Write a one-line goal and a metric before you code. 2. Baseline first. 3. Small commits, clear messages, pull requests, code review. 4. Tests + CI for anything that will be re-run. 5. Log experiments (params, data version, metrics). 6. Explain results to non-technical people: one sentence, one chart, one risk, one next step. 7. Monitor in production and plan rollback. 8. Safety by default: least privilege, read-only data access, no secrets in code, privacy-aware logs. 9. Write a design doc before big work. 10. Say "I don't know — here is how I would find out."

**Resources**
- Source roadmaps: <https://github.com/rashakil-ds/Roadmap-Docs> (AI Engineer, Generative AI Engineer, AI Agent Developer, NLP Engineer, Machine Learning Engineer, Software Engineering with ML-AI, Computer Vision Engineer, Data Scientist, Domain-Specific ML).
- Docs: [scikit-learn](https://scikit-learn.org/stable/) · [PyTorch tutorials](https://pytorch.org/tutorials/beginner/basics/intro.html) · [TensorFlow tutorials](https://www.tensorflow.org/tutorials) · [Hugging Face learn](https://huggingface.co/learn) · [LangChain](https://python.langchain.com/docs/introduction/) · [FastAPI](https://fastapi.tiangolo.com/) · [Spinning Up (RL)](https://spinningup.openai.com/)
- Channels: Andrej Karpathy · Sebastian Raschka · StatQuest · 3Blue1Brown · Study Mart
