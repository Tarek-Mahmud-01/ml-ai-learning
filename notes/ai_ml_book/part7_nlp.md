# PART VII — Natural Language Processing (NLP)

[📖 Table of contents](README.md) · [← previous part](part6_deep_learning_vision.md) · [next part →](part8_reinforcement_learning.md) · [Appendices](appendix.md)


> **Days 63–73 · Category: deep learning for text · Levels: 1 → 3 in every chapter**
> **You will be able to:** clean and represent text (BoW, TF-IDF, Vector Space Model, WordNet), use and train embeddings, explain RNN / LSTM / GRU, derive attention, build a Transformer from scratch, and fine-tune BERT with the right NLP metrics.
> **Math you meet here (just-in-time):** TF-IDF and cosine (Day 64) · skip-gram softmax (65) · back-prop through time (66) · LSTM gates (67) · attention weights (68) · `softmax(QKᵀ/√d)V` (69) · BLEU, ROUGE, perplexity (72).
> **Your class notes used:** *Vector Space Model, CountVectorizer, TF-IDF, WordNet, Stemming, Lemmatization, NLP pipeline* (in *Distance Metrics*).

---

## Chapter 33 — Text basics: cleaning, bag-of-words, TF-IDF, vector space

> ⚠️ **Common mistakes:** removing stop-words blindly ("not" matters) · fitting the vectorizer on test data · huge vocabularies without limits.

### Level 1: preprocessing, WordNet, stemming, lemmatization
<a id="day-63"></a>
#### ☐ Day 63 — Text preprocessing
- 🧠 **Idea · L1:** clean text before counting. Tokenize, lower-case, remove stop-words, stem or lemmatize, tag parts of speech, find entities.
- ➗ **Equation · L1:** vocabulary size `|V|` · type–token ratio.
- ⌨️ **Build · L2:** regex cleaning; NLTK and spaCy: tokenization, stop-words, Porter stemmer vs lemmatizer, **WordNet** (synonyms, hypernyms), POS tags, NER.
- 📊 **Measure · L2:** vocabulary size and classifier score before/after each cleaning step.
- 📈 **Improve · L3:** raw → lower-case → no stop-words → lemmatized (check each really helps).
- 🎤 **Interview · L3:** Stemming vs lemmatization? · Should you always remove stop-words? · What is NER?
- ✅ **Done when:** a reusable `clean_text()` exists with tests.


### Level 2–3: BoW, TF-IDF, the vector space model, classic classifiers
<a id="day-64"></a>
#### ☐ Day 64 — Bag-of-words, TF-IDF & classic text classification
- 🧮 **New math today (just-in-time):** TF-IDF and cosine similarity in the vector space model.
- 🧠 **Idea · L1:** count words → vectors → classic classifiers. TF-IDF down-weights common words.
- ➗ **Equation · L1:** `tf-idf(t,d) = tf(t,d)·log(N/df(t))` (sklearn uses a smoothed form) · n-grams · cosine similarity
- ⌨️ **Build · L2:** CountVectorizer + TF-IDF from scratch → sklearn; the **Vector Space Model** (each document = a vector, search by cosine); Naive Bayes / SVM / logistic sentiment classifier. Stretch: LDA topic modelling.
- 📊 **Measure · L2:** F1, confusion matrix, top words per class, worst mistakes.
- 📈 **Improve · L3:** BoW → TF-IDF → +bigrams → tuned C.
- 🎤 **Interview · L3:** Why TF-IDF over counts? · What is an n-gram? · Limits of bag-of-words?
- ✅ **Done when:** > 85 % F1 on a review dataset.


## Chapter 34 — Word embeddings

> ⚠️ **Common mistakes:** one vector per word (no context) · using a different tokenizer than the one the embeddings were trained with.

### Levels 1 → 3 (inside the day)
<a id="day-65"></a>
#### ☐ Day 65 — Word embeddings: Word2Vec, GloVe, FastText
- 🧮 **New math today (just-in-time):** skip-gram softmax, negative sampling, cosine similarity.
- 🧠 **Idea · L1:** words that appear in similar contexts get similar vectors. "king − man + woman ≈ queen".
- ➗ **Equation · L1:** skip-gram `max Σ log p(w_{t+j}|w_t)`, `p(o|c) = exp(u_o·v_c)/Σ_w exp(u_w·v_c)` · negative sampling · cosine similarity
- ⌨️ **Build · L2:** train a small Word2Vec with `gensim`; nearest neighbours; analogy test; use pretrained GloVe / FastText.
- 📊 **Measure · L2:** similarity tests; where does it fail (one vector per word, no context)?
- 📈 **Improve · L3:** TF-IDF features → averaged Word2Vec → pretrained vectors.
- 🎤 **Interview · L3:** CBOW vs skip-gram? · Why negative sampling? · Static vs contextual embeddings?
- ✅ **Done when:** you can explain why "bank" needs context.


## Chapter 35 — Sequence models: RNN, LSTM, GRU, seq2seq, attention

