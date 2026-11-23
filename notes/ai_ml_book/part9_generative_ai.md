# PART IX — Generative AI and Large Language Models: foundations

[📖 Table of contents](README.md) · [← previous part](part8_reinforcement_learning.md) · [next part →](part10_embeddings_vector_retrieval_rag.md) · [Appendices](appendix.md)

> **Days 77–81 · Category: generative models (text) · Levels: 1 → 3 in every chapter**
> **You will be able to:** explain and build a tiny GPT, call LLM APIs (hosted *and* local) with streaming and cost control, and write tested prompts with structured output.
> **Math you meet here (just-in-time):** next-token probability and perplexity (Day 77) · temperature, top-k, top-p (79).
> **Next:** Part X (Days 82–93) teaches embeddings, vector databases, retrievers and RAG in depth. Part XI (Days 94–98) covers fine-tuning, image / audio generation and safety.
> **More depth:** Advanced shelf Days 164–173 (encoder family, tokenizers, RoPE / KV-cache, PEFT variants, DPO / GRPO, advanced RAG, benchmarks, long context, vision-language and speech).

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
#### ☐ Day 80 — LLM APIs and local models: messages, streaming, cost
- 🧠 **Idea · L1:** use a hosted model through an API. Know: system prompt, messages, `max_tokens`, `temperature`, streaming, rate limits, retries.
- ➗ **Equation · L1:** cost `= (in_tokens × price_in) + (out_tokens × price_out)`
- ⌨️ **Build · L2:** Claude API: first call, multi-turn chat, streaming, token counting, retry with back-off, error handling; a tiny CLI chat. **Local models:** run an open model with **Ollama** or `llama.cpp` (GGUF files, 4-bit quantization), call it through the same OpenAI-compatible interface, and compare quality, speed and cost with the hosted model — the privacy option for company data.
- 📊 **Measure · L2:** latency (first token / total), tokens, cost per call.
- 📈 **Improve · L3:** non-streaming → streaming; long prompt → trimmed prompt (cost drops).
- 🎤 **Interview · L3:** System vs user message? · How do you handle rate limits? · How do you cut cost? · When would you run a model locally instead of calling an API?
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

[📖 Table of contents](README.md) · [← previous part](part8_reinforcement_learning.md) · [next part →](part10_embeddings_vector_retrieval_rag.md) · [Appendices](appendix.md)
