# Spec — Catálogo do domínio `debugging`

- **Domínio:** debugging
- **Status:** em implementação (Onda 1)
- **Fronteira:** achar a causa de falhas — diagnóstico, erros de build, falhas silenciosas.

## Resultado

| Artefato | Base | Fundidos |
|---|---|---|
| `systematic-debugging` | superpowers (quatro fases, lei de ferro, técnicas de apoio) | mattpocock `diagnosing-bugs`: a fase "construa um feedback loop" vira o passo 2 da Fase 1 com critério de conclusão (`references/feedback-loop.md`) e o script HITL |

## Próximos artefatos (ainda não implementados)

- `build-failure-resolution`: um agent genérico `build-resolver` que carrega o pacote da linguagem, substituindo os 13 `*-build-resolver` do ECC e os comandos `*-build`/`build-fix`.
- `silent-failure-hunting`: ECC `silent-failure-hunter`.
- `agent-introspection-debugging` (ECC) é decidido em `agent-engineering`.

## Critérios de aceite

1. Um único ponto de entrada para "algo está quebrado"; variantes por linguagem só como referência.

## Passada final (bundle [manifesto editorial](../../../../catalog/curation/domains/debugging.yaml))

Adicionados: `build-failure-resolution` (base agent `build-error-resolver`; `silent-failure-hunter`; absorve `build-fix`).
