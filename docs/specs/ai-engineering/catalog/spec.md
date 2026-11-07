# Spec — Catálogo do domínio `ai-engineering`

- **Domínio:** ai-engineering
- **Status:** em implementação (Onda 2)
- **Fronteira:** construir produtos com LLM — APIs de modelo, MCP servers, RAG, prompts, evals de produto, custo.

## Resultado (gerado por `tools.curation.bundle` a partir de [manifesto editorial](../../../../catalog/curation/domains/ai-engineering.yaml))

| Artefato | Base | Referências |
|---|---|---|
| `claude-api` | anthropics/skills `claude-api` | — |
| `mcp-server-development` | anthropics/skills `mcp-builder` | `mcp-server-patterns`, `specialized-mcp-builder` |
| `rag-pipelines` | `engineering-rag-pipeline-engineer` | `rag-pipeline-reviewer`, `iterative-retrieval`, `engineering-search-relevance-engineer` |
| `prompt-engineering` | `engineering-prompt-engineer` | `prompt-caching-strategy`, `regex-vs-llm-structured-text` |
| `ml-engineering` | `mle-workflow` | `mle-reviewer`, `ml-adoption-playbook`, `specialized-model-qa`, `engineering-ai-engineer`, `recsys-pipeline-architect`, `engineering-llm-post-training-engineer` |

- `claude-api` mantém o `SKILL.md` oficial com 616 linhas (`line_budget_exception`: os links relativos para as referências por linguagem quebrariam se dividido) e é o único nome com exceção em `naming.yaml` (Claude é o assunto, não a fonte).

## Pendências

- Agency *Voice AI Integration Engineer*, *Knowledge Graph Engineer*, *Tool Evaluator*; ECC `ai-regression-testing`, `cost-aware-llm-pipeline`, `token-budget-advisor`: decidir.
