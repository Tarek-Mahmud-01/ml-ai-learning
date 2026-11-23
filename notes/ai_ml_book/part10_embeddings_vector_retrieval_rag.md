# PART X — Embeddings, Vector Databases, Retrievers and Augmentation (RAG)

[📖 Table of contents](README.md) · [← previous part](part9_generative_ai.md) · [next part →](part11_llm_customization.md) · [Appendices](appendix.md)

> **Days 82–93 · Category: retrieval-augmented generation — the engine behind "chat with your documents" · Levels: 1 → 3 in every chapter**
> **You will be able to:** turn any data into vectors, choose and fine-tune an embedding model, build exact and approximate vector search (IVF, PQ, HNSW), run FAISS / Chroma / pgvector / Qdrant, ingest and chunk real documents, build and measure sparse / dense / hybrid **retrievers**, improve them (rewriting, HyDE, MMR, reranking), **augment** an LLM prompt with cited context, evaluate RAG, and run it in production with access control.
> **Math you meet here (just-in-time):** cosine / dot / L2 and normalization (Day 82) · InfoNCE (83) · `O(n·d)` search and recall@k (84) · IVF, PQ, HNSW (85) · filter selectivity (86) · chunk arithmetic (87) · BM25, RRF, MRR, nDCG (88) · MMR (89) · context budget (90) · faithfulness metrics (92) · cost and latency budgets (93).
> **Builds on:** TF-IDF and the vector space model (Day 64), Word2Vec (Day 65), Transformers (Day 69), LLM APIs and prompts (Days 80–81). **Feeds:** agents (Part XII), the HR assistant crew (Day 109) and the capstone (Part XIV).
> **More depth:** Advanced shelf Days 165 (encoder family), 170 (advanced RAG: HyDE, GraphRAG, multimodal) and 186 (search and learning-to-rank, vector search at scale).

---

## Chapter 42 — Vectorization and embeddings

> **You will learn:** how text (and images, code, audio) becomes a vector, which similarity to use, how embedding models are trained, how to choose and fine-tune one.
> ⚠️ **Common mistakes:** comparing vectors from *different* models · forgetting to normalize · using a general model on a very specific domain without testing · not planning for re-embedding.

### Level 1 — Beginner: from words to vectors
<a id="day-82"></a>
#### ☐ Day 82 — Vectorization: from words to vectors (the ladder)
- 🧮 **New math today (just-in-time):** similarity measures — dot product, cosine, Euclidean distance · unit-vector normalization · the hashing trick.
- 🧠 **Idea · L1:** a computer cannot compare *meaning*, only numbers. **Vectorization** turns data into vectors. The ladder: one-hot (one 1 per word) → bag-of-words counts → TF-IDF weights → hashing trick (fixed size, no vocabulary) → **dense embeddings** (short vectors of 384–3 072 numbers, learned so that similar meaning = close). **Sparse** vectors match *words*; **dense** vectors match *meaning*. Anything can be embedded: text, images, code, audio, users, products. (Revisit Day 64 TF-IDF and Day 65 Word2Vec.)
- ➗ **Equation · L1:** `cos(a,b) = a·b / (‖a‖‖b‖)` · `‖a−b‖² = ‖a‖² + ‖b‖² − 2a·b` · for unit vectors `cos = a·b` and `‖a−b‖² = 2 − 2cos` (so cosine, dot product and L2 give the **same ranking**) · hashing `index = hash(token) mod m`
- ⌨️ **Build · L2:** vectorize 200 HR sentences 5 ways — one-hot, `CountVectorizer`, `TfidfVectorizer`, `HashingVectorizer`, then a sentence-embedding model. Compute cosine / dot / L2 by hand and with `sklearn.metrics.pairwise`; prove the "unit vectors → same ranking" fact in code. PCA / UMAP picture coloured by topic. Embed an image (CLIP) and a code snippet to see "anything can be embedded".
- 📊 **Measure · L2:** top-5 nearest sentences for 10 queries under each representation. Where sparse fails (synonyms: "salary" vs "pay") and where dense fails (exact IDs, rare names). Vector size and memory in MB.
- 📈 **Improve · L3:** BoW → TF-IDF → dense → dense + TF-IDF (a preview of hybrid search, Day 88).
- 🎤 **Interview · L3:** Sparse vs dense vectors? · Why is cosine ≈ dot product for normalized vectors? · What is the hashing trick and what is its downside (collisions)?
- ✅ **Done when:** with your own 10 queries you can show one case where TF-IDF wins and one where embeddings win.


