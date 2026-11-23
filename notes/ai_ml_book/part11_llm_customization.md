# PART XI — Customizing and Shipping Generative AI: fine-tuning, image / audio generation, safety

[📖 Table of contents](README.md) · [← previous part](part10_embeddings_vector_retrieval_rag.md) · [next part →](part12_agentic_ai.md) · [Appendices](appendix.md)

> **Days 94–98 · Category: generative models — customize, create, protect · Levels: 1 → 3 in every chapter**
> **You will be able to:** decide between prompting, RAG and fine-tuning, build a fine-tuning dataset (including synthetic data), fine-tune an LLM with LoRA / QLoRA, understand image and audio generation, defend an LLM app against hallucination and prompt injection, and ship the HR policy assistant.
> **Math you meet here (just-in-time):** low-rank updates `W + BA` (Day 94) · ELBO, GAN game, diffusion noise (96) · latency percentiles and cache hit rate (97).
> **Builds on:** Part IX (LLM basics) and Part X (RAG). **More depth:** Advanced shelf Days 168 (PEFT variants), 169 (alignment and reasoning models), 171 (benchmarks and judges), 173 (vision-language and speech).

---

## Chapter 46 — Fine-tuning LLMs

> ⚠️ **Common mistakes:** fine-tuning to add *knowledge* (use RAG) · tiny dirty datasets · no held-out evaluation.

### Level 1–2: SFT, LoRA, QLoRA theory
<a id="day-94"></a>
#### ☐ Day 94 — Fine-tuning theory: SFT, LoRA, QLoRA
- 🧮 **New math today (just-in-time):** low-rank decomposition `W′ = W + (α/r)·B·A`.
- 🧠 **Idea · L1:** change the model itself. **LoRA** trains two tiny matrices instead of the whole weight. When to use: prompt first → RAG for knowledge → fine-tune for **style / format / skill**.
- ➗ **Equation · L1:** `W′ = W + (α/r)·B·A`, `B ∈ ℝ^{d×r}`, `A ∈ ℝ^{r×k}`, `r ≪ d` · trainable params `= r(d + k)` vs `d·k` · QLoRA = 4-bit base weights
- ⌨️ **Build · L2:** compute the parameter savings for r = 8; format an SFT dataset (instruction → answer); a preference pair for DPO.
- 📊 **Measure · L2:** memory / parameter count with and without LoRA.
- 📈 **Improve · L3:** decision table "prompt vs RAG vs fine-tune" for 6 real tasks.
- 🎤 **Interview · L3:** Why does LoRA work? · RAG vs fine-tuning? · What is QLoRA?
- ✅ **Done when:** you can justify the choice for 6 tasks.


### Level 3: a real LoRA project
<a id="day-95"></a>
#### ☐ Day 95 — LoRA fine-tuning project
- 🧠 **Idea · L1:** do it for real on a small open model (≤ 1–3 B) on a free GPU.
- ➗ **Equation · L1:** same as Day 94; watch training loss and eval loss.
- ⌨️ **Build · L2:** **build the dataset first** — collect or **synthesize** examples with an LLM, review and label them (a spreadsheet or Label Studio), remove duplicates and test-set leaks, split train / validation / test; then `transformers` + `peft` + `trl`; train on 500–2 000 examples; merge or load the adapter; push to the Hugging Face Hub.
- 📊 **Measure · L2:** base vs prompted vs fine-tuned on a held-out set.
- 📈 **Improve · L3:** r = 4 → 8 → 16; LR; epochs; data quality (clean 100 bad examples).
- 🎤 **Interview · L3:** What can go wrong (overfit, forgetting, bad data)? · How do you evaluate a fine-tune? · Adapter vs merged weights?
- ✅ **Done when:** model card on the Hub + a results table.


## Chapter 47 — Image, audio and multimodal generation