> ⚠️ **Common mistakes:** no gradient clipping · padding without masking · long sequences with a plain RNN.

### Level 1: RNN
<a id="day-66"></a>
#### ☐ Day 66 — Recurrent neural networks
- 🧮 **New math today (just-in-time):** back-propagation through time; vanishing / exploding gradients.
- 🧠 **Idea · L1:** read text one word at a time and keep a **memory** `h`.
- ➗ **Equation · L1:** `hₜ = tanh(Wₓₕxₜ + Wₕₕhₜ₋₁ + b)` · back-prop through time (BPTT) multiplies many `Wₕₕ` → vanishing / exploding gradients
- ⌨️ **Build · L2:** RNN cell in NumPy; `nn.RNN` sentiment model on a small dataset.
- 📊 **Measure · L2:** accuracy vs sentence length (long sentences hurt).
- 📈 **Improve · L3:** unidirectional → bidirectional → gradient clipping.
- 🎤 **Interview · L3:** Why do RNNs forget? · What is BPTT? · Why clip gradients?
- ✅ **Done when:** you can draw the unrolled RNN.


### Level 2: LSTM / GRU
<a id="day-67"></a>
#### ☐ Day 67 — LSTM & GRU
- 🧮 **New math today (just-in-time):** the LSTM / GRU gate equations (sigmoid and tanh gates).
- 🧠 **Idea · L1:** gates decide what to **forget**, **write**, **read** — a protected memory cell.
- ➗ **Equation · L1:** `f = σ(W_f[h,x] + b_f)` · `i = σ(W_i[h,x] + b_i)` · `c̃ = tanh(W_c[h,x] + b_c)` · `c = f⊙c₋₁ + i⊙c̃` · `o = σ(W_o[h,x] + b_o)` · `h = o⊙tanh(c)` · GRU: update + reset gates
- ⌨️ **Build · L2:** LSTM cell from scratch; `nn.LSTM`, `nn.GRU` sentiment classifiers; compare RNN / LSTM / GRU.
- 📊 **Measure · L2:** accuracy, parameters, speed.
- 📈 **Improve · L3:** RNN → LSTM → bi-LSTM + pretrained embeddings + dropout.
- 🎤 **Interview · L3:** How does the LSTM fix vanishing gradients? · LSTM vs GRU? · Why bidirectional?
- ✅ **Done when:** you can write the 6 LSTM equations from memory.


### Level 3: seq2seq and attention
<a id="day-68"></a>
#### ☐ Day 68 — Sequence-to-sequence & attention
- 🧮 **New math today (just-in-time):** attention weights as a softmax over scores.
- 🧠 **Idea · L1:** encoder reads, decoder writes. A single summary vector is a bottleneck → let the decoder **look back** at every encoder state (attention).
- ➗ **Equation · L1:** score `eₜₛ = score(hₜ, h̄ₛ)` · weights `αₜₛ = softmax(eₜₛ)` · context `cₜ = Σₛ αₜₛ h̄ₛ`
- ⌨️ **Build · L2:** a tiny seq2seq with attention (e.g. date formats `"3 Jan 2026" → "2026-01-03"`); plot the attention map.
- 📊 **Measure · L2:** exact-match accuracy; BLEU.
- 📈 **Improve · L3:** no attention → attention → bigger hidden size.
- 🎤 **Interview · L3:** Why attention? · Teacher forcing? · What does the attention map show?
- ✅ **Done when:** the attention heat-map looks diagonal for a copy task.


## Chapter 36 — Transformers, BERT and fine-tuning

> ⚠️ **Common mistakes:** not masking padding · LR too high for fine-tuning · judging generation with accuracy.

### Level 1–2: self-attention and the Transformer block
<a id="day-69"></a>
#### ☐ Day 69 — Self-attention & the Transformer (from scratch)
- 🧮 **New math today (just-in-time):** scaled dot-product attention `softmax(QKᵀ/√d_k)V` and positional encoding.
- 🧠 **Idea · L1:** every word looks at every other word **at once** (no recurrence). Parallel, fast, powerful.
- ➗ **Equation · L1:** `Attention(Q,K,V) = softmax(QKᵀ/√d_k)·V` · multi-head = several attentions in parallel, then concatenated · positional encoding `PE(pos,2i) = sin(pos/10000^{2i/d})` · block = attention + residual + LayerNorm + feed-forward
- ⌨️ **Build · L2:** a Transformer block in PyTorch (~60 lines); causal mask; shape table for every tensor.
- 📊 **Measure · L2:** why divide by `√d_k`? Show softmax saturation without it.
- 📈 **Improve · L3:** 1 head → 4 heads → 2 layers; check a copy / reverse task.
- 🎤 **Interview · L3:** Explain Q, K, V. · Why positional encoding? · Complexity of attention (O(n²))?
- ✅ **Done when:** you can draw the Transformer from memory.