### Level 2–3 — Intermediate to Advanced: how embedding models are trained and chosen
<a id="day-83"></a>
#### ☐ Day 83 — Embedding models: how they are trained, chosen and fine-tuned
- 🧮 **New math today (just-in-time):** contrastive loss (InfoNCE) with in-batch negatives · Matryoshka truncation · embedding quantization.
- 🧠 **Idea · L1:** an embedding model is a Transformer encoder trained so that **matching pairs (question ↔ answer, query ↔ document) land close and non-matches land far** — *contrastive learning*. A **bi-encoder** embeds query and document separately (fast; documents can be pre-computed). Choose by task (retrieval, clustering, classification), language, max tokens, size / cost and the **MTEB** leaderboard — then **test on your own data**. Many models need prefixes (`query:` / `passage:`). Changing the model means **re-embedding everything**.
- ➗ **Equation · L1:** InfoNCE `L = −log[ exp(sim(q,d⁺)/τ) / Σⱼ exp(sim(q,dⱼ)/τ) ]` (negatives = other documents in the batch + *hard negatives*) · cosine `sim` · Matryoshka: the first `k` dimensions are also a good smaller embedding · int8 `q = round(x/s)` · binary `sign(x)` with Hamming distance.
- ⌨️ **Build · L2:** compare 3 embedding models on your HR Q&A (recall@5) with `sentence-transformers`. Write InfoNCE in PyTorch (10 lines) and check it against a library loss. **Fine-tune** a small sentence-transformer on 500 (question, passage) pairs with `MultipleNegativesRankingLoss`. Truncate dimensions (768 → 256 → 64) and quantize (int8, binary). Cache embeddings on disk (hash of text → vector) and batch-encode.
- 📊 **Measure · L2:** recall@5 and MRR before vs after fine-tuning; quality loss vs size for each truncation / quantization; sentences per second; cost per 1 M tokens for an API embedding model.
- 📈 **Improve · L3:** general model → better MTEB pick → fine-tuned on your pairs → + hard negatives; log every step in the results table.
- 🎤 **Interview · L3:** How are embedding models trained? · Bi-encoder vs cross-encoder? · What happens in production if you change the embedding model? · How do you choose the dimension?
- ✅ **Done when:** the fine-tuned model beats the general model on your test queries and you can state the re-embedding plan.


## Chapter 43 — Vector databases

> **You will learn:** exact search, the ANN indexes behind every vector database (IVF, PQ, HNSW), and how FAISS, Chroma, pgvector and Qdrant differ in practice.
> ⚠️ **Common mistakes:** HNSW with default parameters and no recall check · post-filtering that returns too few results · no delete / update plan · picking a database by popularity instead of by your scale and team.