### Levels 1 → 3 (inside the day)
<a id="day-96"></a>
#### ☐ Day 96 — Image generation, multimodal & speech
- 🧮 **New math today (just-in-time):** ELBO and KL (VAE), the GAN game, the diffusion noise schedule.
- 🧠 **Idea · L1:** **VAE** compresses, **GAN** plays a forger-vs-detective game, **diffusion** learns to remove noise (today's best). Vision-language models read images; Whisper hears; TTS speaks.
- ➗ **Equation · L1:** VAE `ELBO = E[log p(x|z)] − KL(q(z|x)‖p(z))` · GAN `min_G max_D E[log D(x)] + E[log(1 − D(G(z)))]` · diffusion `x_t = √ᾱ_t·x₀ + √(1−ᾱ_t)·ε`, the net predicts `ε`
- ⌨️ **Build · L2:** a tiny VAE on MNIST; `diffusers` text-to-image, image-to-image, inpainting, super-resolution; overview of style transfer and DreamBooth / LoRA personalisation; a vision-language question on a photo; Whisper transcription; a voice round-trip.
- 📊 **Measure · L2:** sample quality (look), speed, cost; word-error-rate for speech.
- 📈 **Improve · L3:** default → prompt / guidance scale / steps → negative prompts.
- 🎤 **Interview · L3:** GAN vs VAE vs diffusion? · Why is diffusion stable to train? · How does CLIP link text and images?
- ✅ **Done when:** you generated an image and transcribed an audio file.


## Chapter 48 — Safety, evaluation, cost and the GenAI project

### Level 2: safety and evals
<a id="day-97"></a>
#### ☐ Day 97 — LLM safety, evaluation, cost & latency
- 🧠 **Idea · L1:** production LLM apps fail in new ways: hallucination, prompt injection, data leaks, cost spikes.
- ➗ **Equation · L1:** p50 / p95 latency · cache hit rate `= hits/requests` · cost per 1 000 requests
- ⌨️ **Build · L2:** an **eval harness** (cases + metrics + report); guardrails (input / output checks, PII masking); response cache; batching; streaming.
- 📊 **Measure · L2:** before / after: latency, cost, error rate.
- 📈 **Improve · L3:** no guard → guard → guard + cache.
- 🎤 **Interview · L3:** What is prompt injection and how do you defend? · How do you detect hallucination? · How do you cut latency and cost?
- ✅ **Done when:** you have a red-team list of 10 attacks and the results.


### Level 3: project checkpoint
<a id="day-98"></a>
#### ☐ Day 98 — GenAI project
- 🧠 **Idea · L1:** put it all together.
- ➗ **Equation · L1:** none new — report the metrics from Day 92 and the cost per question from Day 93.
- ⌨️ **Build · L2:** **"HR policy assistant v3"**: your Part-X RAG (Day 93) + a LoRA-tuned answer style (Day 95) + safety guards (Day 97) + a streaming FastAPI endpoint + eval set + cost report.
- 📊 **Measure · L2:** accuracy, citation accuracy, p95 latency, cost / question.
- 📈 **Improve · L3:** one full V1 → V4 ladder, written up.
- 🎤 **Interview · L3:** answer **20 questions** on Days 94–98. Design a RAG system on a whiteboard.
- ✅ **Checkpoint:** README + test + demo GIF.




---

### ✅ Part XI cheat card — prompt vs RAG vs fine-tune
| You need… | Use | Why |
|---|---|---|
| A different tone / format | **Prompt** (+ examples) | cheapest, instant |
| Answers from *your* documents, always current | **RAG** | knowledge lives outside the model; citations |
| A consistent style / skill / short outputs at scale | **Fine-tune (LoRA)** | bakes behaviour into weights, lower latency |
| New knowledge **and** consistent style | RAG + fine-tune | combine |
| Actions in the real world | **Agent** (Part XII) | tools + loop |

[📖 Table of contents](README.md) · [← previous part](part10_embeddings_vector_retrieval_rag.md) · [next part →](part12_agentic_ai.md) · [Appendices](appendix.md)
