---
name: rag-pipelines
description: "Use when building, debugging or reviewing retrieval-augmented generation or search: chunking, embeddings, hybrid and lexical search, reranking, query rewriting, iterative retrieval for agents, Elasticsearch/OpenSearch relevance tuning, and retrieval evaluation."
license: MIT
metadata:
  domain: ai-engineering
  status: experimental
---
# RAG pipelines

Retrieval quality decides answer quality: measure retrieval before tuning the prompt.

## 1. Build an evaluation set
Real questions with the documents or passages that answer them. Measure recall@k and precision of retrieval, then faithfulness and correctness of answers.

## 2. Ingest
Parse documents faithfully (tables, headings), chunk by structure rather than fixed size, keep metadata (source, section, date, permissions), and deduplicate.

## 3. Retrieve
Hybrid search (lexical plus embeddings) with metadata filters, then rerank. Rewrite or decompose the query when questions are multi-part; for agents, retrieve iteratively.

## 4. Generate
Pass only the top passages with their sources; instruct the model to answer from them and cite, and to say when the context does not contain the answer.

## 5. Iterate and monitor
Change one thing at a time against the evaluation set; log queries, retrieved chunks and feedback in production; enforce document permissions at retrieval time.

## References

Load only what the task needs:

- [`references/role-guide.md`](references/role-guide.md) — the role profile this skill was distilled from: mission, critical rules, deliverable templates and examples
- [`references/review.md`](references/review.md) — covers rag-pipeline-reviewer
- [`references/iterative-retrieval.md`](references/iterative-retrieval.md) — covers Iterative Retrieval Pattern
- [`references/search-relevance.md`](references/search-relevance.md) — covers Search Relevance Engineer