### Level 1 — Beginner: exact nearest-neighbour search
<a id="day-84"></a>
#### ☐ Day 84 — Vector search from scratch: exact nearest neighbours
- 🧮 **New math today (just-in-time):** batched dot products as one matrix product · complexity `O(n·d)` · recall@k against exact search · the curse of dimensionality.
- 🧠 **Idea · L1:** at its core a vector database does one thing: given a query vector, find the `k` stored vectors that are closest. The simplest correct method is **exact (brute-force) search** — compare with every vector. It is the baseline every index must be measured against.
- ➗ **Equation · L1:** scores `S = Q·Dᵀ` (Q: m×d queries, D: n×d documents, both normalized) · top-k with `argpartition` · cost `O(n·d)` per query · memory `n·d·4` bytes (float32) · `recall@k = |approx ∩ exact| / k` · in high dimensions `(d_max − d_min)/d_min → 0` (distances look alike).
- ⌨️ **Build · L2:** brute-force top-k in NumPy for 100 000 random vectors (d = 384); FAISS `IndexFlatIP` and `IndexFlatL2`; batching queries; float32 vs float16; measure latency and memory; simulate the curse of dimensionality (nearest vs farthest distance as `d` grows).
- 📊 **Measure · L2:** queries per second vs `n` (10 k, 100 k, 1 M if RAM allows); memory in MB; confirm NumPy = FAISS results.
- 📈 **Improve · L3:** Python loop → vectorized matrix product → FAISS Flat → float16 / GPU (awareness).
- 🎤 **Interview · L3:** Why is exact search slow at scale? · What is recall@k for a vector index? · Why do distances become less meaningful in high dimensions?
- ✅ **Done when:** you know how long exact search takes at 100 k vectors and can project it to 10 M.


### Level 2 — Intermediate: approximate indexes
<a id="day-85"></a>
#### ☐ Day 85 — Approximate nearest-neighbour (ANN) indexes: IVF, PQ, HNSW
- 🧮 **New math today (just-in-time):** k-means partitions (IVF) · product quantization codebooks · small-world graphs (HNSW).
- 🧠 **Idea · L1:** trade a little accuracy for a lot of speed. **LSH** hashes similar vectors into the same bucket. **IVF** clusters the vectors with k-means and searches only the `nprobe` nearest clusters. **PQ** compresses each vector: split it into `m` parts and store a short code per part from a small codebook (32×–64× smaller). **HNSW** builds a multi-layer graph of neighbours and walks greedily from the top layer down — the most popular index in vector databases.
- ➗ **Equation · L1:** IVF cost `≈ nlist·d + nprobe·(n/nlist)·d` · PQ `d = m·d′`, each sub-vector → one of `2^b` centroids → code of `m·b` bits, distances by lookup tables · HNSW parameters `M` (links per node), `efConstruction`, `efSearch`, search `≈ O(log n)` · recall–latency–memory trade-off.
- ⌨️ **Build · L2:** FAISS `IndexIVFFlat`, `IndexIVFPQ`, `IndexHNSWFlat` on 200 k–1 M vectors; sweep `nprobe` and `efSearch`; your own mini-IVF (k-means + inverted lists) in NumPy; measure build time and RAM; read about DiskANN and ScaNN.
- 📊 **Measure · L2:** a plot of **recall@10 vs latency** for each index and parameter; bytes per vector; build time.
- 📈 **Improve · L3:** Flat → IVF → IVF-PQ (memory) → HNSW (speed and recall); pick the knee of the curve for a 95 % recall target.
- 🎤 **Interview · L3:** IVF vs HNSW — trade-offs? · What do `nprobe` / `efSearch` control? · How does PQ compress vectors? · When is exact search still the right choice?
- ✅ **Done when:** a table "index → recall@10 → ms per query → MB" and a rule for choosing among them.


