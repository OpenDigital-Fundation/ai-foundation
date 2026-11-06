# Spec — Catálogo do domínio `testing`

- **Domínio:** testing
- **Status:** em implementação (Onda 1)
- **Fronteira:** provar comportamento — TDD, estratégia de testes, E2E/navegador, verificação antes de concluir.

## Resultado

| Artefato | Base | Fundidos |
|---|---|---|
| `test-driven-development` | superpowers | mattpocock `tdd` (seams combinadas, fatias verticais, anti-padrão tautológico, `tests.md`, `mocking.md`), ECC `tdd-workflow`, `tdd-guide` |
| `verification-before-completion` | superpowers | ECC `verification-loop`, agency *Reality Checker*, *Evidence Collector* |

Decisões em [`catalog/decisions/engineering-core.yaml`](../../../../catalog/decisions/engineering-core.yaml).

## Próximos artefatos (ainda não implementados)

- [feito] `browser-testing`: base `anthropics/skills:webapp-testing` (Apache-2.0) + ECC `e2e-testing`, `browser-qa`, agent `e2e-runner`, `windows-desktop-e2e`. Falta `click-path-audit`.
- `test-strategy`: ECC `test-collaboration`, `ai-regression-testing`; agency *Test Automation Engineer*, *API Tester*, *Performance Benchmarker*.
- Variantes por linguagem (`*-testing`, `*-tdd`) vão para `languages/<x>/references/testing.md`.

## Critérios de aceite

1. Nenhuma skill de `testing` com similaridade ≥ 0,60 com outra do catálogo.
2. Evals de gatilho distinguem TDD (implementar) de debugging (falha existente) e de verificação (antes de declarar pronto).
