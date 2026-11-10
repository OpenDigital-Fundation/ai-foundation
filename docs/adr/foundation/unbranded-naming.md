# Nomes sem marca e sem superlativo
- **Status:** proposto
- **Data:** 2026-11-06
- **Domínio:** foundation

## Contexto

Nomes como `ui-ux-pro-max`, `superpowers:brainstorming`, `ponytail-review` ou `ecc-guide` carregam a marca da fonte e, às vezes, misturam domínios. Isso dificulta entender o que o artefato faz e prende o catálogo a uma origem.

## Decisão

Nomes em kebab-case, em inglês, descrevendo a capacidade; únicos no repositório; sem marca, autor ou superlativo (lista em `catalog/naming.yaml`). A origem é registrada em `PROVENANCE.yaml` e `THIRD_PARTY_NOTICES.md`.

## Consequências

- Quem vem das fontes precisa de um mapa de nomes antigos para novos: gerado de `supersedes`.
- O crédito às fontes é mantido na proveniência, não no nome.