### Level 3 — Advanced: products, filtering and operations
<a id="day-86"></a>
#### ☐ Day 86 — Vector databases: products, filtering and operations (FAISS, Chroma, pgvector, Qdrant)
- 🧮 **New math today (just-in-time):** selectivity of a metadata filter · memory estimate for HNSW.
- 🧠 **Idea · L1:** an index is only a library. A **vector database** adds what a real app needs: persistence, insert / update / **delete**, **metadata filtering** (`department = "HR" AND year = 2026`), hybrid search, multi-tenancy (namespaces / collections), replicas and sharding, backups, access control and an API. Filtering can run **before** the search (exact but may be slow), **after** (fast but may return too few hits) or **inside the index** (best — e.g. filterable HNSW). Choose by scale, team skills and operations cost.
- ➗ **Equation · L1:** post-filter returns about `k·s` results (`s` = fraction passing the filter), so fetch `k/s` candidates · pgvector operators `<->` (L2), `<=>` (cosine), `<#>` (negative inner product) · memory `≈ n·d·4 B` (+ `≈ n·M·8 B` for the HNSW graph).
- ⌨️ **Build · L2:** the same 50 k HR chunks in **FAISS**, **Chroma** (persistent client), **pgvector** (Postgres + `CREATE INDEX … USING hnsw (embedding vector_cosine_ops)`) and **Qdrant** (Docker: collection, payload filter, upsert, delete, snapshot). Same queries and filters in each; filter by department and date; delete + re-insert; restart and check persistence.
- 📊 **Measure · L2:** recall@10, p95 latency, build time, RAM and lines of code per system; recall of *filtered* queries (the post-filter pitfall).
- 📈 **Improve · L3:** unfiltered → filtered; default index parameters → tuned (`m`, `ef_construct`); one node → read about replicas and sharding.
- 🎤 **Interview · L3:** Vector DB vs FAISS? · Pre- vs post-filtering? · pgvector vs Qdrant vs Pinecone — how do you choose? · How do you update and delete vectors safely?
- ✅ **Done when:** the comparison table below this chapter is filled from your own measurements and you can pick a database for your company case.


## Chapter 44 — Retrievers

> **You will learn:** ingestion (parsing and chunking), BM25, dense and hybrid retrieval, retrieval metrics, and the techniques that make retrieval better (rewriting, HyDE, MMR, reranking).
> ⚠️ **Common mistakes:** one chunk size for everything · skipping table / PDF parsing problems · never measuring the retriever alone · adding techniques without measuring the gain.

### Level 1 — Beginner: ingestion — parsing and chunking
<a id="day-87"></a>
#### ☐ Day 87 — Ingestion: parsing and chunking documents
- 🧮 **New math today (just-in-time):** chunk-size / overlap arithmetic · tokens vs characters.
- 🧠 **Idea · L1:** retrieval quality starts *before* the vector database. **Parse** the document correctly (PDF text vs scans that need OCR, tables, headers and footers, web boilerplate), **clean** it, attach **metadata** (source, page, section, date, owner, access level), then **chunk**. Strategies: fixed-size, recursive (paragraph → sentence), sentence-window, **semantic** (split where embedding similarity drops), **structure-aware** (Markdown headings, tables), **parent–child** (search small chunks, return the bigger parent). Too small = no context; too big = diluted and expensive.
- ➗ **Equation · L1:** `#chunks = ⌈(L − o)/(c − o)⌉` for text length `L`, chunk size `c`, overlap `o` · semantic split when `cos(sᵢ, sᵢ₊₁) < θ` · token budget `k·c ≤ window − prompt − answer`.
- ⌨️ **Build · L2:** parse a PDF (`pypdf`, `unstructured` or `docling`), a DOCX, a web page and a scanned page (OCR with Tesseract or `docling`); keep tables as Markdown; write fixed, recursive, semantic and Markdown-aware chunkers and a parent–child retriever. **Idempotent ingestion:** content hash → upsert, skip unchanged, delete removed.
- 📊 **Measure · L2:** a chunk-size sweep (200 / 400 / 800 / 1 200 tokens) against recall@5 on 20 questions you write now; % of chunks with broken tables or cut sentences.
- 📈 **Improve · L3:** fixed 1 000 → recursive 400 + overlap → structure-aware + metadata → parent–child.
- 🎤 **Interview · L3:** How do you choose chunk size? · What goes wrong with PDFs? · What is parent–child retrieval? · How do you avoid duplicate chunks on re-ingestion?
- ✅ **Done when:** your HRM rulebook is ingested with metadata and you can show the best chunk size from a measured sweep.


