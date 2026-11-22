# Specs e ADRs em `docs/<domínio>/`, com data no nome do ADR
- **Status:** proposto
- **Data:** 2026-11-21
- **Domínio:** foundation
- **Substitui:** [docs-layout-by-domain](../../adr/foundation/docs-layout-by-domain.md)

## Contexto

O layout anterior agrupa por tipo de documento (`docs/specs/<domínio>/`, `docs/adr/<domínio>/`) e separa o que pertence a um domínio em duas árvores. Documentos que atravessam domínios não têm lugar.

## Decisão

- Specs: `docs/<domínio>/specs/<feature>/{spec,plan,tasks}.md`, com `docs/<domínio>/specs/ROADMAP.md`.
- ADRs: `docs/<domínio>/adr/AAAA-MM-DD-<decisão>.md`. A data no nome mantém a ordem cronológica sem numeral.
- Transversal: `docs/transversal/{specs,adr}/`.
- Sem número sequencial. ADR substituído recebe `Status: substituído por <caminho>`.
- Documentos existentes não são movidos nem renomeados. Na transição, o validador aceita os dois caminhos. A migração em lote é a issue [#12](https://github.com/OpenDigital-Fundation/ai-foundation/issues/12).

## Consequências

- Tudo de um domínio fica sob `docs/<domínio>/`.
- Sem colisão de número entre branches.
- Durante a transição existem duas árvores; o validador recusa a mesma feature nas duas.
- `docs/architecture/` serve ao contrato do repositório e ao domínio `architecture`.
