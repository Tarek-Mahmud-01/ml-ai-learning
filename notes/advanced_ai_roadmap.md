# 🚀 Advanced AI/ML Roadmap — Top-Level Path

> **Pace:** Intense (3–4 hrs/day) · **Style:** Theory + Projects · **Prereq:** ✅ Your completed 7-day classical-ML program
>
> This picks up exactly where you left off (regression, trees, forests, tuning, sales forecasting, anomaly detection). Each phase has **theory to master**, a **hands-on project**, and a **checkpoint**. Do them in order.

---

## 📍 Where You Are Now
You already know: pandas wrangling · linear/logistic regression · decision trees · random forests · hyperparameter tuning · train/test evaluation · a full forecasting project · anomaly detection (Isolation Forest).

**What's missing before deep learning:** the *math backbone* (gradients, linear algebra intuition) and *neural network mechanics*. We fix that in Phase 0–1.

---

## 🧮 Phase 0 — Math Backbone (3–4 days)
The math you *actually* need. Not a full degree — just enough to read papers and debug models.

**Theory**
- **Linear algebra:** vectors, matrices, matrix multiplication, dot products (this IS a neural network layer). Watch 3Blue1Brown "Essence of Linear Algebra".
- **Calculus:** derivatives, the chain rule, partial derivatives, gradients. This IS backpropagation.
- **Probability:** distributions, Bayes' theorem, expectation, cross-entropy (this IS the loss function you'll use everywhere).

**Project:** Implement gradient descent *from scratch* in NumPy — no scikit-learn. Fit a line to data by manually computing gradients and updating weights in a loop. When you understand this, you understand 80% of deep learning.

**Checkpoint:** You can explain, in plain words, what a gradient is and why we subtract it.

---

## 🧠 Phase 1 — Deep Learning Foundations (2 weeks)

**Theory**
- Neurons, layers, activation functions (ReLU, sigmoid, softmax).
- Forward pass → loss → **backpropagation** → weight update. The full loop.
- Overfitting, regularization (dropout, L2), batch normalization.
- Optimizers: SGD → Momentum → Adam.

**Tools:** PyTorch (recommended — it's what research & industry use). Learn `Tensor`, `nn.Module`, `autograd`, `DataLoader`, the training loop.

**Projects**
1. **Neural net from scratch in NumPy** — a 2-layer net that classifies handwritten digits (MNIST). Implement backprop yourself.
2. **Rebuild it in PyTorch** — same task, feel the difference. This is your "aha" moment.
3. **Tabular deep learning** — take your existing HRM/sales data and train a neural net on it. Compare against your random forest. (Great real-world lesson: DL doesn't always win on tabular data!)

**Checkpoint:** You can write a PyTorch training loop from memory.

---

## 👁️ Phase 2 — Computer Vision & CNNs (1.5 weeks)

**Theory**
- Convolutions, filters, pooling, feature maps.
- Classic architectures: LeNet → ResNet (residual connections — a key idea).
- **Transfer learning** — the single most practical CV skill. Reuse pretrained models.
- Data augmentation.

**Projects**
1. **CNN image classifier** on CIFAR-10 (10 object classes).
2. **Transfer learning project** — fine-tune a pretrained ResNet on a *custom* dataset you care about (e.g., document/receipt classification — ties into your HRM work).

**Checkpoint:** You can take any pretrained model and fine-tune it on your own images.

---

## 📝 Phase 3 — NLP & The Transformer (2 weeks)

**Theory**
- Text → numbers: tokenization, embeddings (word2vec intuition).
- RNNs & LSTMs (understand them, then understand why transformers replaced them).
- **The Transformer** — self-attention, multi-head attention, positional encoding. Read/skim the "Attention Is All You Need" paper. This is THE architecture behind all modern AI.
- The Hugging Face ecosystem (`transformers`, `datasets`).

**Projects**
1. **Sentiment classifier** with a fine-tuned BERT model via Hugging Face.
2. **Text generation** with a small GPT-style model.

**Checkpoint:** You can explain self-attention and fine-tune a Hugging Face model.

---

## 🤖 Phase 4 — LLMs & Generative AI (2–3 weeks) ⭐ *Most in-demand*

**Theory**
- How LLMs really work: pretraining, fine-tuning, RLHF, context windows, tokens.
- **Prompt engineering** as an engineering discipline.
- **RAG (Retrieval-Augmented Generation)** — give an LLM your own documents. Embeddings + vector databases (FAISS/Chroma).
- **Fine-tuning vs. RAG** — when to use which. LoRA / parameter-efficient fine-tuning.
- **AI Agents** — tool use, function calling, multi-step reasoning.

**Tools:** The **Claude API** (Anthropic) and/or OpenAI API, LangChain or LlamaIndex, a vector DB.

**Projects**
1. **RAG chatbot over your own docs** — e.g., a "Company HR Policy Assistant" that answers questions from your HRM rulebook. (Perfect fusion with your existing HRM project!)
2. **AI Agent** — a tool-using agent that can, say, query your payslip data and flag anomalies *in natural language*.
3. **Fine-tune a small open model** (LoRA) on a custom task.

**Checkpoint:** You've built and deployed a working RAG app that answers from your data.

---

## ⚙️ Phase 5 — MLOps & Production (2 weeks)

**Theory**
- Serving models as APIs (**FastAPI**).
- **Docker** — containerize your model so it runs anywhere.
- Experiment tracking (**MLflow** or **Weights & Biases**).
- Model monitoring, drift detection, retraining pipelines.
- CI/CD basics for ML. Cloud deploy (one of: AWS SageMaker, GCP, Hugging Face Spaces, or Modal).

**Projects**
1. **Wrap your HRM anomaly detector in a FastAPI endpoint** — `POST /check-payslip` returns "Normal / Anomaly".
2. **Dockerize it** and run the container locally.
3. **Deploy** one project publicly (Hugging Face Spaces is the easiest free option).

**Checkpoint:** You have a live URL where someone can use your model.

---

## 🏆 Phase 6 — Capstone (1–2 weeks)
Build ONE portfolio-grade project that combines everything:

> **"Intelligent HRM Assistant"** — a deployed web app where a user uploads payslip/attendance data. The system (1) runs your anomaly-detection model, (2) uses a RAG-powered LLM to *explain in plain English* why each flagged payslip is wrong per company policy, and (3) serves it all through a FastAPI + simple frontend, containerized with Docker, deployed publicly.

This single project demonstrates: classical ML + deep learning awareness + LLMs/RAG + deployment. It's a strong portfolio centerpiece.

---

## 📚 Reference Resources
- **Math:** 3Blue1Brown (YouTube) — Linear Algebra & Neural Networks series.
- **Deep Learning:** "Dive into Deep Learning" (d2l.ai, free) · Andrej Karpathy's "Zero to Hero" YouTube series (build GPT from scratch — legendary).
- **Fast track:** fast.ai "Practical Deep Learning for Coders" (free).
- **LLMs:** Hugging Face free courses · Anthropic Claude docs.
- **Paper:** "Attention Is All You Need" (skim after Phase 3 theory).

---

## ✅ Progress Tracker
- [ ] Phase 0 — Math backbone
- [ ] Phase 1 — Deep learning foundations
- [ ] Phase 2 — Computer vision / CNNs
- [ ] Phase 3 — NLP & Transformers
- [ ] Phase 4 — LLMs & Generative AI
- [ ] Phase 5 — MLOps & production
- [ ] Phase 6 — Capstone

**Golden rule:** Don't just watch/read. Every phase ends with a *project you built and can explain*. That's what makes it top-level.
