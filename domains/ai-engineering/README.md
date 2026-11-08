# `ai-engineering`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

Building products with LLMs - model APIs, MCP servers, RAG, prompts, product evals, cost.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install ai-engineering@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`claude-api`](skills/claude-api/SKILL.md) | experimental | Use when building with the Claude API or Anthropic SDKs: choosing a model, messages and streaming, tool use, MCP, agents, prompt caching, batch, token counting, error handling, or migrating between model versions. Read… |
| [`mcp-server-development`](skills/mcp-server-development/SKILL.md) | experimental | Use when designing, building, testing or evaluating a Model Context Protocol server: choosing tools, resources and prompts, writing tool schemas and descriptions, transports, auth, error handling, the TypeScript or Pyth… |
| [`ml-engineering`](skills/ml-engineering/SKILL.md) | experimental | Use when adding or operating machine learning in a product: data contracts, features, reproducible training, evaluation and model QA, serving, monitoring and drift, recommendation and ranking pipelines, and LLM post-tra… |
| [`prompt-engineering`](skills/prompt-engineering/SKILL.md) | experimental | Use when writing, testing or optimising prompts for an LLM feature: system prompts, few-shot examples, structured output, prompt evaluation sets, prompt caching for cost and latency, and deciding whether a regex or pars… |
| [`rag-pipelines`](skills/rag-pipelines/SKILL.md) | experimental | Use when building, debugging or reviewing retrieval-augmented generation or search: chunking, embeddings, hybrid and lexical search, reranking, query rewriting, iterative retrieval for agents, Elasticsearch/OpenSearch r… |

## Origem e manutenção

- Entrada editorial: [manifesto de `ai-engineering`](../../catalog/curation/domains/ai-engineering.yaml).
- Requisitos: [spec do domínio](../../docs/specs/ai-engineering/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/ai-engineering/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `claude-api` | anthropics/skills |
| `mcp-server-development` | affaan-m/ECC, anthropics/skills, msitarzewski/agency-agents |
| `ml-engineering` | affaan-m/ECC, msitarzewski/agency-agents |
| `prompt-engineering` | affaan-m/ECC, getsentry/skills, msitarzewski/agency-agents |
| `rag-pipelines` | affaan-m/ECC, msitarzewski/agency-agents |
