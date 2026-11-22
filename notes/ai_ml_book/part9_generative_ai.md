# PART IX — Generative AI and Large Language Models

[📖 Table of contents](README.md) · [← previous part](part8_reinforcement_learning.md) · [next part →](part10_agentic_ai.md) · [Appendices](appendix.md)

> **Days 77–90 · Category: generative models · Levels: 1 → 3 in every chapter**
> **You will be able to:** explain and build a tiny GPT, call LLM APIs with streaming and cost control, write tested prompts with structured output, build and evaluate RAG with citations, fine-tune with LoRA, understand image / audio generation, and defend an LLM app against hallucination and prompt injection.
> **Math you meet here (just-in-time):** next-token probability and perplexity (Day 77) · temperature, top-k, top-p (79) · cosine and ANN (82) · RRF, MRR (84–85) · low-rank `W + BA` (86) · ELBO, diffusion noise (88).
> **More depth:** Advanced shelf Days 150–159 (tokenizers, RoPE / KV-cache, DPO / GRPO, advanced RAG, benchmarks).

---

## Chapter 40 — How LLMs work + a tiny GPT

> ⚠️ **Common mistakes:** thinking an LLM "knows" facts (it predicts tokens) · ignoring tokenization cost · skipping the overfit-one-batch check on your tiny GPT.

### Level 1: tokens and next-token prediction
<a id="day-77"></a>
#### ☐ Day 77 — How an LLM really works
- 🧮 **New math today (just-in-time):** next-token probability, cross-entropy loss, perplexity, BPE merge counts.
- 🧠 **Idea · L1:** an LLM predicts the **next token**. Pre-training (read the internet) → SFT (follow instructions) → preference tuning (be helpful and safe). Know: token, context window, KV-cache.
- ➗ **Equation · L1:** `P(w₁…w_T) = Π P(wₜ|w<ₜ)` · loss `−(1/T)Σ log P(wₜ|w<ₜ)` · BPE merges the most frequent pair of symbols, again and again
- ⌨️ **Build · L2:** a mini **BPE tokenizer** from scratch; count tokens of a text with a real tokenizer; estimate cost = tokens × price.
- 📊 **Measure · L2:** tokens per word in English vs another language; context-window budget for a long document.
- 📈 **Improve · L3:** char-level → word-level → BPE: compare vocabulary and sequence length.
- 🎤 **Interview · L3:** What is a token? · Why a context limit? · Pre-training vs fine-tuning vs RLHF?
- ✅ **Done when:** you can explain "next-token prediction" to a non-technical person.


### Level 2: build the attention block
<a id="day-78"></a>
#### ☐ Day 78 — Tiny GPT, part 1: attention block
- 🧠 **Idea · L1:** build a decoder-only Transformer on characters (follow Karpathy's *Let's build GPT*).
- ➗ **Equation · L1:** causal mask `scores[i,j] = −∞ for j > i` · `softmax(QKᵀ/√d)V` · block = LayerNorm → attention → residual → LayerNorm → MLP → residual
- ⌨️ **Build · L2:** data loader (context windows), embeddings, one masked attention head, then multi-head; a transformer block.
- 📊 **Measure · L2:** loss at init `≈ ln(vocab)`; overfit one batch (Day-57 check).
- 📈 **Improve · L3:** bigram model → 1 head → multi-head → full block.
- 🎤 **Interview · L3:** Why mask? · Decoder-only vs encoder-decoder? · Why residual connections?
- ✅ **Done when:** loss drops below the bigram baseline.


### Level 3: train, sample and decode
<a id="day-79"></a>
#### ☐ Day 79 — Tiny GPT, part 2: train, sample, decode
- 🧮 **New math today (just-in-time):** temperature, top-k and top-p sampling.
- 🧠 **Idea · L1:** stack blocks, train, then **generate** by sampling one token at a time.
- ➗ **Equation · L1:** temperature `softmax(z/T)` · top-k keeps k best · top-p keeps the smallest set with probability ≥ p · perplexity `= exp(loss)`
- ⌨️ **Build · L2:** train on a small text (e.g. your own HR policies); generate with greedy / temperature / top-k / top-p.
- 📊 **Measure · L2:** validation loss / perplexity; quality of samples at T = 0.2, 1.0, 1.5.
- 📈 **Improve · L3:** more layers → longer context → tuned LR + cosine schedule → dropout.
- 🎤 **Interview · L3:** What does temperature do? · Top-k vs top-p? · Why is generation slow (KV-cache)?
- ✅ **Done when:** your model writes text that looks like the training text.


