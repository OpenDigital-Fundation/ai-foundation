# `web3`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

Blockchain and DeFi engineering - smart contracts, token/accounting units, mechanism invariants and local verification; no investment recommendations or live transactions.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install web3@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`defi-engineering`](skills/defi-engineering/SKILL.md) | experimental | Use when engineering or reviewing DeFi mechanism invariants, AMM/share accounting, token decimals, oracle assumptions, collateral/liquidation flows or protocol simulations. |
| [`smart-contract-development`](skills/smart-contract-development/SKILL.md) | experimental | Use when designing, implementing and testing blockchain smart contracts, token interfaces, upgrade/storage layouts or a deployment plan, excluding investment recommendations and live value transfers. |

## Origem e manutenção

- Entrada editorial: [manifesto de `web3`](../../catalog/curation/domains/web3.yaml).
- Requisitos: [spec do domínio](../../docs/specs/web3/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/web3/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `defi-engineering` | affaan-m/ECC |
| `smart-contract-development` | msitarzewski/agency-agents, wshobson/agents |
