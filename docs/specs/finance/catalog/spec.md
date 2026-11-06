# Spec — Catálogo do domínio `finance`

- **Domínio:** finance
- **Status:** em implementação (Onda 3)
- **Fronteira:** contabilidade, FP&A, precificação, impostos, cobrança.

## Resultado (gerado por `tools.curation.bundle` a partir de [`bundles/business.yaml`](../../../../catalog/decisions/bundles/business.yaml))

| Artefato | Base | Referências |
|---|---|---|
| `financial-analysis` | `financial-analyst` | `fpa-analyst`, `pricing-analyst`, `investment-researcher` |
| `accounting` | `bookkeeper-controller` | `tax-strategist`, `accounts-payable-agent`, `finance-tracker` |
| `billing-operations` | `billing-ops` | `customer-billing-ops`, `engineering-payments-billing-engineer` |

## Notas

- Base em personas do agency-agents: o texto é persona, não procedimento verificável. Revisar cada skill e reescrever o corpo como passos com critério de saída antes de promover a `stable`.
