# `operations`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

Project management, people operations, customer support, processes.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install operations@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`customer-support`](skills/customer-support/SKILL.md) | experimental | Use for customer support and success work: answering tickets, writing help-center replies and macros, escalations, onboarding and health checks for accounts, and turning support trends into product feedback. |
| [`people-operations`](skills/people-operations/SKILL.md) | experimental | Use for people operations: hiring plans and job descriptions, interview loops, onboarding new staff, training programmes, and managing organisational change. |
| [`project-management`](skills/project-management/SKILL.md) | experimental | Use when running a project or programme: plans and milestones, status tracking, risks and dependencies, stakeholder updates, meeting notes and action items, and keeping a Jira or tracker workflow healthy. |

## Origem e manutenção

- Entrada editorial: [manifesto de `operations`](../../catalog/curation/domains/operations.yaml).
- Requisitos: [spec do domínio](../../docs/specs/operations/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/operations/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `customer-support` | msitarzewski/agency-agents |
| `people-operations` | msitarzewski/agency-agents |
| `project-management` | affaan-m/ECC, msitarzewski/agency-agents |
