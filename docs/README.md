# Documentação

| Objetivo | Documento |
|---|---|
| Encontrar capacidades | [Catálogo](CATALOG.md) ou [facetas](FACETS.md) |
| Entender e manter o repositório | [Contrato de diretórios e fluxo de manutenção](architecture/repository-layout.md) |
| Conferir a revisão estrutural | [Revisão de organização](reviews/repository-organization.md) |
| Conferir licenças e conteúdo upstream | [Fontes](SOURCES.md) e [avisos de terceiros](../THIRD_PARTY_NOTICES.md) |
| Entender requisitos e sequência de implementação | `docs/<domínio>/specs/ROADMAP.md` (ex.: [foundation](foundation/specs/ROADMAP.md)); specs legadas em [ROADMAP](specs/ROADMAP.md) |
| Entender uma decisão arquitetural | `docs/<domínio>/adr/` (ex.: [foundation](foundation/adr/)); ADRs legados em [adr/](adr/) |

`CATALOG.md`, `FACETS.md` e `SOURCES.md` são índices gerados. Specs e ADRs são documentos editoriais ([layout por domínio](foundation/adr/2026-11-21-docs-layout-domain-first.md); os caminhos antigos seguem válidos na transição): uma feature por spec, uma decisão por ADR. Evidências de uma revisão ficam em `reviews/`; dados operacionais ficam em `catalog/inventory/`.
