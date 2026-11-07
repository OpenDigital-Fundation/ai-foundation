# `principles`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

Always-on coding behaviour for agents - simplicity, surgical changes, explicit assumptions, verifiable success criteria.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install principles@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`coding-discipline`](skills/coding-discipline/SKILL.md) | experimental | Use on any task that writes, fixes or refactors code. Makes the smallest change that fully solves the task, surfaces assumptions before coding, keeps diffs surgical, and defines a verifiable success check. Also use when… |

## Origem e manutenção

- Entrada editorial: [manifesto de `principles`](../../catalog/curation/domains/principles.yaml).
- Requisitos: [spec do domínio](../../docs/specs/principles/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/principles/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `coding-discipline` | DietrichGebert/ponytail, affaan-m/ECC, msitarzewski/agency-agents, multica-ai/andrej-karpathy-skills |