## Chapter 41 — Using LLMs: APIs and prompt engineering

> ⚠️ **Common mistakes:** judging a prompt by feel (use a test set) · no retries / rate-limit handling · free-text output where JSON is needed.

### Level 1–2: API, streaming, cost
<a id="day-80"></a>
#### ☐ Day 80 — LLM APIs: messages, streaming, cost
- 🧠 **Idea · L1:** use a hosted model through an API. Know: system prompt, messages, `max_tokens`, `temperature`, streaming, rate limits, retries.
- ➗ **Equation · L1:** cost `= (in_tokens × price_in) + (out_tokens × price_out)`
- ⌨️ **Build · L2:** Claude API: first call, multi-turn chat, streaming, token counting, retry with back-off, error handling; a tiny CLI chat.
- 📊 **Measure · L2:** latency (first token / total), tokens, cost per call.
- 📈 **Improve · L3:** non-streaming → streaming; long prompt → trimmed prompt (cost drops).
- 🎤 **Interview · L3:** System vs user message? · How do you handle rate limits? · How do you cut cost?
- ✅ **Done when:** a script chats, streams and prints cost.


### Level 3: prompts as code, structured output
<a id="day-81"></a>
#### ☐ Day 81 — Prompt engineering & structured output
- 🧠 **Idea · L1:** prompts are code. Zero-shot, few-shot, chain-of-thought, clear roles, delimiters, **JSON output validated by a schema**.
- ➗ **Equation · L1:** accuracy on a **test set** of 30 cases `= correct/30` — never judge a prompt by feeling.
- ⌨️ **Build · L2:** extract fields from messy HR text → JSON validated by `pydantic`; retry when invalid.
- 📊 **Measure · L2:** accuracy, invalid-JSON rate, cost for each prompt version.
- 📈 **Improve · L3:** V1 plain → V2 clear instructions → V3 few-shot examples → V4 schema + retry.
- 🎤 **Interview · L3:** Few-shot vs chain-of-thought? · How do you stop prompt injection? · How do you test prompts?
- ✅ **Done when:** V4 is ≥ 95 % on your test set.


## Chapter 42 — Retrieval-Augmented Generation (RAG)

> ⚠️ **Common mistakes:** one giant chunk size for everything · no citations · not separating retrieval failures from generation failures.

### Level 1: embeddings and vector search
<a id="day-82"></a>
#### ☐ Day 82 — Embeddings & vector databases
- 🧮 **New math today (just-in-time):** cosine similarity and approximate nearest neighbours (HNSW).
- 🧠 **Idea · L1:** turn text into a vector so **meaning** can be compared. Store vectors in a vector DB; search by nearest neighbour.
- ➗ **Equation · L1:** cosine `a·b/(‖a‖‖b‖)` · ANN indexes: flat (exact), IVF, **HNSW** (graph) · `recall@k`
- ⌨️ **Build · L2:** embed 200 HR sentences; brute-force search → FAISS → Chroma → pgvector; metadata filters.
- 📊 **Measure · L2:** recall@k and latency per index type.
- 📈 **Improve · L3:** keyword search → embedding search → + filters.
- 🎤 **Interview · L3:** Why cosine? · Exact vs approximate search? · How do you pick an embedding model?
- ✅ **Done when:** semantic search finds answers with zero shared keywords.


### Level 2: RAG v1 and v2
<a id="day-83"></a>
#### ☐ Day 83 — RAG, version 1
- 🧠 **Idea · L1:** the model does not know *your* documents. **Retrieve** the right chunks, put them in the prompt, answer **only** from them.
- ➗ **Equation · L1:** chunk size `c` and overlap `o` · top-k retrieval `argmax_k cos(q, dᵢ)`
- ⌨️ **Build · L2:** load HRM rulebook → chunk → embed → store → retrieve → prompt → answer ("What is the overtime policy?").
- 📊 **Measure · L2:** 20 test questions: right chunk retrieved? right answer?
- 📈 **Improve · L3:** V1 chunk 1000 → V2 chunk 400 + overlap → V3 k tuned.
- 🎤 **Interview · L3:** What is RAG and why not fine-tune? · How do you choose chunk size? · What if the answer is not in the documents?
- ✅ **Done when:** it answers 15 / 20 questions correctly.

