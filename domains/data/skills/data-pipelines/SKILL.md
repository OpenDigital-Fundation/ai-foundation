---
name: data-pipelines
description: "Use when building or fixing data pipelines and bulk data movement: ingestion, ETL/ELT, backfills, exports, warehouse or lakehouse loading, streaming, data quality checks and throughput problems."
license: MIT
metadata:
  domain: data
  status: experimental
---
# Data pipelines

Move data reliably: correct, complete, on time, and recoverable when something breaks.

## 1. Define the contract
Sources, destination, schema, freshness target, volume, and who consumes the data. Write the data contract (fields, types, keys, nullability) before writing code.

## 2. Design the flow
Batch or streaming; ELT into the warehouse or ETL before it; incremental loads keyed on a watermark or change data capture rather than full reloads. Every step idempotent so a rerun never duplicates.

## 3. Build in quality checks
Row counts, uniqueness of keys, nulls, ranges and referential checks at each stage; quarantine bad records instead of failing silently.

## 4. Operate
Orchestrate with retries and alerts, record lineage, and keep backfills as a first-class, rate-limited job. For slow or large movements, see the throughput reference.

## 5. Verify
Compare source and destination totals for the run, check freshness against the target, and document how to replay a failed window.

## References

Load only what the task needs:

- [`references/role-guide.md`](references/role-guide.md) — the role profile this skill was distilled from: mission, critical rules, deliverable templates and examples
- [`references/throughput.md`](references/throughput.md) — covers Data Throughput Accelerator
- [`references/spark/README.md`](references/spark/README.md) — covers PySpark Performance & Parallelism Reviewer (); Decision Rules (must follow); Example prompts this agent is optimized for; Safety / correctness boundaries
- [`references/derived-guides.md`](references/derived-guides.md) — sections merged from other collections where this skill had no equivalent: Code Patterns; Example: Minimal Batch Pipeline
- `references/airflow-dag-patterns/` — Build production Apache Airflow DAGs with best practices for operators, sensors, testing, and deployment. Use when creating data pipelines, orchestrating workflows, or scheduling batch jobs.
- `references/dbt-transformation-patterns/` — Master dbt (data build tool) for analytics engineering with model organization, testing, documentation, and incremental strategies. Use when building data transformations, creating data models, or imp
- `references/data-quality-frameworks/` — Implement data quality validation with Great Expectations, dbt tests, and data contracts. Use when building data quality pipelines, implementing validation rules, or establishing data contracts.
