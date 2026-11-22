# Spec — Layout de specs e ADRs por domínio

- **Domínio:** foundation
- **Status:** implementada e verificada localmente
- **Issue:** [#11](https://github.com/OpenDigital-Fundation/ai-foundation/issues/11)
- **ADRs:** [docs-layout-domain-first](../../adr/2026-11-21-docs-layout-domain-first.md)

## Problema

Specs ficam em `docs/specs/<domínio>/<feature>/` e ADRs em `docs/adr/<domínio>/<decisão>.md`. Os dois agrupam por tipo de documento antes do domínio, então tudo que pertence a um domínio fica espalhado em duas árvores. Também não há lugar para documentos que atravessam domínios, e nenhum validador confere o formato.

## Requisitos

- R1. Specs ficam em `docs/<domínio>/specs/<feature>/` com `spec.md`, `plan.md` e `tasks.md`; a ordem das specs do domínio fica em `docs/<domínio>/specs/ROADMAP.md`.
- R2. ADRs ficam em `docs/<domínio>/adr/AAAA-MM-DD-<decisão>.md`; a data do nome é uma data de calendário válida e repete a do cabeçalho.
- R3. Documentos transversais ficam em `docs/transversal/{specs,adr}/`.
- R4. Sem número sequencial em nomes de feature ou de ADR.
- R5. `<domínio>` é um domínio de `catalog/domains.yaml`, `foundation` ou `transversal`.
- R6. Durante a transição, os caminhos antigos (`docs/specs/<domínio>/<feature>/`, `docs/adr/<domínio>/<decisão>.md`) continuam válidos e nada existente é movido nem renomeado.
- R7. A mesma feature não existe nos dois layouts ao mesmo tempo.
- R8. O validador (`tools.validate`) aplica R1 a R7 aos documentos do layout novo e tem testes de regressão.
- R9. `AGENTS.md`, o guia de layout, o índice de `docs/` e os padrões das skills de spec, plano, ADR e revisão apontam para o layout novo e citam o antigo como legado.
- R10. A migração em lote é uma issue separada ([#12](https://github.com/OpenDigital-Fundation/ai-foundation/issues/12)).

## Critérios de aceite

1. Spec e ADR no layout novo e no antigo passam em `uv run python -m tools.validate`.
2. Falham: nome numerado, domínio desconhecido, feature sem `plan.md` ou `tasks.md` no layout novo, ADR sem data no nome e a mesma feature nos dois layouts.
3. `uv run pytest -q` passa, incluindo o teste de links locais sobre os dois layouts.
4. Nenhuma projeção gerada é editada à mão.

## Fora de escopo

Mover ou renomear specs e ADRs existentes; remover o suporte ao caminho antigo; aprovação humana do ADR.
