# RAG pipelines — derived guides

Part of `ai-engineering:rag-pipelines`.

## llm-architect

<!-- source: davila7/claude-code-templates cli-tool/components/agents/ai-specialists/llm-architect.md#serving-infrastructure-selection,rag-pipeline-architecture -->

### Serving Infrastructure Selection

#### Choose Your Serving Framework

- **vLLM**: Default choice for open-weight models requiring high throughput. PagedAttention handles variable-length KV cache automatically. Use chunked prefill (`--enable-chunked-prefill`) for long-context workloads above 16K tokens — chunked prefill and prefix caching are standard features in recent releases. Supports tensor parallelism across multiple GPUs with `--tensor-parallel-size`.
- **SGLang**: Prefer for chatbot/RAG/agent workloads with shared or repeated context — RadixAttention automatically caches shared prefixes across requests, typically outperforming vLLM on these workload shapes.
- **TGI (Text Generation Inference)**: Hugging Face's repo moved to maintenance mode in late 2025 and was archived in March 2026 — HF's own migration guidance now points TGI Inference Endpoints users to vLLM. Only choose TGI for maintaining an existing deployment; for new production stacks, prefer vLLM or SGLang.
- **Triton Inference Server**: Use when integrating with existing NVIDIA Triton pipelines, ensemble models, or when the serving layer must unify LLMs with vision/audio models.
- **TensorRT-LLM**: Prefer for maximum throughput/latency on NVIDIA-only infrastructure when the target model architecture has a supported TensorRT-LLM build — typically the fastest option on H100s but with a narrower model-support surface and heavier build/compile step than vLLM.
- **Ollama**: Development and single-user deployments only. Not suitable for multi-user production traffic.

#### Quantization Decision Tree

Apply in order — stop at the first condition that matches:

1. Latency-critical (P95 time-to-first-token < 150ms, or P95 end-to-end < 150ms for short structured outputs like classification/extraction) AND GPU memory constrained → **AWQ 4-bit** (best quality/speed at 4-bit, use `autoawq` library)
2. Batch workloads with moderate quality tolerance → **GPTQ 4-bit** (`auto-gptq`, calibration dataset required)
3. CPU fallback required or edge deployment → **llama.cpp GGUF q4_K_M** (good balance of speed and perplexity on CPU)
4. Quality-critical with sufficient GPU memory budget → **BitsAndBytes NF4 + double quantization** (`load_in_4bit=True, bnb_4bit_use_double_quant=True`)
5. No memory constraint → FP16 or BF16 (BF16 preferred on Ampere+ GPUs)

For longer generations (>200 output tokens) under a strict end-to-end P95 target, treat time-to-first-token and per-token decode latency separately — quantizing further rarely closes a gap driven by output length. Prioritize speculative decoding (see KV Cache and Batching below) or a hard output-length cap over more aggressive quantization in this case, and still apply the memory-constrained branch above for the model's footprint.

#### KV Cache and Batching

- Enable continuous batching in vLLM by default — it is on unless explicitly disabled.
- For speculative decoding: use a draft model 3–5x smaller than the target model. Gains are most pronounced on long outputs (>200 tokens) with low diversity.
- Prefix caching (`--enable-prefix-caching` in recent vLLM releases): high value for system-prompt-heavy workloads where the same prefix repeats across requests.

### RAG Pipeline Architecture

#### Vector Store Selection

| Corpus Size | Update Frequency | Recommendation |
|---|---|---|
| < 1M documents | Low (weekly+) | pgvector on existing Postgres — no new infrastructure |
| < 10M documents | Medium (daily) | Qdrant (self-hosted) or Weaviate |
| > 10M documents | High (real-time) | Pinecone or Weaviate with replication |
| Hybrid keyword + vector required at any scale | Any | Elasticsearch with dense_vector field + BM25 |

#### Chunking Strategy

- **Fixed-size with overlap**: Default starting point. Chunk size 512 tokens, overlap 50 tokens.
- **Semantic chunking**: Use when document structure is inconsistent. Split on embedding similarity drops (threshold 0.85).
- **Hierarchical chunking**: For long documents with section structure — index summaries at top level, full chunks at leaf level. Retrieves summary first, then fetches child chunks on match.

#### Retrieval and Reranking

- **Hybrid search**: Combine dense (cosine similarity) + sparse (BM25) with Reciprocal Rank Fusion (RRF). Default alpha = 0.5; tune on your evaluation set.
- **Reranking**: Apply a cross-encoder reranker (open-weight default: `BAAI/bge-reranker-v2-m3`; hosted: Cohere Rerank 4 or Voyage Rerank 2.5) on top-20 candidates to produce final top-5. Budget ~30–50ms for a self-hosted open-weight reranker; hosted/managed rerankers add network and provider latency on top of the model call itself — budget ~80–150ms depending on region and provider, and measure against your own traffic before committing to a latency-sensitive SLO.
- **Query expansion**: For low-recall scenarios, use HyDE (Hypothetical Document Embeddings) — generate a hypothetical answer, embed it, retrieve against that embedding.

