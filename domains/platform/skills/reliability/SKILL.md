---
name: reliability
description: "Use when defining SLOs and error budgets, adding logs, metrics and traces, building operator dashboards (Grafana, SigNoz), planning capacity, running chaos experiments, or maintaining infrastructure health."
license: MIT
metadata:
  domain: platform
  status: experimental
---
# Reliability and observability

Make reliability measurable, then spend effort where the measurement says.

## 1. Define SLOs
For each user-facing journey: the SLI (successful, fast-enough requests over valid requests), the target and window, and the error budget. Start from what users notice, not what is easy to measure.

## 2. Instrument
Structured logs with request IDs, RED metrics (rate, errors, duration) per service, traces across service boundaries, and saturation for the resources that run out first.

## 3. Alert on symptoms
Multi-window burn-rate alerts on the SLOs, routed to an owner, each with a runbook. Remove alerts nobody acts on.

## 4. Dashboards
One page per service that answers "is it healthy, and if not, where": SLOs and budget, golden signals, recent deploys. See the dashboards reference.

## 5. Spend the budget
Budget left: ship. Budget burnt: freeze risky changes and fix reliability. Reduce toil you repeat, plan capacity from data, and test failure modes deliberately (game days, chaos experiments) in safe environments.

## References

Load only what the task needs:

- [`references/role-guide.md`](references/role-guide.md) — the role profile this skill was distilled from: mission, critical rules, deliverable templates and examples
- [`references/dashboards.md`](references/dashboards.md) — covers Dashboard Builder
- [`references/infrastructure-maintenance.md`](references/infrastructure-maintenance.md) — covers Infrastructure Maintainer; Executive Summary; Detailed Infrastructure Analysis; Cost Analysis and Optimization
- [`references/operational-checklists/README.md`](references/operational-checklists/README.md) — covers Platform SRE for Kubernetes; DevOps Core Principles
- [`references/derived-guides.md`](references/derived-guides.md) — sections merged from other collections where this skill had no equivalent: Common Optimizations; INP: Interaction to Next Paint; CLS: Cumulative Layout Shift; Advanced React Performance Patterns; Quick-Start Examples
- `references/slo-implementation/` — Define and implement Service Level Indicators (SLIs) and Service Level Objectives (SLOs) with error budgets and alerting. Use when establishing reliability targets, implementing SRE practices, or meas
- `references/distributed-tracing/` — Implement distributed tracing with Jaeger and Tempo to track requests across microservices and identify performance bottlenecks. Use when debugging microservices, analyzing request flows, or implement