### Level 2 — Intermediate: sparse, dense and hybrid retrieval
<a id="day-88"></a>
#### ☐ Day 88 — Retrievers: sparse (BM25), dense and hybrid — and how to measure them
- 🧮 **New math today (just-in-time):** BM25 · Reciprocal Rank Fusion · hit rate, MRR and nDCG.
- 🧠 **Idea · L1:** a **retriever** takes a question and returns the best chunks. **Sparse (BM25)** = keyword match with smart weighting — great for names, codes, exact terms. **Dense** = embedding similarity — great for meaning. **Hybrid** = both fused (usually best). **Multi-vector (ColBERT)** keeps one vector per token for finer matching. Always **measure the retriever alone**, before any LLM is involved.
- ➗ **Equation · L1:** BM25 `Σₜ IDF(t)·f(t,d)(k₁+1) / (f(t,d) + k₁(1−b+b·|d|/avgdl))` · RRF `score(d) = Σᵢ 1/(k + rankᵢ(d))`, `k ≈ 60` · `hit@k` · `MRR = (1/Q)Σ 1/rankᵢ` · `nDCG@k = DCG@k / IDCG@k`, `DCG = Σ relᵢ / log₂(i+1)`.
- ⌨️ **Build · L2:** BM25 from scratch → `rank_bm25`; the dense retriever from Day 86; hybrid with RRF and with weighted scores; metadata filters. **A labeled test set:** 50 questions → relevant chunk ids (write 20 by hand, generate 30 with an LLM, review them).
- 📊 **Measure · L2:** hit@5, recall@10, MRR, nDCG@10 for BM25 vs dense vs hybrid; a per-question failure list (why was the right chunk missed?).
- 📈 **Improve · L3:** BM25 only → dense only → hybrid RRF → weighted + filters.
- 🎤 **Interview · L3:** BM25 vs embeddings — when does each win? · Why RRF? · Recall@k vs MRR vs nDCG? · How do you build a retrieval test set?
- ✅ **Done when:** a results table where hybrid beats both single methods (or a clear explanation of why not).


### Level 3 — Advanced: making retrieval better
<a id="day-89"></a>
#### ☐ Day 89 — Improving retrieval: query transformation, MMR and reranking
- 🧮 **New math today (just-in-time):** maximal marginal relevance · cross-encoder scoring.
- 🧠 **Idea · L1:** retrieval is often the bottleneck. Fixes: **query rewriting** (typos, acronyms), **multi-query** (several paraphrases merged with RRF), **decomposition** (split a multi-part question), **HyDE** (embed a hypothetical answer), **MMR** (diverse results), **cross-encoder reranking** (retrieve 50, rerank to 5), **contextual chunks** (prepend a short document summary to every chunk before embedding) and a **score threshold** (answer "no result" when nothing is close).
- ➗ **Equation · L1:** MMR `argmax_d [ λ·sim(d,q) − (1−λ)·maxₛ∈S sim(d,s) ]` · HyDE `q′ = embed(LLM(q))` · reranker score `s(q,d) = g([q ; d])` (query and document are read *together* by one model).
- ⌨️ **Build · L2:** add rewriting, multi-query + RRF, HyDE, MMR and a cross-encoder reranker (`bge-reranker` or a hosted rerank API) to your Day-88 retriever; contextual-chunk preprocessing; a score cut-off for abstention.
- 📊 **Measure · L2:** hit@5, MRR, nDCG@10, latency and extra LLM cost for each technique; which questions each technique fixes.
- 📈 **Improve (V1 → V4) · L3:** hybrid → + rewrite → + rerank (top-50 → 5) → + contextual chunks; keep only what pays for itself.
- 🎤 **Interview · L3:** What does a reranker add over a bi-encoder? · When does HyDE help or hurt? · Why MMR? · How do you decide retrieval is "not good enough" and abstain?
- ✅ **Done when:** a measured gain of at least 10 % hit@5 over the Day-88 baseline, with the cost per query noted.


