# `extended-reality`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

Immersive AR/VR/XR applications - reference spaces, tracked input, spatial interaction, comfort and device/runtime verification.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install extended-reality@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`immersive-development`](skills/immersive-development/SKILL.md) | experimental | Use when designing or implementing AR, VR or XR applications: spatial reference frames, tracked input, immersive interaction, comfort, rendering budgets and runtime fallbacks. |

## Origem e manutenção

- Entrada editorial: [manifesto de `extended-reality`](../../catalog/curation/domains/extended-reality.yaml).
- Requisitos: [spec do domínio](../../docs/specs/extended-reality/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/extended-reality/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `immersive-development` | davila7/claude-code-templates |
