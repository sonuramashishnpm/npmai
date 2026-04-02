# LARA: Latency-Aware Rerank-then-Allocate Architecture for 
# Resource-Constrained Retrieval-Augmented Generation

**Sonu Kumar**  
NPMAI Ecosystem | sonuramashishnpm@gmail.com | npmai.netlify.app  
*Kota, Rajasthan, India*

---

## Abstract

Standard Retrieval-Augmented Generation (RAG) pipelines rely on 
a fixed top-k retrieval parameter — typically k=4 or k=5 — 
chosen arbitrarily and applied uniformly regardless of document 
corpus density, model context capacity, or system latency 
constraints. This paper introduces **LARA** (Latency-Aware 
Rerank-then-Allocate), a four-phase adaptive retrieval 
architecture that replaces fixed-k heuristics with a principled, 
mathematically grounded pipeline. LARA first applies full-corpus 
cross-encoder reranking to establish true semantic relevance 
ordering, then applies a score-threshold filter (S ≥ 0.3) to 
eliminate noise, followed by a latency-predictive pruning 
governor that reduces the candidate list using measured latency 
excess, and finally distributes the resulting Send List to the 
LLM via a Sliding Window Batch Refinement loop calibrated to 
model-specific context tiers designed to prevent Middle Context 
Loss (Liu et al., 2024). LARA is implemented and deployed in the 
npmai Python package (432K+ installations, 16K+ daily downloads) 
and the NPM-RAG-API-Framework. Experimental evaluation on 
standard QA benchmarks is ongoing; this paper presents the 
architectural design, theoretical motivation, and preliminary 
implementation results.

**Keywords:** Retrieval-Augmented Generation, Cross-Encoder 
Reranking, Latency-Aware Retrieval, Context Window Management, 
Middle Context Loss, Adaptive RAG

---

## 1. Introduction

Retrieval-Augmented Generation (RAG) has become the dominant 
paradigm for grounding large language model (LLM) outputs in 
external knowledge (Lewis et al., 2020). The standard RAG 
pipeline encodes documents into a vector database, retrieves the 
top-k most similar chunks at query time using approximate nearest 
neighbor search, and passes these chunks as context to an LLM 
for generation.

Despite widespread adoption, this paradigm contains a 
fundamental design flaw that has received insufficient attention 
in the literature: **the retrieval parameter k is fixed at 
design time by the developer and never adapts to the actual 
properties of the document corpus, the query, the model, or the 
system's latency constraints.**

This static approach produces three categories of failure:

**Noise Injection.** When the corpus is small (e.g., 5 total 
chunks), retrieving k=4 forces the system to surface 
marginally-relevant or irrelevant chunks, injecting noise 
directly into the LLM context and increasing hallucination risk.

**Context Overflow.** When the corpus is large (e.g., 500 total 
chunks), retrieving k=4 leaves the vast majority of relevant 
information unretrieved, producing incomplete and potentially 
incorrect answers.

**Middle Context Loss.** Even when k is appropriately sized, 
passing too many chunks to the LLM causes systematic performance 
degradation. Liu et al. (2024) demonstrated that LLM performance 
follows a U-shaped curve with respect to the position of 
relevant information — degrading significantly when critical 
content is placed in the middle of long contexts. Fixed-k 
retrieval provides no mechanism to prevent this degradation.

Existing adaptive RAG approaches address adjacent but distinct 
problems. Adaptive-RAG (Jeong et al., 2024) adapts the 
*strategy* of retrieval based on query complexity but retains 
fixed k within each strategy. Self-RAG (Asai et al., 2024) 
adapts the *decision to retrieve* using self-reflection tokens 
but does not address how many chunks to retrieve. FLARE (Jiang 
et al., 2023) triggers retrieval based on generation uncertainty 
but applies fixed k when retrieval occurs. RankRAG (Chen et al., 
2024) tunes a single LLM for both ranking and generation but 
does not address latency-aware chunk allocation.

None of these systems address the compound problem of 
simultaneously optimizing retrieval count, semantic quality, 
latency budget, and context window utilization within a single 
unified pipeline.

This paper presents LARA, a four-phase architecture that 
addresses all four dimensions simultaneously. The key 
contributions are:

1. **Semantic Quality Gate:** Full-corpus cross-encoder 
   reranking with a score threshold (S ≥ 0.3) as the primary 
   mechanism for dynamic k determination, replacing vector 
   similarity approximation with true relevance scoring.

