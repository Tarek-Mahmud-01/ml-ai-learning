# 🧰 Tools, Frameworks & Python Libraries — Reference

> Reference only — **nothing is installed here.** This lists what you'll use in each phase of the [daily plan](daily_plan_advanced.md), when you need it, and what it's for. Install each when its week arrives.
>
> **Environment:** Python 3.12.2 · `venv` virtual environment · VS Code

---

## ✅ Already Have (from your 7-day program)
| Tool / Library | Purpose |
|---|---|
| **pandas** | Data wrangling, DataFrames |
| **numpy** | Numerical arrays, math |
| **matplotlib** | Plotting / charts |
| **seaborn** | Statistical visualization |
| **scikit-learn** | Classical ML (regression, trees, forests) |
| **joblib** | Saving/loading models |
| **jupyter** *(optional)* | Interactive notebooks |

---

## 🧮 WEEK 1 — Math + Deep Learning Start
| Tool / Library | Purpose | Used On |
|---|---|---|
| **numpy** | Build gradient descent & neural nets from scratch | Days 1–6 |
| **matplotlib** | Plot functions, loss curves | Days 2–3 |
| **PyTorch** (`torch`) | Deep learning framework — tensors, autograd | Day 7 |

**Learning aids (not libraries):** 3Blue1Brown (YouTube), pen & paper for derivatives.

---

## 🧠 WEEK 2 — Deep Learning with PyTorch
| Tool / Library | Purpose | Used On |
|---|---|---|
| **PyTorch** (`torch`) | Core deep learning | All week |
| **torchvision** | Datasets (MNIST, CIFAR-10), pretrained models, image transforms | Days 9–14 |
| **matplotlib** | Train vs validation curves | Day 10 |
| **tqdm** | Progress bars for training loops | Optional, all week |

**Key concepts (built-in to PyTorch):** `nn.Module`, `DataLoader`, `nn.Conv2d`, optimizers (SGD, Adam), pretrained **ResNet**.

---

## 📝 WEEK 3 — NLP & Transformers
| Tool / Library | Purpose | Used On |
|---|---|---|
| **Hugging Face `transformers`** | Pretrained models (BERT, GPT), fine-tuning, `Trainer` API | Days 18–21 |
| **Hugging Face `datasets`** | Load & prepare NLP datasets | Days 18–21 |
| **`tokenizers`** | Text tokenization (comes with transformers) | Day 15+ |
| **PyTorch** | Backend for transformers, LSTMs | All week |
| **scikit-learn** | Metrics (accuracy, F1) | Day 19 |

---

## 🤖 WEEK 4 — LLMs & Generative AI
| Tool / Library | Purpose | Used On |
|---|---|---|
| **Anthropic SDK** (`anthropic`) | Claude API — LLM calls (recommended) | Days 22–28 |
| **OpenAI SDK** (`openai`) | Alternative LLM API | Optional |
| **LangChain** *or* **LlamaIndex** | RAG pipelines, agents, chaining | Days 25–26 |
| **FAISS** *or* **ChromaDB** | Vector database for embeddings | Days 24–25 |
| **sentence-transformers** | Generate text embeddings | Day 24 |
| **PyPDF / python-docx** | Read documents into RAG | Day 25 |
| **peft** | LoRA parameter-efficient fine-tuning | Day 27 |
| **bitsandbytes** | Quantization for efficient fine-tuning | Day 27 |
| **python-dotenv** | Store API keys safely in `.env` | Day 22 |

> ⚠️ **API keys:** Keep them in a `.env` file (already git-ignored). Never commit keys.

---

## ⚙️ WEEK 5 — MLOps & Deployment
| Tool / Library | Purpose | Used On |
|---|---|---|
| **FastAPI** | Serve models as REST APIs | Days 29, 35 |
| **Uvicorn** | ASGI server to run FastAPI | Day 29 |
| **Pydantic** | Request/response validation (comes with FastAPI) | Day 29 |
| **Docker** *(not a pip lib — a program)* | Containerize your app | Day 30 |
| **MLflow** *or* **Weights & Biases** (`wandb`) | Experiment tracking | Day 31 |
| **Hugging Face Hub** (`huggingface_hub`) | Deploy to HF Spaces (free) | Day 33 |
| **GitHub Actions** *(config, not a lib)* | CI/CD pipelines | Day 34 |
| **pytest** | Testing your code | Day 34 |
| **Gradio** *or* **Streamlit** | Quick web UI for demos | Day 33, capstone |

---

## 🏆 WEEK 6 — Capstone (combines all of the above)
| Layer | Tools |
|---|---|
| **Anomaly model** | scikit-learn (Isolation Forest) |
| **Explanation (RAG)** | Anthropic SDK + ChromaDB/FAISS + LangChain |
| **API** | FastAPI + Uvicorn |
| **Frontend** | Gradio or Streamlit |
| **Container** | Docker |
| **Deploy** | Hugging Face Spaces |

---

## 🗂️ Suggested Install Order (per week — install only when you reach it)
```
Week 1:  torch
Week 2:  torchvision  tqdm
Week 3:  transformers  datasets
Week 4:  anthropic  langchain  chromadb  sentence-transformers  python-dotenv  peft
Week 5:  fastapi  uvicorn  mlflow  gradio  pytest  huggingface_hub
         (+ install Docker Desktop — separate program)
```

## 🌐 Non-Python Tools (install separately when needed)
| Tool | Week | What it is |
|---|---|---|
| **Docker Desktop** | 5 | Containers — download from docker.com |
| **Git** | ✅ have it | Version control |
| **VS Code** | ✅ have it | Editor |
| **Hugging Face account** | 4–5 | Free — for models & deployment |
| **Anthropic API account** | 4 | For Claude API key |

---

## 💡 Categories at a Glance (mental map)
- **Data:** pandas, numpy
- **Viz:** matplotlib, seaborn
- **Classical ML:** scikit-learn, joblib
- **Deep Learning:** PyTorch, torchvision
- **NLP / LLMs:** transformers, datasets, anthropic, langchain
- **Vector search / RAG:** faiss, chromadb, sentence-transformers
- **Serving / Deploy:** fastapi, uvicorn, docker, gradio/streamlit
- **Ops:** mlflow / wandb, pytest, github actions
