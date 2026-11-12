# `geospatial`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

Geographic information - spatial analysis, coordinate systems, cartography, GIS data pipelines and spatial services.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install geospatial@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`geospatial-analysis`](skills/geospatial-analysis/SKILL.md) | experimental | Use when analysing geographic vector/raster data, selecting coordinate reference systems, making analytical maps, validating spatial accuracy or interpreting spatial statistics. |
| [`geospatial-engineering`](skills/geospatial-engineering/SKILL.md) | experimental | Use when building GIS data pipelines, spatial services, map applications, BIM/GIS integration, geoprocessing tools or scalable map delivery. |

## Origem e manutenção

- Entrada editorial: [manifesto de `geospatial`](../../catalog/curation/domains/geospatial.yaml).
- Requisitos: [spec do domínio](../../docs/specs/geospatial/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/geospatial/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `geospatial-analysis` | msitarzewski/agency-agents |
| `geospatial-engineering` | msitarzewski/agency-agents |
