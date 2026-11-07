# Spec — Catálogo do domínio `data`

- **Domínio:** data
- **Status:** em implementação (Onda 2)
- **Fronteira:** bancos de dados, migrações, modelagem e engenharia de dados.

## Resultado (gerado por `tools.curation.bundle` a partir de [manifesto editorial](../../../../catalog/curation/domains/data.yaml))

| Artefato | Base | Referências |
|---|---|---|
| `database-design` | ECC `postgres-patterns` | ECC `mysql-patterns`, `redis-patterns`, `clickhouse-io`, `prisma-patterns`, agent `database-reviewer`; agency *Database Optimizer*, *Database Reliability Engineer* |
| `database-migrations` | ECC `database-migrations` | — (absorve o comando `database-migration`) |
| `data-pipelines` | agency *Data Engineer* | ECC `data-throughput-accelerator` |

Variantes de ORM por linguagem (JPA, MyBatis, Exposed, Django ORM) ficam nos pacotes de `languages`.

## Pendências

- Agency *AI Data Remediation Engineer*, *Data Consolidation Agent*, *Sales Data Extraction Agent*; ECC `data-scraper-agent`: decidir (os dois últimos tendem a `sales`/`research`).