### Level 2: pretrained models and Hugging Face
<a id="day-70"></a>
#### ☐ Day 70 — BERT, GPT, T5 & Hugging Face
- 🧠 **Idea · L1:** pretrained models. **Encoder** (BERT, masked-word), **decoder** (GPT, next-word), **encoder–decoder** (T5). BERT is a Transformer, not an RNN.
- ➗ **Equation · L1:** masked LM loss `−Σ_{masked} log p(wᵢ|context)` · causal LM `−Σ log p(wₜ|w<ₜ)` · subword tokenizers (WordPiece, BPE)
- ⌨️ **Build · L2:** `pipeline()` for sentiment, fill-mask, generation; tokenizer inspection; sentence-embedding model + semantic search.
- 📊 **Measure · L2:** zero-shot accuracy on your data.
- 📈 **Improve · L3:** zero-shot → add a classifier on frozen embeddings (preview of fine-tuning).
- 🎤 **Interview · L3:** BERT vs GPT? · Why subword tokens? · What is masked language modelling?
- ✅ **Done when:** you ran 5 different Hugging Face tasks.


### Level 3: fine-tuning, other tasks, project
<a id="day-71"></a>
#### ☐ Day 71 — Fine-tune BERT
- 🧠 **Idea · L1:** start from a pretrained model; train a little on **your** labels.
- ➗ **Equation · L1:** classification head `softmax(W·h_[CLS] + b)` · AdamW with LR ≈ 2e-5 and warm-up
- ⌨️ **Build · L2:** `datasets` + `Trainer`; tokenization with padding / truncation; evaluate F1; **error analysis** on the 30 worst examples.
- 📊 **Measure · L2:** F1 vs the TF-IDF baseline from Day 64.
- 📈 **Improve · L3:** frozen features + logistic → full fine-tune → tuned LR / epochs → DistilBERT (speed).
- 🎤 **Interview · L3:** Fine-tune vs feature extraction? · Catastrophic forgetting? · How to pick LR and epochs?
- ✅ **Done when:** fine-tuned model beats TF-IDF by a clear margin (log it).

<a id="day-72"></a>
#### ☐ Day 72 — NER, QA, summarization, translation & NLP metrics
- 🧮 **New math today (just-in-time):** BLEU, ROUGE and perplexity.
- 🧠 **Idea · L1:** other NLP tasks, each with its own metric.
- ➗ **Equation · L1:** entity-level F1 · QA exact-match / F1 · ROUGE (n-gram overlap) · `BLEU = BP·exp(Σ wₙ log pₙ)` · perplexity `= exp(−(1/N)Σ log p(wᵢ|w<ᵢ))`
- ⌨️ **Build · L2:** NER pipeline; extractive QA; summarization; translation; compute each metric by hand on 3 examples.
- 📊 **Measure · L2:** where metrics disagree with human judgement.
- 📈 **Improve · L3:** off-the-shelf → domain fine-tune idea → post-processing rules.
- 🎤 **Interview · L3:** BLEU vs ROUGE? · What is perplexity? · Token-level vs entity-level F1?
- ✅ **Done when:** you can pick the metric for each task.

<a id="day-73"></a>
#### ☐ Day 73 — NLP project
- 🧠 **Idea · L1:** put it together on your own domain.
- ➗ **Equation · L1:** none new — report F1 and error slices.
- ⌨️ **Build · L2:** **"HR document / complaint classifier + entity extractor"**; clean → model → API.
- 📊 **Measure · L2:** F1 per class; 20 worst mistakes grouped by cause.
- 📈 **Improve · L3:** TF-IDF → fine-tuned BERT → rules for the top error cause.
- 🎤 **Interview · L3:** answer **20 questions** (Days 63–73). Transformer walk-through at the whiteboard.
- ✅ **Checkpoint:** FastAPI endpoint + test + README.


---

### ✅ Part VII cheat card — text representation ladder
| Step | Representation | Context? | Good for | Limit |
|---|---|---|---|---|
| 1 | Bag-of-words (counts) | no | quick baseline | long sparse vectors, no word order |
| 2 | TF-IDF | no | search, classic classifiers | same |
| 3 | Word2Vec / GloVe / FastText | no (one vector per word) | similarity, features | "bank" has one meaning |
| 4 | RNN / LSTM states | yes (left to right) | small sequence tasks | slow, long-range forgetting |
| 5 | BERT-style embeddings | **yes** | classification, NER, QA | needs GPU, 512-token limit |
| 6 | LLM / sentence embeddings | yes | semantic search, RAG | cost, model choice |

| NLP task | Metric |
|---|---|
| Classification / sentiment | accuracy, macro-F1 |
| NER | entity-level F1 |
| Extractive QA | exact match, F1 |
| Summarization | ROUGE (+ human check) |
| Translation | BLEU / chrF |
| Language model | perplexity |

[📖 Table of contents](README.md) · [← previous part](part6_deep_learning_vision.md) · [next part →](part8_reinforcement_learning.md) · [Appendices](appendix.md)
