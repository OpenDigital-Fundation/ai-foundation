# `research`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

Source-backed research with citations, literature reviews.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install research@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`docs-lookup`](skills/docs-lookup/SKILL.md) | experimental | Use when the user asks how to use a library, framework, SDK or API, or before writing code against one whose current behaviour matters. Fetches up-to-date documentation (for example through a Context7 MCP server) instea… |
| [`literature-review`](skills/literature-review/SKILL.md) | experimental | Use for a systematic literature review or for evaluating scholarly work: search planning across academic databases, screening criteria, extraction, synthesis, citation checks, and structured critique of papers, proposal… |
| [`source-research`](skills/source-research/SKILL.md) | experimental | Use when a question needs current or verifiable facts from outside the codebase: research a topic, compare options, check what a library or service does today, or produce a cited report. Plans sub-questions, prefers pri… |

## Origem e manutenção

- Entrada editorial: [manifesto de `research`](../../catalog/curation/domains/research.yaml).
- Requisitos: [spec do domínio](../../docs/specs/research/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/research/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `docs-lookup` | affaan-m/ECC, github/awesome-copilot |
| `literature-review` | affaan-m/ECC, msitarzewski/agency-agents |
| `source-research` | VoltAgent/awesome-claude-code-subagents, affaan-m/ECC, davila7/claude-code-templates, github/awesome-copilot, mattpocock/skills, msitarzewski/agency-agents |