#### Contextual Retrieval (optional upgrade)

When retrieval quality on standard hybrid search plateaus, upgrade to Anthropic's Contextual Retrieval technique: prepend a short LLM-generated context (chunk-specific summary situating the chunk within the full document) to each chunk before embedding it (contextual embeddings) and before indexing it for BM25 (contextual BM25), then apply reranking on top. Anthropic's published benchmark shows this reduces failed retrievals by 49% (67% when combined with reranking) relative to plain hybrid search. See anthropic.com/engineering/contextual-retrieval. Consider "late chunking" (embedding the full document first, then pooling token-level embeddings into chunks) as an alternative to context-prepending when chunk-level context loss is the primary failure mode.

#### Embedding Model Selection

- **Default**: `text-embedding-3-large` (OpenAI) for quality, `text-embedding-3-small` for cost-sensitive workloads.
- **Managed alternative**: Voyage AI embedding models — used in Anthropic's own contextual retrieval reference implementation, worth evaluating alongside OpenAI on your eval set.
- **Open-weight**: `BAAI/bge-large-en-v1.5` or `intfloat/e5-mistral-7b-instruct` for self-hosted.
- Never mix embedding models between index time and query time.

#### When Standard RAG Isn't Enough

For multi-hop or relationship-heavy queries where chunk-level retrieval consistently under-performs, escalate to GraphRAG-style entity-graph retrieval or agentic (LLM-driven) retrieval planning rather than tuning chunking/reranking further. Treat this as an escalation path, not a default — only introduce the added complexity once standard hybrid retrieval + reranking has been evaluated and found insufficient.

## Qdrant - Vector Similarity Search Engine

<!-- source: davila7/claude-code-templates cli-tool/components/skills/ai-research/rag-qdrant/SKILL.md#rag-integration -->

### RAG integration

#### With sentence-transformers

```python
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

# Initialize
encoder = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient(host="localhost", port=6333)

# Create collection
client.create_collection(
    collection_name="knowledge_base",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

# Index documents
documents = [
    {"id": 1, "text": "Python is a programming language", "source": "wiki"},
    {"id": 2, "text": "Machine learning uses algorithms", "source": "textbook"},
]

points = [
    PointStruct(
        id=doc["id"],
        vector=encoder.encode(doc["text"]).tolist(),
        payload={"text": doc["text"], "source": doc["source"]}
    )
    for doc in documents
]
client.upsert(collection_name="knowledge_base", points=points)

# RAG retrieval
def retrieve(query: str, top_k: int = 5) -> list[dict]:
    query_vector = encoder.encode(query).tolist()
    results = client.search(
        collection_name="knowledge_base",
        query_vector=query_vector,
        limit=top_k
    )
    return [{"text": r.payload["text"], "score": r.score} for r in results]

# Use in RAG pipeline
context = retrieve("What is Python?")
prompt = f"Context: {context}\n\nQuestion: What is Python?"
```

#### With LangChain

```python
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Qdrant.from_documents(documents, embeddings, url="http://localhost:6333", collection_name="docs")
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
```

#### With LlamaIndex

```python
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex, StorageContext

vector_store = QdrantVectorStore(client=client, collection_name="llama_docs")
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
query_engine = index.as_query_engine()
```

## search-specialist

<!-- source: davila7/claude-code-templates cli-tool/components/agents/ai-specialists/search-specialist.md#search-strategies -->

### Search Strategies

#### Query Optimization

- Use specific phrases in quotes for exact matches
- Exclude irrelevant terms with negative keywords
- Target specific timeframes for recent or historical data with `after:` / `before:` operators
- Formulate multiple query variations covering different phrasings and synonyms
- Use `site:` to target authoritative domains (official docs, academic, vendor advisories)

#### Domain Filtering

- `allowed_domains` for trusted sources (official docs, peer-reviewed journals, vendor advisories)
- `blocked_domains` to exclude content farms, aggregators, and low-signal sites
- Target academic sources (`site:arxiv.org`, `site:scholar.google.com`) for research topics
- Target primary sources for CVEs (`nvd.nist.gov`, vendor security advisories)
- Use either `allowed_domains` or `blocked_domains` per search call, never both — combine by running separate queries if you need both an allow-list and a block-list strategy

#### WebFetch Deep Dive

- Write a specific, verbatim-extraction prompt per WebFetch call (e.g., "Quote the exact pricing table rows and version numbers verbatim; do not summarize or paraphrase numeric values") rather than a generic "extract the content" request
- WebFetch only returns raw page text unmodified when the source is already Markdown and under ~100K characters — otherwise the content is routed through a smaller model that summarizes/paraphrases it based on your prompt, so numeric or exact-wording claims (prices, version ranges, CVE ranges) can be silently altered unless you explicitly ask for verbatim quotes
- Follow citation trails and reference sections for academic or technical claims
- Capture ephemeral data (pricing pages, job postings) before it changes
