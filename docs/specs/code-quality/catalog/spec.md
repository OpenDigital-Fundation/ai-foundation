# Spec — Catálogo do domínio `code-quality`

- **Domínio:** code-quality
- **Status:** em implementação (Onda 1)
- **Fronteira:** avaliar e melhorar código existente — review (dar e receber), simplificação, refatoração, dívida, auditoria.

## Resultado

| Artefato | Tipo | Base | Fundidos |
|---|---|---|---|
| `code-review` | skill | superpowers `requesting-code-review` | mattpocock `code-review` (dois eixos, baseline de smells), ponytail `ponytail-review` (formato de achados), ECC `code-review`/`review-pr` |
| `code-reviewer` | agent | superpowers `code-reviewer.md` | ponytail (prioridades e "caso concreto"), ECC `code-reviewer`, agency *Code Reviewer*; substitui os ~20 revisores por linguagem do ECC, que carregam `languages/<x>/references/review.md` |
| `receiving-code-review` | skill | superpowers | — |
| `codebase-audit` | skill | `revisor-de-codigo` (contribuição OpenDigital de Matheus Breguêz e Danilo Ribeiro, traduzida e generalizada): orquestrador, mapeador, 9 especialistas e verificador cético | ponytail `ponytail-audit` como modo rápido (`references/quick-audit.md`) |
| `debt-ledger` | skill | ponytail `ponytail-debt` | — |

## Próximos artefatos (ainda não implementados)

- `simplification`/refatoração: ECC `code-simplifier`, `refactor-cleaner`, `plankton-code-quality`; agency *Rust Refactoring Specialist* (vai para `languages:rust`).
- Decidir ECC `production-audit`, `repo-scan`, `change-impact`, `comment-analyzer`, `type-design-analyzer`, `pr-test-analyzer`, `commit-reviewer`.

## Critérios de aceite

1. Um único revisor (agent) no catálogo inteiro; revisores por linguagem não existem.
2. Formato de achado único: Must/Should/Nice, cada um com caso concreto, e veredito.

## Passada final (bundle [`gaps.yaml`](../../../../catalog/decisions/bundles/gaps.yaml))

Adicionados: `simplification` (base agent `code-simplifier`; `refactor-cleaner`, `comment-analyzer`, `type-design-analyzer`; absorve `refactor-clean`).