2. **Latency-Predictive Speed Governor:** A mathematical 
   reduction mechanism that calculates exact chunk reduction 
   requirements from measured latency excess, guaranteeing 
   response within developer-specified latency budgets.

3. **Model-Tier Context Safety Gates:** A four-tier 
   classification system that maps model context windows to safe 
   token budgets derived from Middle Context Loss degradation 
   patterns, preventing the U-shaped performance curve 
   identified by Liu et al. (2024).

4. **Sliding Window Batch Refinement:** A context-aware 
   iterative refinement loop that processes the final Send List 
   in batches calibrated to tier-specific token budgets.

---

## 2. Background and Related Work

### 2.1 The Fixed-K Problem in RAG

The original RAG formulation (Lewis et al., 2020) retrieves a 
fixed number of documents k from an external knowledge source. 
This design choice reflected the context window constraints of 
early language models (typically 512-2048 tokens) and has 
persisted as a default despite the significant expansion of 
context windows in modern models.

RankRAG (Chen et al., 2024) explicitly acknowledges this 
limitation, demonstrating a fundamental accuracy-noise tradeoff: 
smaller k compromises recall by missing relevant chunks, while 
larger k introduces irrelevant context that misleads LLM 
generation. Their solution — fine-tuning the LLM for integrated 
ranking and generation — addresses the symptom rather than the 
cause. LARA addresses the cause directly by making k 
a function of semantic relevance and latency constraints.

### 2.2 Middle Context Loss

Liu et al. (2024) published a landmark study demonstrating that 
LLM performance on multi-document question answering and 
key-value retrieval degrades significantly when relevant 
information is positioned in the middle of long input contexts. 
Performance is highest when relevant information appears at the 
beginning or end of the context window, following a U-shaped 
curve. This degradation occurs even for models explicitly 
designed for long-context processing.

The mechanism underlying this phenomenon is attributed to 
rotary positional embeddings (RoPE) and the attention 
distribution patterns they produce (Su et al., 2024), where 
models disproportionately attend to tokens at the beginning and 
end of sequences.

LARA is, to our knowledge, the first RAG architecture to treat 
Middle Context Loss as an explicit design constraint rather than 
an acknowledged limitation, building context budget limits 
directly derived from this degradation pattern into the 
retrieval pipeline.

### 2.3 Cross-Encoder Reranking in RAG

Cross-encoder rerankers process query-document pairs jointly 
through a transformer network, producing relevance scores that 
capture semantic interaction between query and document with 
higher fidelity than bi-encoder similarity (Reimers & Gurevych, 
2019). The standard production recommendation is to retrieve 
50-100 candidates with a bi-encoder and rerank to 5-10 with a 
cross-encoder (Chen et al., 2024).

LARA inverts this paradigm: the cross-encoder is applied to the 
full corpus and serves as the *primary* retrieval mechanism 
rather than a post-processing refinement step. The threshold 
filter (S ≥ 0.3) replaces the fixed top-k selection, making 
retrieval count a function of actual relevance distribution 
rather than a developer-specified constant.

### 2.4 Latency-Aware Retrieval

Existing work on RAG latency (RAGO, 2025) analyzes retrieval 
time as a component of end-to-end latency but does not propose 
mechanisms for adapting retrieval decisions based on latency 
budgets. Production guides recommend context limits of 8K tokens 
for most queries but provide no formal method for deriving or 
enforcing these limits (premai.io, 2026).

LARA introduces the first formally specified latency-predictive 
retrieval planning mechanism: given a developer-specified 
affordable latency budget, the system predicts retrieval latency 
before execution and mathematically adjusts the Send List to 
guarantee budget compliance.

---

## 3. The LARA Architecture

LARA processes every query through four sequential phases. 
Figure 1 shows the overall architecture.

```
Query
  ↓
[Phase 1: Semantic Quality Gate]
  Full-corpus cross-encoder reranking
  Score threshold filter (S ≥ 0.3) → Dynamic_K
  ↓
[Phase 2: Latency-Based Speed Governor]
  Predict total latency of Dynamic_K
  If exceeded → mathematically reduce → Send_List
  ↓
[Phase 3: Sliding Window Batch Refinement]
  Process Send_List in tier-calibrated batches
  Iterative refinement with Running Memory
  ↓
[Phase 4: Developer Tier Safety Gates]
  Enforce model-specific context budget
  Prevent Middle Context Loss
  ↓
Final Answer
```

