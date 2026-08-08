# 📅 Advanced AI/ML — Day-by-Day Plan

> **Pace:** 3–4 hrs/day · Every day = **Theory → Practice → Mini-Project**
> Full roadmap: [advanced_ai_roadmap.md](advanced_ai_roadmap.md)
>
> **Daily time split (≈3.5 hrs):**
> - 🧠 **Theory (1 hr)** — understand the concept + math
> - ⌨️ **Practice (1.5 hr)** — code along, small exercises
> - 🛠️ **Project (1 hr)** — build something you can run & explain
>
> Check the box when a day is done. Don't skip the project — that's what makes it stick.

---

# 🧮 WEEK 1 — Math Backbone + Deep Learning Start

### ✅ Day 1 — Linear Algebra Intuition  — DONE (practice 8/8)
- 🧠 **Theory:** Vectors, matrices, matrix multiplication, dot product. Watch 3Blue1Brown "Essence of Linear Algebra" (ch 1–4).
- ⌨️ **Practice:** NumPy — create vectors/matrices, do dot products, matrix multiply by hand then verify with `np.dot`.
- 🛠️ **Project:** Write a function that multiplies two matrices *manually* (nested loops), compare to NumPy. Understand a neural layer = matrix multiply.

### ☐ Day 2 — Calculus & Gradients
- 🧠 **Theory:** Derivatives, chain rule, partial derivatives, what a gradient is. Watch 3Blue1Brown "Neural Networks" ch on backprop.
- ⌨️ **Practice:** Compute derivatives by hand for simple functions (x², x³, sin). Plot a function and its slope in matplotlib.
- 🛠️ **Project:** Write a function that numerically estimates the derivative of any function at a point.

### ☐ Day 3 — Gradient Descent from Scratch ⭐
- 🧠 **Theory:** Loss functions (MSE), how gradient descent minimizes loss step by step. Learning rate.
- ⌨️ **Practice:** Understand the update rule: `w = w - learning_rate * gradient`.
- 🛠️ **Project:** Fit a line to data using **pure NumPy gradient descent** (no scikit-learn). Print loss going down each step. *This is the heart of deep learning.*

### ☐ Day 4 — Probability & Cross-Entropy
- 🧠 **Theory:** Distributions, Bayes' theorem, expectation, cross-entropy loss (used in all classification).
- ⌨️ **Practice:** Compute mean/variance in NumPy. Implement cross-entropy for two probability arrays.
- 🛠️ **Project:** Build a tiny logistic regression from scratch using gradient descent + cross-entropy (connects to your Day 3 classical work).

### ☐ Day 5 — Neurons & Neural Network Theory
- 🧠 **Theory:** Neuron = weighted sum + activation. Layers. Activations: ReLU, sigmoid, softmax. Forward pass.
- ⌨️ **Practice:** Implement a single neuron in NumPy. Implement ReLU and sigmoid.
- 🛠️ **Project:** Build a forward pass for a 2-layer network by hand (random weights, one input → output).

### ☐ Day 6 — Backpropagation from Scratch ⭐⭐
- 🧠 **Theory:** How backprop works — chain rule through the network. The full loop: forward → loss → backward → update.
- ⌨️ **Practice:** Derive the gradients for a 2-layer net on paper.
- 🛠️ **Project:** Full 2-layer neural net in **pure NumPy** that learns XOR. Watch it learn. Huge milestone.

### ☐ Day 7 — PyTorch Introduction
- 🧠 **Theory:** Why frameworks exist. Tensors, autograd (automatic gradients), `nn.Module`.
- ⌨️ **Practice:** Install PyTorch. Create tensors, do operations, use `.backward()` to get gradients automatically.
- 🛠️ **Project:** Rebuild Day 6's XOR net in PyTorch. Feel how much easier autograd makes it.

---

# 🧠 WEEK 2 — Deep Learning with PyTorch

### ☐ Day 8 — The PyTorch Training Loop
- 🧠 **Theory:** The 5 steps: forward → loss → zero_grad → backward → step. Optimizers (SGD, Adam).
- ⌨️ **Practice:** Write a training loop for a simple regression in PyTorch.
- 🛠️ **Project:** Train a PyTorch net on your existing sales data (`data/`). Compare to your Day 7 random forest.

### ☐ Day 9 — MNIST Digit Classifier
- 🧠 **Theory:** Datasets, DataLoaders, batching, image data as tensors.
- ⌨️ **Practice:** Load MNIST with `torchvision`. Explore the data.
- 🛠️ **Project:** Train a fully-connected net to classify handwritten digits. Aim for >95% accuracy.

### ☐ Day 10 — Overfitting & Regularization
- 🧠 **Theory:** Overfitting, train vs validation loss, dropout, L2 regularization, batch normalization.
- ⌨️ **Practice:** Add dropout & batch norm to your MNIST net.
- 🛠️ **Project:** Plot train vs validation curves. Show overfitting, then fix it with regularization.

