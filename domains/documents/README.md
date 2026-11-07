# `documents`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

Office documents and technical or corporate writing.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install documents@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`doc-coauthoring`](skills/doc-coauthoring/SKILL.md) | experimental | Use when the user wants to write a document together with you - a proposal, technical spec, decision doc, RFC or similar - through a structured workflow: gather context, refine section by section, then test the draft ag… |
| [`internal-comms`](skills/internal-comms/SKILL.md) | experimental | Use when writing internal communications: status reports, leadership updates, incident notices, company newsletters, FAQs and project updates, in the formats and tone a company expects. |
| [`office-documents`](skills/office-documents/SKILL.md) | experimental | Use when a task reads or produces Word, Excel, PowerPoint or PDF files (.docx, .xlsx, .pptx, .pdf): creating, editing, converting, extracting tables or text, filling forms or merging. Routes to the official document ski… |
| [`technical-writing`](skills/technical-writing/SKILL.md) | experimental | Use when writing or updating developer documentation: READMEs, API references, guides, tutorials, runbooks, architecture overviews or code maps, and keeping docs in sync after code changes. |

## Origem e manutenção

- Entrada editorial: [manifesto de `documents`](../../catalog/curation/domains/documents.yaml).
- Requisitos: [spec do domínio](../../docs/specs/documents/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/documents/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `doc-coauthoring` | anthropics/skills, msitarzewski/agency-agents |
| `internal-comms` | anthropics/skills, msitarzewski/agency-agents |
| `office-documents` | anthropics/skills, msitarzewski/agency-agents |
| `technical-writing` | affaan-m/ECC, msitarzewski/agency-agents |
