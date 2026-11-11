# `data`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

Databases, migrations, data modelling and data engineering.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install data@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`data-pipelines`](skills/data-pipelines/SKILL.md) | experimental | Use when building or fixing data pipelines and bulk data movement: ingestion, ETL/ELT, backfills, exports, warehouse or lakehouse loading, streaming, data quality checks and throughput problems. |
| [`database-design`](skills/database-design/SKILL.md) | experimental | Use when designing a schema, writing or optimising queries, choosing indexes, transactions or isolation levels, or reviewing database code for PostgreSQL, MySQL/MariaDB, Redis, ClickHouse or an ORM such as Prisma. Cover… |
| [`database-migrations`](skills/database-migrations/SKILL.md) | experimental | Use when changing a production database schema or data: writing migrations, renaming or dropping columns, backfills, adding indexes or constraints without downtime, and planning rollback. Applies expand-migrate-contract… |

## Origem e manutenção

- Entrada editorial: [manifesto de `data`](../../catalog/curation/domains/data.yaml).
- Requisitos: [spec do domínio](../../docs/specs/data/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/data/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `data-pipelines` | Jeffallan/claude-skills, affaan-m/ECC, github/awesome-copilot, msitarzewski/agency-agents, wshobson/agents |
| `database-design` | affaan-m/ECC, davila7/claude-code-templates, github/awesome-copilot, msitarzewski/agency-agents, wshobson/agents |
| `database-migrations` | affaan-m/ECC, github/awesome-copilot |