### ☐ Day 11 — Optimizers & Learning Rate
- 🧠 **Theory:** SGD → Momentum → Adam. Learning rate schedules. Why they matter.
- ⌨️ **Practice:** Train the same net with different optimizers/learning rates, compare.
- 🛠️ **Project:** Experiment log — find the best optimizer + LR for MNIST, document results in a notes file.

### ☐ Day 12 — Convolutions (CNN Theory)
- 🧠 **Theory:** Convolutions, filters, pooling, feature maps, why CNNs beat dense nets on images.
- ⌨️ **Practice:** Add `nn.Conv2d` and `nn.MaxPool2d` layers. Understand shapes.
- 🛠️ **Project:** Build a small CNN, retrain on MNIST, compare accuracy to Day 9's dense net.

### ☐ Day 13 — CNN on CIFAR-10
- 🧠 **Theory:** Color images, deeper CNNs, data augmentation.
- ⌨️ **Practice:** Load CIFAR-10, apply augmentation (flips, crops).
- 🛠️ **Project:** Train a CNN to classify 10 object types. This is real computer vision.

### ☐ Day 14 — Transfer Learning ⭐
- 🧠 **Theory:** Pretrained models (ResNet), freezing layers, fine-tuning. The most practical CV skill.
- ⌨️ **Practice:** Load a pretrained ResNet from `torchvision`.
- 🛠️ **Project:** Fine-tune ResNet on a small custom image set (e.g., receipts/documents — ties to HRM). High accuracy with little data.

---

# 📝 WEEK 3 — NLP & Transformers

### ☐ Day 15 — Text to Numbers
- 🧠 **Theory:** Tokenization, vocabulary, word embeddings (word2vec intuition).
- ⌨️ **Practice:** Tokenize text, build a vocabulary, one-hot vs embeddings.
- 🛠️ **Project:** Turn a batch of sentences into embedding vectors and visualize similarity.

### ☐ Day 16 — RNNs & LSTMs
- 🧠 **Theory:** Sequence models, why order matters, RNN → LSTM (memory), vanishing gradients.
- ⌨️ **Practice:** Build a small LSTM in PyTorch.
- 🛠️ **Project:** Train an LSTM for text sentiment (positive/negative) on a small dataset.

### ☐ Day 17 — Self-Attention & Transformers ⭐⭐
- 🧠 **Theory:** Self-attention, query/key/value, multi-head attention, positional encoding. Skim "Attention Is All You Need".
- ⌨️ **Practice:** Implement a tiny self-attention function in NumPy/PyTorch.
- 🛠️ **Project:** Diagram + code a single attention head. Explain it in your own words in a notes file.

### ☐ Day 18 — Hugging Face Ecosystem
- 🧠 **Theory:** Pretrained transformers, the `transformers` + `datasets` libraries, model hub.
- ⌨️ **Practice:** Load a pretrained BERT, run inference on text.
- 🛠️ **Project:** Use a pretrained model for sentiment analysis out of the box.

### ☐ Day 19 — Fine-Tuning BERT
- 🧠 **Theory:** Fine-tuning vs training from scratch, the `Trainer` API.
- ⌨️ **Practice:** Prepare a dataset for fine-tuning.
- 🛠️ **Project:** Fine-tune BERT on a custom text-classification task. Evaluate accuracy.

### ☐ Day 20 — Text Generation
- 🧠 **Theory:** How generative models produce text, decoding (greedy, sampling, temperature).
- ⌨️ **Practice:** Use a small GPT-style model to generate text.
- 🛠️ **Project:** Build a mini text generator; experiment with temperature settings.

### ☐ Day 21 — NLP Review + Mini-Project
- 🧠 **Theory:** Consolidate — embeddings, attention, transformers, fine-tuning.
- ⌨️ **Practice:** Revisit weak spots.
- 🛠️ **Project:** Build a "document classifier" for your HRM domain (e.g., classify HR document types).

---

# 🤖 WEEK 4 — LLMs & Generative AI ⭐ (Most in-demand)

### ☐ Day 22 — How LLMs Really Work
- 🧠 **Theory:** Pretraining, fine-tuning, RLHF, tokens, context windows, capabilities & limits.
- ⌨️ **Practice:** Explore an LLM API (Claude API recommended). Send your first API call.
- 🛠️ **Project:** Simple script that sends a prompt and prints the response.

### ☐ Day 23 — Prompt Engineering
- 🧠 **Theory:** Prompting as engineering — system prompts, few-shot, chain-of-thought, structure.
- ⌨️ **Practice:** Test the same task with different prompt styles.
- 🛠️ **Project:** Build a prompt template that reliably extracts structured data from messy text.

### ☐ Day 24 — Embeddings & Vector Search
- 🧠 **Theory:** Text embeddings, semantic similarity, vector databases (FAISS/Chroma).
- ⌨️ **Practice:** Generate embeddings, compute cosine similarity, store in a vector DB.
- 🛠️ **Project:** "Semantic search" over a folder of documents — find by meaning, not keywords.

