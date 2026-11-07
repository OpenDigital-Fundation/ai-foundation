# `architecture`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

System and code design - modules, domain models, ADRs, APIs, boundaries.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install architecture@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`api-design`](skills/api-design/SKILL.md) | experimental | Use when designing or reviewing an HTTP/REST API: resource naming, methods and status codes, response and error formats, pagination, filtering and sorting, authentication, rate limiting and versioning. Produces consiste… |
| [`architecture-review`](skills/architecture-review/SKILL.md) | experimental | Use when the user asks to improve or review the architecture of an existing codebase. Scans recent hot spots for shallow modules and leaky seams, presents ranked deepening opportunities as a visual HTML report, then gri… |
| [`codebase-design`](skills/codebase-design/SKILL.md) | experimental | Use when designing or restructuring a module's interface: deciding where a seam goes, making code testable or easier for agents to navigate, applying ports and adapters, or finding deepening opportunities. Provides the… |
| [`codebase-onboarding`](skills/codebase-onboarding/SKILL.md) | experimental | Use when someone (or an agent) needs to understand an unfamiliar codebase fast: map its structure and entry points, trace a feature end to end, write a guided code tour, recover the intent behind legacy code, or mine an… |
| [`decision-records`](skills/decision-records/SKILL.md) | experimental | Use when a significant technical decision is made or needs recording (architecture shape, a technology with lock-in, a boundary, a deliberate deviation from the obvious path, a rejected alternative someone will propose… |
| [`domain-modeling`](skills/domain-modeling/SKILL.md) | experimental | Use when the project's domain language is being changed, not just read: a term is fuzzy, overloaded or conflicts with GLOSSARY.md, or the user and the code disagree about how a concept works. Challenges terms with concr… |
| [`system-design`](skills/system-design/SKILL.md) | experimental | Use when designing a service, system or major feature end to end: components and boundaries, data flow, APIs and contracts, consistency and failure handling, scalability and latency budgets, caching, real-time collabora… |

## Origem e manutenção

- Entrada editorial: [manifesto de `architecture`](../../catalog/curation/domains/architecture.yaml).
- Requisitos: [spec do domínio](../../docs/specs/architecture/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/architecture/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `api-design` | affaan-m/ECC |
| `architecture-review` | affaan-m/ECC, mattpocock/skills |
| `codebase-design` | affaan-m/ECC, mattpocock/skills |
| `codebase-onboarding` | affaan-m/ECC, msitarzewski/agency-agents |
| `decision-records` | affaan-m/ECC, mattpocock/skills |
| `domain-modeling` | mattpocock/skills |
| `system-design` | affaan-m/ECC, msitarzewski/agency-agents |
