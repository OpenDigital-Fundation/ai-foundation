# `healthcare`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

Health systems and clinician-reviewed support - interoperability, traceable evidence briefs and documentation of verified clinical facts and decisions.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install healthcare@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`clinical-documentation`](skills/clinical-documentation/SKILL.md) | experimental | Use when drafting or checking clinical notes, structured reports, handoffs or documentation of plans already supplied by a qualified clinician, with field-level traceability and professional review. |
| [`clinical-evidence`](skills/clinical-evidence/SKILL.md) | experimental | Use when a healthcare professional needs a source-backed clinical evidence brief, appraisal of a clinical claim or a documented evidence profile; not a patient-specific diagnosis or prescription. |
| [`health-informatics`](skills/health-informatics/SKILL.md) | experimental | Use when designing or reviewing EHR/EMR systems, health-data interoperability, clinician workflows or clinical decision-support software architecture and validation. |

## Origem e manutenção

- Entrada editorial: [manifesto de `healthcare`](../../catalog/curation/domains/healthcare.yaml).
- Requisitos: [spec do domínio](../../docs/specs/healthcare/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/healthcare/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `clinical-documentation` | K-Dense-AI/claude-scientific-skills |
| `clinical-evidence` | K-Dense-AI/claude-scientific-skills, msitarzewski/agency-agents |
| `health-informatics` | affaan-m/ECC |