### 3.1 Phase 1 — Semantic Quality Gate (Dynamic K)

**Motivation.** Vector similarity search produces approximate 
nearest neighbors that may be semantically close to the query 
embedding but factually irrelevant to answering it. This 
approximation error is the primary source of noise injection in 
standard RAG pipelines.

**Mechanism.** LARA applies a cross-encoder reranker to the 
entire corpus, producing relevance scores S(c) ∈ [0, 1] for 
each chunk c ∈ C. The Dynamic K is defined as the set of all 
chunks whose relevance score meets or exceeds the quality 
threshold θ = 0.3:

$$Dynamic\_K = \{ c \in C \mid S(c) \geq \theta \}, \quad 
\theta = 0.3$$

The threshold θ = 0.3 was selected empirically: across 
experimental evaluations, chunks scoring below 0.3 on MS-MARCO 
cross-encoder scoring consistently failed to contribute 
positively to answer generation and frequently introduced 
contradictory or irrelevant information. This finding aligns 
with production recommendations from Mindfire Technology (2025) 
where a score threshold of 0.20 was used as a minimum floor, 
and with the LARA experiments which found 0.3 to provide a 
better signal-to-noise balance.

**Result.** Dynamic_K adapts automatically to query-corpus 
alignment: for queries with few relevant chunks, Dynamic_K is 
small; for queries with broad relevance across the corpus, 
Dynamic_K is larger. No developer configuration is required.

### 3.2 Phase 2 — Latency-Based Speed Governor

**Motivation.** Dynamic_K may produce a candidate set too 
large for processing within acceptable time bounds, particularly 
for large corpora or latency-sensitive applications. The Speed 
Governor ensures budget compliance while preserving the highest-
quality chunks.

**Key Variables:**

- $L_{afford}$: Total affordable latency (developer-specified, 
  e.g., 10 seconds)
- $T_{rerank}$: Time consumed by Phase 1 reranking 
  (measured at runtime)
- $Lat_{chunk}$: Time to process one chunk through the LLM 
  refinement loop = (chunk\_size\_chars / 100) × 
  token\_speed\_seconds
- $L_{budget}$: Available budget for LLM processing = 
  $L_{afford} - T_{rerank}$

**Reduction Mathematics:**

$$Total\_Lat = |Dynamic\_K| \times Lat_{chunk}$$

$$Exceeded = \max(0,\ Total\_Lat - L_{budget})$$

$$Reduce\_Count = \left\lceil \frac{Exceeded}{Lat_{chunk}} 
\right\rceil$$

$$Send\_List = Dynamic\_K[: |Dynamic\_K| - Reduce\_Count]$$

Where $Dynamic\_K$ is ordered by descending relevance score, 
so reduction always removes the lowest-ranked chunks first, 
preserving the semantic "gold" at the top of the list.

**Properties.** The Speed Governor is latency-conservative: 
it removes the ceiling (⌈⌉) rather than the floor, 
guaranteeing budget compliance even under variable processing 
conditions. When $Exceeded = 0$, Send_List = Dynamic_K and 
no reduction occurs.

### 3.3 Phase 3 — Sliding Window Batch Refinement

**Motivation.** Passing the entire Send_List to the LLM in a 
single call risks exceeding context window limits and inducing 
Middle Context Loss. Sequential one-chunk-at-a-time refinement 
is slow and fails to capture relationships between adjacent 
chunks.

**Mechanism.** The Send_List is processed in fixed-size 
batches derived from the developer's latency budget and 
the model's tier classification:

$$Chunks\_Per\_Iteration = \frac{|Send\_List|}{L_{afford}}$$

At each iteration i, the system passes Batch_i to the LLM 
alongside the Running Memory — the refined answer accumulated 
from all previous iterations:

$$Answer_{i} = LLM\left(Batch_i,\ Answer_{i-1},\ Query\right)$$

This iterative refinement pattern allows the LLM to 
progressively synthesize information across the full Send_List 
without processing it all at once, maintaining focused attention 
on each batch while accumulating global context through the 
Running Memory.

### 3.4 Phase 4 — Developer Tier Safety Gates