## Chapter 45 — Augmentation and generation (RAG)

> **You will learn:** how to build the augmented prompt, cite sources, handle follow-ups, evaluate retrieval and generation separately, and run RAG in production.
> ⚠️ **Common mistakes:** no "I don't know" rule · no citations · judging answers by feel · no access control · stale indexes.

### Level 1 — Beginner: build the augmented prompt
<a id="day-90"></a>
#### ☐ Day 90 — Augmentation: building the prompt from retrieved context (RAG v1)
- 🧮 **New math today (just-in-time):** the context token budget.
- 🧠 **Idea · L1:** the model does not know *your* documents. **Augmentation** = put the retrieved chunks into the prompt and tell the model to answer **only** from them. Design the **context assembly**: instructions, numbered sources, the question, the output format, and "say you don't know if the context lacks the answer". Order matters (models under-use the middle: *lost in the middle*); respect the **token budget**.
- ➗ **Equation · L1:** `k·c + P + A ≤ W` (k chunks of c tokens, prompt P, answer A, context window W) · abstain if `best score < θ`.
- ⌨️ **Build · L2:** end-to-end RAG v1 on the HRM rulebook: retrieve (Day 89) → assemble the prompt with numbered sources → LLM → answer ("What is the overtime policy?"). Try 3 prompt templates and best-first vs best-at-the-ends ordering. Refusal test: ask 5 things that are not in the documents.
- 📊 **Measure · L2:** 20 test questions — right chunk retrieved? answer correct? answer supported by the context? refusal rate on out-of-scope questions.
- 📈 **Improve · L3:** V1 chunk 1 000 → V2 chunk 400 + overlap → V3 tuned k + ordering → V4 + abstain rule.
- 🎤 **Interview · L3:** What is RAG and why not fine-tune? · What if the answer is not in the documents? · What is "lost in the middle"? · How do you keep the answer inside the context?
- ✅ **Done when:** at least 15 / 20 answers are correct and the assistant says "I don't know" on 5 / 5 out-of-scope questions.


### Level 2 — Intermediate: citations, follow-ups, streaming
<a id="day-91"></a>
#### ☐ Day 91 — Cited and conversational RAG
- 🧮 **New math today (just-in-time):** similarity threshold for a semantic cache · citation precision.
- 🧠 **Idea · L1:** users ask follow-ups ("and for part-time staff?"). A **history-aware retriever** first rewrites the question into a standalone one using the chat history. Answers need **citations** (source file + page) so people can verify them. **Stream** the answer. Add a **semantic cache**: if a new question is almost the same as an old one, reuse the answer.
- ➗ **Equation · L1:** standalone query `q* = LLM(history, q)` · cache hit if `cos(q, qᵢ) ≥ θ` · citation precision `= cited chunks that really support the claim / all cited chunks`.
- ⌨️ **Build · L2:** question condensation; answer format `… [1][3]` with a sources list (file, page); verify each citation with a second check (string match or entailment); an SSE streaming endpoint (FastAPI); a semantic cache with TTL and a version key (invalidate when documents change).
- 📊 **Measure · L2:** citation precision and recall on 30 questions; follow-up accuracy with and without condensation; cache hit rate and wrong-hit rate.
- 📈 **Improve · L3:** no history → condensation → + citation check → + cache.
- 🎤 **Interview · L3:** How do you handle follow-up questions in RAG? · How do you make citations trustworthy? · What are the risks of semantic caching?
- ✅ **Done when:** every answer in your test set has correct citations and follow-ups work.


