# `logistics`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

Physical supply chains - replenishment, suppliers, transport/carriers, shipment exceptions and reverse logistics.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install logistics@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`logistics-operations`](skills/logistics-operations/SKILL.md) | experimental | Use when organizing physical transport and carrier operations, shipment exceptions, delivery evidence, returns/reverse logistics, disposition or operational handoffs. |
| [`supply-chain-planning`](skills/supply-chain-planning/SKILL.md) | experimental | Use when planning physical supply chains: demand/capacity, inventory policy, suppliers, lead-time risk, sourcing alternatives and scenario-based total cost. |

## Origem e manutenção

- Entrada editorial: [manifesto de `logistics`](../../catalog/curation/domains/logistics.yaml).
- Requisitos: [spec do domínio](../../docs/specs/logistics/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/logistics/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `logistics-operations` | affaan-m/ECC |
| `supply-chain-planning` | msitarzewski/agency-agents |