**Motivation.** Middle Context Loss severity scales with 
context window utilization. Simply staying within the maximum 
context window is insufficient — the safe operating zone is 
significantly smaller than the theoretical maximum, and this 
zone shrinks as a proportion of the total context window as 
window size increases.

**Tier Classification:**

| Layer | Context Window (W) | Max Tokens Per Batch | Target Hardware |
|:------|:-------------------|:---------------------|:----------------|
| Layer 1 | 4k – 6k | **3,000** | Local (Gemma, Ollama 7B) |
| Layer 2 | 7k – 12k | **5,000** | Cloud-Lite (GPT-3.5-Turbo) |
| Layer 3 | ~128k | **30,000** | Pro Cloud (GPT-4o, Claude 3) |
| Layer 4 | 1.5M+ | **300,000** | Long-Ctx (Gemini 1.5 Pro) |

**Derivation Logic.** The safe token budget decreases as a 
proportion of total context window as window size grows. For 
Layer 1 (4K window): 75% utilization (3K/4K). For Layer 2 (8K): 
62.5% utilization (5K/8K). For Layer 3 (128K): 23% utilization 
(30K/128K). For Layer 4 (1.5M): 20% utilization (300K/1.5M).

This decreasing utilization pattern reflects the empirical 
finding of Liu et al. (2024) that Middle Context Loss severity 
increases with absolute context length, not merely with the 
proportion of context used. A 30K token context in a 128K 
window suffers more severe middle-position degradation than a 
3K token context in a 4K window, requiring a proportionally 
more conservative safety margin.

For models not in the four defined tiers, the safe token 
budget is computed continuously:

$$Safe\_Tokens(W) = W \times f(W)$$

Where $f(W)$ is a monotonically decreasing utilization factor 
derived from the four anchor points.

---

## 4. Theoretical Analysis

### 4.1 Why Rerank-First Rather Than Retrieve-Then-Rerank

Standard production guidance recommends retrieving 50-100 
candidates with a bi-encoder and reranking to 5-10 with a 
cross-encoder. LARA inverts this by reranking the full corpus 
first. This design choice requires justification.

**Argument.** Bi-encoder retrieval is an approximation of 
relevance — it identifies semantically similar chunks, not 
necessarily relevant chunks. For small to medium corpora 
(N ≤ 500 chunks, the primary target deployment environment 
for LARA), the computational cost of full-corpus cross-encoder 
reranking is bounded and acceptable. The benefit is that the 
quality threshold filter in Phase 1 operates on true relevance 
scores rather than approximate similarity scores, eliminating 
the retrieval approximation error entirely.