### Level 3 — Advanced: evaluation and production
<a id="day-92"></a>
#### ☐ Day 92 — RAG evaluation: retrieval vs generation
- 🧮 **New math today (just-in-time):** context precision / recall, faithfulness and answer-relevance metrics · judge agreement (Cohen's κ).
- 🧠 **Idea · L1:** split every failure into **retrieval** (the right chunk was not found or ranked low) or **generation** (the chunk was found but the answer is wrong or unsupported). Measure both separately on a fixed eval set. An LLM judge is useful but must be checked against human labels.
- ➗ **Equation · L1:** context recall `= facts found in the context / facts needed` · context precision `= relevant chunks / retrieved chunks` · faithfulness `= supported claims / all claims` · `MRR = (1/Q)Σ 1/rankᵢ` · Cohen's `κ = (p_o − p_e)/(1 − p_e)`.
- ⌨️ **Build · L2:** an eval set of 40–60 Q&A (half by hand, half **synthetic** — ask an LLM to write a question and gold answer from each chunk, then review them); retrieval metrics + a judge prompt (and the `ragas` library); a failure table by cause (parsing, chunking, retrieval, ranking, prompt, generation, missing document); compare the judge with 20 human labels.
- 📊 **Measure · L2:** metrics for V1…V4; the biggest failure cause; judge-vs-human κ.
- 📈 **Improve · L3:** fix the top cause → re-run → log.
- 🎤 **Interview · L3:** How do you evaluate RAG? · LLM-as-judge risks? · Retrieval failure vs generation failure? · How do you build an eval set without labels?
- ✅ **Done when:** a results table shows V1 → V4 gains and a ranked failure list.

<a id="day-93"></a>
#### ☐ Day 93 — Production RAG (checkpoint)
- 🧮 **New math today (just-in-time):** freshness lag · cost per query · per-stage latency budget.
- 🧠 **Idea · L1:** a demo becomes a product when it is **fresh** (incremental indexing, deletions), **safe** (per-user **access control** enforced as metadata filters *before* retrieval, PII handling), **fast and cheap** (caching, a small model for rewriting, a latency budget per stage), **observable** (trace every stage, log retrieved ids, feedback buttons) and **improvable** (A/B test retrievers). Beyond text: **tables / SQL + vectors**, **images (multimodal RAG)**, **GraphRAG**, **agentic RAG** (the agent decides when and what to retrieve) — see the shelf.
- ➗ **Equation · L1:** freshness lag `= t_available − t_changed` · cost per query `= embed + retrieve + rerank + LLM (tokens_in·p_in + tokens_out·p_out)` · latency `= Σ stage latencies` (watch the p95 of each stage).
- ⌨️ **Build · L2:** the **HR Policy Assistant v2**: scheduled incremental ingestion (hash diff), per-role filters (HR sees all, managers see their own department), PII masking in logs, caching, tracing (Langfuse or similar), a feedback endpoint, an A/B flag for rerank on / off; load test with 20 simulated users.
- 📊 **Measure · L2:** p95 latency per stage, cost per query, freshness lag, a **leak test** (user A can never see user B's documents), quality metrics from Day 92.
- 📈 **Improve (checkpoint) · L3:** V1 → V4 on quality *and* cost; list the 3 biggest production risks and their mitigations.
- 🎤 **Interview · L3:** answer **20 questions** on Days 82–93. Design RAG for 5 000 employees with different permissions. · How do you keep the index fresh? · How do you stop data leaks between users?
- ✅ **Done when:** the access-control leak test passes (0 leaks) and the README has an architecture diagram and your metrics.


---

### ✅ Part X cheat card — which vector database?
| System | Type | Hosting | Index | Metadata filtering | Best for | Watch out |
|---|---|---|---|---|---|---|
| **FAISS** | library | in your process | Flat, IVF, PQ, HNSW, GPU | none built in (you filter) | research, batch jobs, full control | no persistence / CRUD / server |
| **Chroma** | embedded or server DB | local / self-host | HNSW | yes | prototypes, small apps | scale and high availability |
| **pgvector** | Postgres extension | any Postgres | HNSW, IVFFlat | yes — SQL `WHERE`, joins, transactions | you already run Postgres; up to tens of millions of vectors | memory tuning; no built-in sharding |
| **Qdrant** | purpose-built DB | self-host / cloud | HNSW (+ quantization) | rich payload filters, filterable HNSW | production, filter-heavy search | you must operate it |
| **Milvus** | distributed DB | self-host / cloud | HNSW, IVF, DiskANN, GPU | yes | very large scale (100 M+) | operational complexity |
| **Weaviate** | DB with modules | self-host / cloud | HNSW, flat | yes + built-in hybrid (BM25) | hybrid search, schema + modules | resource use |
| **Pinecone** | managed service | cloud only | proprietary | yes, namespaces | zero-ops, fast to scale | vendor lock-in, cost |
| **Elasticsearch / OpenSearch** | search engine | self-host / cloud | HNSW | very rich + BM25 | you already run it; strong hybrid | heavier, needs tuning |

### ✅ Part X cheat card — which index?
| Index | Memory | Speed | Recall | Build | Use when |
|---|---|---|---|---|---|
| Flat (exact) | `n·d·4` B | slow `O(n·d)` | 100 % | none | up to ~100 k vectors, or as ground truth |
| IVF-Flat | `n·d·4` B | fast | 90–99 % (`nprobe`) | k-means training | 100 k–10 M vectors, RAM is fine |
| IVF-PQ | tiny (≈ `m` bytes per vector) | fast | 80–95 % | training | RAM-limited, 10 M+ vectors |
| HNSW | `n·d·4` B + graph | fastest at high recall | 95–99 % | slower, incremental inserts | **default for most apps** |
| DiskANN | on SSD | fast | high | long | billion-scale on disk |

### ✅ Part X cheat card — which chunking?
| Document type | Strategy |
|---|---|
| Policies and manuals with headings | structure-aware (Markdown / headings) + parent–child |
| Chats and emails | one message or a thread window |
| Contracts and legal text | clause-based, metadata, small overlap |
| Tables and spreadsheets | row groups with the header repeated — or use SQL |
| Source code | by function / class |
| Plain unstructured text | recursive 300–500 tokens with 10–20 % overlap; semantic if budget allows |

### ✅ Part X cheat card — retrieval metrics
| Metric | Question it answers | Formula |
|---|---|---|
| hit@k | Is *any* relevant chunk in the top k? | `1[∃ relevant in top k]` averaged |
| recall@k | What share of the relevant chunks did we find? | `found / relevant` |
| MRR | How high is the first relevant chunk? | `(1/Q) Σ 1/rankᵢ` |
| nDCG@k | Are the *best* chunks near the top? | `DCG@k / IDCG@k` |
| Context precision | How much of what we retrieved is useful? | `relevant retrieved / retrieved` |

### ✅ Part X cheat card — RAG failure → fix
| Symptom | Likely cause | Fix |
|---|---|---|
| The right document is never retrieved | parsing, chunking or embedding mismatch | fix ingestion · hybrid search · fine-tune embeddings · larger `k` |
| Right chunk retrieved but ranked low | weak ranking | cross-encoder rerank · hybrid · MMR |
| Answer ignores the context | prompt or ordering | stricter instruction · reorder · fewer chunks |
| Made-up facts | no abstain rule | score threshold + "I don't know" · citation check |
| Stale answers | no re-indexing | incremental ingestion · cache invalidation by version |
| Leaks another user's data | no access control | metadata filters **before** retrieval |
| Slow or expensive | too many chunks, big model everywhere | smaller `k`, cache, rerank then trim, small model for rewriting |

[📖 Table of contents](README.md) · [← previous part](part9_generative_ai.md) · [next part →](part11_llm_customization.md) · [Appendices](appendix.md)
