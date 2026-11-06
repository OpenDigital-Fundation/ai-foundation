# Spec — Catálogo do domínio `architecture`

- **Domínio:** architecture
- **Status:** em implementação (Onda 1)
- **Fronteira:** desenho de sistema e de código — módulos, domínio, ADR, API, fronteiras.

## Resultado

| Artefato | Base | Fundidos |
|---|---|---|
| `domain-modeling` | mattpocock | — (escrita de ADR delegada a `decision-records`) |
| `decision-records` | ECC `architecture-decision-records` | mattpocock `ADR-FORMAT.md` (forma mínima e critério de três condições) |
| `codebase-design` | mattpocock (módulos profundos, design-it-twice) | ECC `hexagonal-architecture` como `references/ports-and-adapters.md` |
| `architecture-review` | mattpocock `improve-codebase-architecture` | — |
| `api-design` | ECC `api-design` | — (padrões de implementação movidos para `references/`; variantes por framework nos pacotes de linguagem) |

## Decisões de conteúdo

- Local dos ADRs: segue o layout do repositório; sem layout, `docs/adr/<domínio>/<slug>.md` sem numeral (coerente com o [ADR deste repositório](../../../adr/foundation/docs-layout-by-domain.md)); repositórios que já numeram continuam numerando.

## Próximos artefatos (ainda não implementados)

- `system-design`: personas *Software Architect*, *Backend Architect* (agency), agents `architect`, `code-architect` (ECC).
- `codebase-onboarding`: ECC `codebase-onboarding`, `code-tour`; agency *Codebase Onboarding Engineer*, *Codebase Archaeologist*; agent `code-explorer` (ECC).
- `contract-first` e `spec-miner` (ECC): avaliar contra `api-design` e `workflow:brainstorming`.