### ☐ Day 25 — RAG (Retrieval-Augmented Generation) ⭐⭐
- 🧠 **Theory:** RAG architecture — retrieve relevant chunks → feed to LLM → grounded answer. Chunking strategies.
- ⌨️ **Practice:** Wire retrieval + LLM together.
- 🛠️ **Project:** RAG chatbot over your **HRM rulebook** — ask "What's the overtime policy?" and get answers from your docs.

### ☐ Day 26 — AI Agents & Tool Use
- 🧠 **Theory:** Agents, function/tool calling, multi-step reasoning, the agent loop.
- ⌨️ **Practice:** Give an LLM a tool (e.g., a calculator or data-query function).
- 🛠️ **Project:** Agent that can query your payslip data and answer questions in natural language.

### ☐ Day 27 — Fine-Tuning LLMs (LoRA)
- 🧠 **Theory:** Parameter-efficient fine-tuning, LoRA, when to fine-tune vs RAG.
- ⌨️ **Practice:** Set up a LoRA fine-tune on a small open model.
- 🛠️ **Project:** Fine-tune a small model on a custom task; compare to prompting.

### ☐ Day 28 — GenAI Review + Combine
- 🧠 **Theory:** RAG vs fine-tuning vs agents — decision framework.
- ⌨️ **Practice:** Refine your Week 4 projects.
- 🛠️ **Project:** Combine RAG + agent — an assistant that retrieves HR policy AND queries payslip data.

---

# ⚙️ WEEK 5 — MLOps & Deployment

### ☐ Day 29 — Serving Models with FastAPI
- 🧠 **Theory:** REST APIs, endpoints, request/response, why models need APIs.
- ⌨️ **Practice:** Build a basic FastAPI app with one endpoint.
- 🛠️ **Project:** Wrap your **HRM anomaly detector** in `POST /check-payslip` returning Normal/Anomaly.

### ☐ Day 30 — Docker
- 🧠 **Theory:** Containers, images, why "works on my machine" dies with Docker.
- ⌨️ **Practice:** Write a Dockerfile, build an image, run a container.
- 🛠️ **Project:** Dockerize your FastAPI model service; run it in a container locally.

### ☐ Day 31 — Experiment Tracking
- 🧠 **Theory:** Tracking runs, params, metrics (MLflow / Weights & Biases).
- ⌨️ **Practice:** Log a training run's metrics.
- 🛠️ **Project:** Add experiment tracking to one of your earlier training scripts.

### ☐ Day 32 — Monitoring & Drift
- 🧠 **Theory:** Model monitoring, data drift, when to retrain.
- ⌨️ **Practice:** Add logging to your API to record predictions.
- 🛠️ **Project:** Simple drift check — compare new data distribution to training data.

### ☐ Day 33 — Deploy to the Cloud ⭐
- 🧠 **Theory:** Deployment options (Hugging Face Spaces = easiest free, Modal, cloud).
- ⌨️ **Practice:** Prepare your app for deployment.
- 🛠️ **Project:** Deploy one project publicly. Get a **live URL** anyone can use.

### ☐ Day 34 — CI/CD Basics
- 🧠 **Theory:** Automated testing & deployment pipelines for ML.
- ⌨️ **Practice:** Set up a basic GitHub Action.
- 🛠️ **Project:** Auto-run tests when you push to your repo.

### ☐ Day 35 — MLOps Review
- 🧠 **Theory:** Consolidate the full production lifecycle.
- ⌨️ **Practice:** Clean up and document your deployed service.
- 🛠️ **Project:** Write a README so anyone can run your service.

---

# 🏆 WEEK 6 — Capstone: Intelligent HRM Assistant

### ☐ Day 36 — Capstone Design
Plan the architecture: data upload → anomaly model → RAG explanation → API → frontend → deploy.

### ☐ Day 37 — Anomaly Engine
Integrate your HRM anomaly detector as the core service.

### ☐ Day 38 — RAG Explanation Layer
Add the LLM that explains *in plain English* why each flagged payslip breaks policy.

### ☐ Day 39 — API + Frontend
FastAPI backend + a simple frontend (upload data, see results).

### ☐ Day 40 — Dockerize & Deploy
Containerize everything, deploy publicly. Get your live URL.

### ☐ Day 41 — Polish & Document
README, screenshots, architecture diagram. Make it portfolio-grade.

### ☐ Day 42 — Showcase 🎓
Write up what you built, record a demo, add it to your portfolio/GitHub. **You're now top-level.**

---

## 📌 Daily Habits
1. **Never skip the project** — building beats watching.
2. **Write one notes file per phase** explaining concepts in your own words.
3. **Commit to git daily** — `git add . && git commit -m "Day X: <topic>"`.
4. **Stuck > 30 min?** Ask for help, then move on. Momentum matters.
