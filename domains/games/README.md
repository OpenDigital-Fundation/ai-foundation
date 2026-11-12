# `games`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

Game design and engineering - mechanics, progression, economies, levels, engine integration, runtime performance and multiplayer.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install games@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`game-design`](skills/game-design/SKILL.md) | experimental | Use when designing game mechanics, player loops, progression, economies, narrative systems or levels and planning playtests. Use game-engineering for engine implementation. |
| [`game-engineering`](skills/game-engineering/SKILL.md) | experimental | Use when implementing and profiling a game runtime: scenes, entity state, save systems, engine integration, game audio, networking or a packaged game build. |

## Origem e manutenção

- Entrada editorial: [manifesto de `games`](../../catalog/curation/domains/games.yaml).
- Requisitos: [spec do domínio](../../docs/specs/games/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/games/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `game-design` | msitarzewski/agency-agents |
| `game-engineering` | msitarzewski/agency-agents |
