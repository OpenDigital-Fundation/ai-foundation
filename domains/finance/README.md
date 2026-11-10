# `finance`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

Bookkeeping, FP&A, pricing, tax.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install finance@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`accounting`](skills/accounting/SKILL.md) | experimental | Use for day-to-day accounting: bookkeeping, reconciliations, month-end close, accounts payable, expense tracking, financial statements, and tax planning questions to prepare for an accountant. |
| [`billing-operations`](skills/billing-operations/SKILL.md) | experimental | Use when building or operating billing: subscriptions, invoicing, payment providers, refunds and disputes, dunning, revenue reporting and customer billing issues. |
| [`financial-analysis`](skills/financial-analysis/SKILL.md) | experimental | Use for financial modelling and planning: three-statement and unit-economics models, forecasts and budgets, scenario analysis, variance analysis, pricing models and investment memos. |

## Origem e manutenção

- Entrada editorial: [manifesto de `finance`](../../catalog/curation/domains/finance.yaml).
- Requisitos: [spec do domínio](../../docs/specs/finance/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/finance/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `accounting` | msitarzewski/agency-agents |
| `billing-operations` | affaan-m/ECC, msitarzewski/agency-agents |
| `financial-analysis` | msitarzewski/agency-agents, wshobson/agents |