<a id="day-84"></a>
#### ☐ Day 84 — RAG, version 2: hybrid search, rerank, citations
- 🧮 **New math today (just-in-time):** Reciprocal Rank Fusion and BM25.
- 🧠 **Idea · L1:** better retrieval = better answers. Combine keyword (BM25) and vector search, **rerank** with a cross-encoder, rewrite the query, **cite** sources.
- ➗ **Equation · L1:** Reciprocal Rank Fusion `score(d) = Σ 1/(k + rankᵢ(d))` · BM25 (TF-IDF family)
- ⌨️ **Build · L2:** BM25 + vectors + RRF; reranker; query rewriting; answer with `[source: file p.3]`.
- 📊 **Measure · L2:** recall@k and answer accuracy vs V1.
- 📈 **Improve · L3:** vector only → hybrid → + rerank → + query rewrite.
- 🎤 **Interview · L3:** Why hybrid search? · What does a reranker do? · How do you reduce hallucination?
- ✅ **Done when:** every answer has a citation that is correct.


### Level 3: evaluate and improve
<a id="day-85"></a>
#### ☐ Day 85 — RAG evaluation & improvement
- 🧮 **New math today (just-in-time):** recall@k, MRR and faithfulness metrics.
- 🧠 **Idea · L1:** you cannot improve what you do not measure. Split failures into **retrieval** vs **generation**.
- ➗ **Equation · L1:** `MRR = (1/Q) Σ 1/rankᵢ` · `recall@k` · faithfulness (answer supported by context?) · answer relevance · LLM-as-judge (check it against human labels)
- ⌨️ **Build · L2:** an eval set of 40 Q&A; automatic metrics; judge prompt; a table of failures by cause.
- 📊 **Measure · L2:** metrics for V1…V4; the biggest failure cause.
- 📈 **Improve · L3:** fix the top cause → re-run → log.
- 🎤 **Interview · L3:** How do you evaluate RAG? · LLM-as-judge risks? · Retrieval failure vs generation failure?
- ✅ **Done when:** a results table shows V1 → V4 gains.


## Chapter 43 — Fine-tuning LLMs

> ⚠️ **Common mistakes:** fine-tuning to add *knowledge* (use RAG) · tiny dirty datasets · no held-out evaluation.

### Level 1–2: SFT, LoRA, QLoRA theory
<a id="day-86"></a>
#### ☐ Day 86 — Fine-tuning theory: SFT, LoRA, QLoRA
- 🧮 **New math today (just-in-time):** low-rank decomposition `W′ = W + (α/r)·B·A`.
- 🧠 **Idea · L1:** change the model itself. **LoRA** trains two tiny matrices instead of the whole weight. When to use: prompt first → RAG for knowledge → fine-tune for **style / format / skill**.
- ➗ **Equation · L1:** `W′ = W + (α/r)·B·A`, `B ∈ ℝ^{d×r}`, `A ∈ ℝ^{r×k}`, `r ≪ d` · trainable params `= r(d + k)` vs `d·k` · QLoRA = 4-bit base weights
- ⌨️ **Build · L2:** compute the parameter savings for r = 8; format an SFT dataset (instruction → answer); a preference pair for DPO.
- 📊 **Measure · L2:** memory / parameter count with and without LoRA.
- 📈 **Improve · L3:** decision table "prompt vs RAG vs fine-tune" for 6 real tasks.
- 🎤 **Interview · L3:** Why does LoRA work? · RAG vs fine-tuning? · What is QLoRA?
- ✅ **Done when:** you can justify the choice for 6 tasks.


### Level 3: a real LoRA project
<a id="day-87"></a>
#### ☐ Day 87 — LoRA fine-tuning project
- 🧠 **Idea · L1:** do it for real on a small open model (≤ 1–3 B) on a free GPU.
- ➗ **Equation · L1:** same as Day 86; watch training loss and eval loss.
- ⌨️ **Build · L2:** `transformers` + `peft` + `trl`; train on 500–2 000 examples; merge or load the adapter; push to the Hugging Face Hub.
- 📊 **Measure · L2:** base vs prompted vs fine-tuned on a held-out set.
- 📈 **Improve · L3:** r = 4 → 8 → 16; LR; epochs; data quality (clean 100 bad examples).
- 🎤 **Interview · L3:** What can go wrong (overfit, forgetting, bad data)? · How do you evaluate a fine-tune? · Adapter vs merged weights?
- ✅ **Done when:** model card on the Hub + a results table.