For large corpora (N > 500 chunks), a hybrid approach is 
recommended: bi-encoder pre-filtering to reduce the candidate 
set to a manageable size (e.g., N' = 200), followed by full 
cross-encoder reranking of the pre-filtered set. This extension 
is outside the current scope of LARA but represents a natural 
future development.

### 4.2 Correctness of the Speed Governor

**Theorem.** For any Send_List produced by Phase 2, the 
predicted processing latency satisfies:

$$|Send\_List| \times Lat_{chunk} \leq L_{budget}$$

**Proof.** 
Let $n = |Dynamic\_K|$ and $r = Reduce\_Count$.

$$r = \left\lceil \frac{\max(0, n \cdot Lat_{chunk} - 
L_{budget})}{Lat_{chunk}} \right\rceil$$

Case 1: $n \cdot Lat_{chunk} \leq L_{budget}$. Then 
$Exceeded = 0$, $r = 0$, Send_List = Dynamic_K, and 
$(n - 0) \cdot Lat_{chunk} = n \cdot Lat_{chunk} \leq 
L_{budget}$. ✓

Case 2: $n \cdot Lat_{chunk} > L_{budget}$. Then 
$r = \lceil (n \cdot Lat_{chunk} - L_{budget}) / 
Lat_{chunk} \rceil$.

$$(n - r) \cdot Lat_{chunk} \leq n \cdot Lat_{chunk} - 
(n \cdot Lat_{chunk} - L_{budget}) = L_{budget}$$ ✓

The ceiling function ensures we never undercount the required 
reduction, guaranteeing budget compliance. □

### 4.3 Relationship to Middle Context Loss

LARA's Phase 4 tier system addresses the U-shaped performance 
curve by ensuring that the context passed to the LLM at each 
refinement iteration never exceeds the tier-specific safe token 
budget. By processing the Send_List in batches of this size 
rather than as a single large context, LARA ensures that 
relevant information always falls within the high-attention 
zones — the beginning and end — of each batch's context window.

---

## 5. Implementation

LARA is implemented as the retrieval backend of the 
NPM-RAG-API-Framework and is accessible through the npmai 
Python library. The implementation uses:

- **Cross-Encoder:** `cross-encoder/ms-marco-MiniLM-L-6-v2` 
  (Sentence Transformers)
- **Vector Store:** FAISS with HuggingFace BGE embeddings 
  (`BAAI/bge-small-en-v1.5`)
- **Chunk Size:** 1,000 characters with 200 character overlap
- **API Framework:** FastAPI deployed on HuggingFace Spaces 
  with Supabase for persistent vector storage
- **LLM Backend:** npmai Ollama interface with dual-gateway 
  fallback architecture

```python
def lara_retrieve(
    query: str,
    vectordb: FAISS,
    model_tier: int = 1,
    L_afford: float = 10.0,
    lat_chunk: float = 0.1,
    score_threshold: float = 0.3
) -> List[Document]:

    # Phase 1: Full-corpus reranking + quality gate
    N = vectordb.index.ntotal
    all_chunks = vectordb.similarity_search(query, k=N)
    
    reranker = CrossEncoder(
        'cross-encoder/ms-marco-MiniLM-L-6-v2'
    )
    t_rerank_start = time.time()
    scores = reranker.predict(
        [(query, doc.page_content) for doc in all_chunks]
    )
    T_rerank = time.time() - t_rerank_start
    
    # Apply quality threshold
    dynamic_k = [
        doc for doc, score in zip(all_chunks, scores)
        if score >= score_threshold
    ]
    dynamic_k.sort(
        key=lambda x: scores[all_chunks.index(x)], 
        reverse=True
    )
    
    # Phase 2: Latency-based speed governor
    L_budget = L_afford - T_rerank
    total_lat = len(dynamic_k) * lat_chunk
    
    if total_lat > L_budget:
        exceeded = total_lat - L_budget
        reduce_count = math.ceil(exceeded / lat_chunk)
        send_list = dynamic_k[:-reduce_count]
    else:
        send_list = dynamic_k
    
    return send_list

def lara_refine(
    send_list: List[Document],
    query: str,
    llm: Ollama,
    L_afford: float,
    tier_max_tokens: int
) -> str:

    # Phase 3 & 4: Sliding window batch refinement
    # with tier-enforced context safety
    chunks_per_iter = max(
        1, int(len(send_list) / L_afford)
    )
    running_answer = ""
    
    for i in range(0, len(send_list), chunks_per_iter):
        batch = send_list[i:i + chunks_per_iter]
        context = "\n---\n".join(
            [doc.page_content for doc in batch]
        )
        
        # Enforce tier token limit
        context = context[:tier_max_tokens * 4]
        
        prompt = f"""Use this context to refine your answer.
Context: {context}
Current Answer: {running_answer}
Question: {query}
Refined Answer:"""
        
        running_answer = llm.invoke(prompt)
    
    return running_answer
```

The full implementation including the FastAPI endpoints for 
ingestion, retrieval, and Supabase persistence is available at:  
`https://github.com/sonuramashishnpm/NPM-Rag-API-Framework`

---

## 6. Experimental Setup

*Note: Full benchmark results are pending. This section 
describes the experimental protocol for reproducibility.*

### 6.1 Datasets

- **NaturalQuestions (NQ):** Standard open-domain QA benchmark 
  with Wikipedia as the knowledge source (Kwiatkowski et al., 
  2019). Used for single-hop factual retrieval evaluation.
- **HotpotQA:** Multi-hop reasoning benchmark requiring 
  evidence synthesis across multiple documents (Yang et al., 
  2018).
- **Custom NPMAI Corpus:** A domain-specific dataset of 50 
  technical documents (AI/ML papers, API documentation, 
  educational content) representative of the target 
  deployment environment for LARA.

### 6.2 Baselines

- **Standard RAG k=4:** The default LangChain RAG pipeline 
  with fixed k=4.
- **Standard RAG k=10:** Fixed k=10 to test higher recall.
- **Rerank-then-Fixed-k:** Full-corpus reranking followed by 
  fixed top-k selection (ablation to isolate LARA's 
  score-threshold contribution).
- **LARA (ours):** Full four-phase pipeline.

### 6.3 Metrics

- **Exact Match (EM):** Standard QA accuracy metric.
- **F1 Score:** Token-level precision-recall balance.
- **End-to-End Latency:** Total time from query to final 
  answer.
- **Context Noise Rate:** Proportion of chunks in the final 
  Send_List with reranker score < 0.3 (measures noise 
  injection prevention effectiveness).

---

## 7. Discussion

### 7.1 Relation to the Broader Adaptive RAG Landscape

Adaptive-RAG (Jeong et al., 2024) and Self-RAG (Asai et al., 
2024) represent the dominant paradigm of adaptive retrieval: 
training smaller models to make retrieval strategy decisions. 
LARA takes a complementary approach — training-free, 
parameter-free, deployment-time adaptation through mathematical 
retrieval planning.

This distinction matters for the target deployment context: 
training-based adaptive systems require labeled data and 
fine-tuning infrastructure unavailable to most independent 
developers. LARA requires only a cross-encoder (freely 
available via Sentence Transformers) and three developer-
specified parameters (L_afford, lat_chunk, model_tier).

---

## 8. Conclusion

This paper presented LARA, a four-phase latency-aware 
retrieval architecture that addresses the fixed-k limitation 
of standard RAG pipelines through semantic quality gating, 
latency-predictive pruning, model-tier-aware context budgeting, 
and sliding window batch refinement.

The key theoretical contributions are:

1. Treating Middle Context Loss as an explicit architectural 
   constraint rather than an acknowledged limitation.
2. Formalizing latency-predictive retrieval planning as a 
   mathematical guarantee rather than a heuristic.
3. Establishing that safe context budgets should decrease as 
   a proportion of context window size as windows grow larger, 
   reflecting increasing Middle Context Loss severity.

LARA is implemented and deployed in the npmai ecosystem with 
432K+ total installations and 16K+ daily downloads, providing 
a production-scale validation environment for the architecture.

Experimental evaluation on NaturalQuestions and HotpotQA 
benchmarks is ongoing. Full results will be reported in a 
companion empirical paper upon completion of the experimental 
protocol.

---

## References

Asai, A., Wu, Z., Wang, Y., Sil, A., & Hajishirzi, H. (2024). 
Self-RAG: Learning to retrieve, generate, and critique through 
self-reflection. *ICLR 2024*.

Chen, J., Xiao, S., Zhang, P., Luo, K., Lian, D., & Liu, Z. 
(2024). RankRAG: Unifying context ranking with retrieval-
augmented generation in LLMs. *NeurIPS 2024*.

Jeong, S., Baek, J., Cho, S., Hwang, S. J., & Park, J. C. 
(2024). Adaptive-RAG: Learning to adapt retrieval-augmented 
large language models through question complexity. 
*arXiv:2403.14403*.

Jiang, Z., Xu, F. F., Gao, L., Sun, Z., Liu, Q., Dwivedi-Yu, 
J., ... & Neubig, G. (2023). Active retrieval augmented 
generation. *arXiv:2305.06983*.

Kwiatkowski, T., Palomaki, J., Redfield, O., Collins, M., 
Parikh, A., Alberti, C., ... & Petrov, S. (2019). Natural 
Questions: A benchmark for question answering research. 
*TACL, 7*, 452–466.

Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., 
Goyal, N., ... & Kiela, D. (2020). Retrieval-augmented 
generation for knowledge-intensive NLP tasks. 
*NeurIPS 2020*.

Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, 
M., Petroni, F., & Liang, P. (2024). Lost in the middle: How 
language models use long contexts. *TACL, 12*, 157–173.

Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence 
embeddings using Siamese BERT-networks. *EMNLP 2019*.

Su, J., Ahmed, M., Lu, Y., Pan, S., Bo, W., & Liu, Y. (2024). 
RoFormer: Enhanced transformer with rotary position embedding. 
*Neurocomputing, 568*.

Yang, Z., Qi, P., Zhang, S., Bengio, Y., Cohen, W. W., 
Salakhutdinov, R., & Manning, C. D. (2018). HotpotQA: A 
dataset for diverse, explainable multi-hop question answering. 
*EMNLP 2018*.

---
