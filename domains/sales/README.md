# `sales`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

Prospecting, qualification, proposals, pipeline.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install sales@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`deal-strategy`](skills/deal-strategy/SKILL.md) | experimental | Use when working an active sales opportunity: discovery calls, qualification, mapping stakeholders, technical sales and demos, proposals, handling objections, pipeline reviews and forecasting, and coaching reps. |
| [`investor-relations`](skills/investor-relations/SKILL.md) | experimental | Use when raising money: pitch decks, one-pagers, financial narratives, data rooms, and investor outreach and follow-up. |
| [`prospecting`](skills/prospecting/SKILL.md) | experimental | Use when finding and reaching new customers: defining the ideal customer profile, building and scoring lead lists, finding warm paths, and writing personalised outbound sequences. |

## Origem e manutenção

- Entrada editorial: [manifesto de `sales`](../../catalog/curation/domains/sales.yaml).
- Requisitos: [spec do domínio](../../docs/specs/sales/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/sales/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `deal-strategy` | msitarzewski/agency-agents |
| `investor-relations` | affaan-m/ECC |
| `prospecting` | affaan-m/ECC, msitarzewski/agency-agents |