## Chapter 44 — Image, audio and multimodal generation

### Levels 1 → 3 (inside the day)
<a id="day-88"></a>
#### ☐ Day 88 — Image generation, multimodal & speech
- 🧮 **New math today (just-in-time):** ELBO and KL (VAE), the GAN game, the diffusion noise schedule.
- 🧠 **Idea · L1:** **VAE** compresses, **GAN** plays a forger-vs-detective game, **diffusion** learns to remove noise (today's best). Vision-language models read images; Whisper hears; TTS speaks.
- ➗ **Equation · L1:** VAE `ELBO = E[log p(x|z)] − KL(q(z|x)‖p(z))` · GAN `min_G max_D E[log D(x)] + E[log(1 − D(G(z)))]` · diffusion `x_t = √ᾱ_t·x₀ + √(1−ᾱ_t)·ε`, the net predicts `ε`
- ⌨️ **Build · L2:** a tiny VAE on MNIST; `diffusers` text-to-image, image-to-image, inpainting, super-resolution; overview of style transfer and DreamBooth / LoRA personalisation; a vision-language question on a photo; Whisper transcription; a voice round-trip.
- 📊 **Measure · L2:** sample quality (look), speed, cost; word-error-rate for speech.
- 📈 **Improve · L3:** default → prompt / guidance scale / steps → negative prompts.
- 🎤 **Interview · L3:** GAN vs VAE vs diffusion? · Why is diffusion stable to train? · How does CLIP link text and images?
- ✅ **Done when:** you generated an image and transcribed an audio file.


## Chapter 45 — Safety, evaluation, cost and the GenAI project

### Level 2: safety and evals
<a id="day-89"></a>
#### ☐ Day 89 — LLM safety, evaluation, cost & latency
- 🧠 **Idea · L1:** production LLM apps fail in new ways: hallucination, prompt injection, data leaks, cost spikes.
- ➗ **Equation · L1:** p50 / p95 latency · cache hit rate `= hits/requests` · cost per 1 000 requests
- ⌨️ **Build · L2:** an **eval harness** (cases + metrics + report); guardrails (input / output checks, PII masking); response cache; batching; streaming.
- 📊 **Measure · L2:** before / after: latency, cost, error rate.
- 📈 **Improve · L3:** no guard → guard → guard + cache.
- 🎤 **Interview · L3:** What is prompt injection and how do you defend? · How do you detect hallucination? · How do you cut latency and cost?
- ✅ **Done when:** you have a red-team list of 10 attacks and the results.


### Level 3: project checkpoint
<a id="day-90"></a>
#### ☐ Day 90 — GenAI project
- 🧠 **Idea · L1:** put it all together.
- ➗ **Equation · L1:** none new — report the metrics from Day 85.
- ⌨️ **Build · L2:** **"HR policy assistant"**: RAG with citations, streaming FastAPI endpoint, eval set, cost report.
- 📊 **Measure · L2:** accuracy, citation accuracy, p95 latency, cost / question.
- 📈 **Improve · L3:** one full V1 → V4 ladder, written up.
- 🎤 **Interview · L3:** answer **20 questions** (Days 77–90). Design a RAG system on a whiteboard.
- ✅ **Checkpoint:** README + test + demo GIF.


---

### ✅ Part IX cheat card — prompt vs RAG vs fine-tune
| You need… | Use | Why |
|---|---|---|
| A different tone / format | **Prompt** (+ examples) | cheapest, instant |
| Answers from *your* documents, always current | **RAG** | knowledge lives outside the model; citations |
| A consistent style / skill / short outputs at scale | **Fine-tune (LoRA)** | bakes behaviour into weights, lower latency |
| New knowledge **and** consistent style | RAG + fine-tune | combine |
| Actions in the real world | **Agent** (Part X) | tools + loop |

[📖 Table of contents](README.md) · [← previous part](part8_reinforcement_learning.md) · [next part →](part10_agentic_ai.md) · [Appendices](appendix.md)
