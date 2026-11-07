# Plano — Classificação por facetas

- Vocabulários em `catalog/taxonomy/*.yaml` + `catalog/schema/taxonomy.schema.json`.
- Atribuição em `catalog/facets.yaml`: padrões por domínio (conhecimento e capacidades típicos) ajustados artefato a artefato; facetas de tecnologia pelo tipo e pelo assunto (RAG, MCP, harness, evals).
- Validação: nova checagem em `tools/validate/checks.py` (R4).
- Navegação: `tools/build/docs.py` gera `docs/FACETS.md` e acrescenta facetas aos READMEs de domínio; o CI já falha se os índices divergirem.
