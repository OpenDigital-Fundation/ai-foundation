# Specs e ADRs organizados por domínio, sem numeral
- **Status:** substituído por [docs-layout-domain-first](../../foundation/adr/2026-11-21-docs-layout-domain-first.md)
- **Data:** 2026-11-06
- **Domínio:** foundation

## Contexto

Numerar specs (`001-...`) e ADRs (`0001-...`) cria conflito de número entre branches paralelas e mistura domínios numa sequência única.

## Decisão

Specs em `docs/specs/<domínio>/<feature>/{spec,plan,tasks}.md`; ADRs em `docs/adr/<domínio>/<slug>.md`, com status e data no cabeçalho. A ordem de execução vive em `docs/specs/ROADMAP.md`. ADR substituído recebe `Status: substituído por <caminho>`.

## Consequências

- Sem colisão entre branches.
- Ordem cronológica dos ADRs vem da data, não do nome.
