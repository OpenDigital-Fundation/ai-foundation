---
name: harness-design
description: "Use when designing or auditing an AI agent or agentic product: its tools and action space, observation formatting, permissions, identity and trust, multi-agent topology, and the twelve-layer audit for wrapper regressions, memory pollution and silent repair loops."
license: MIT
metadata:
  domain: agent-engineering
  status: experimental
---
# Agent Harness Construction

Use this skill when you are improving how an agent plans, calls tools, recovers from errors, and converges on completion.

## Core Model

Agent output quality is constrained by:
1. Action space quality
2. Observation quality
3. Recovery quality
4. Context budget quality

## Action Space Design

1. Use stable, explicit tool names.
2. Keep inputs schema-first and narrow.
3. Return deterministic output shapes.
4. Avoid catch-all tools unless isolation is impossible.

## Granularity Rules

- Use micro-tools for high-risk operations (deploy, migration, permissions).
- Use medium tools for common edit/read/search loops.
- Use macro-tools only when round-trip overhead is the dominant cost.

## Observation Design

Every tool response should include:
- `status`: success|warning|error
- `summary`: one-line result
- `next_actions`: actionable follow-ups
- `artifacts`: file paths / IDs

## Error Recovery Contract

For every error path, include:
- root cause hint
- safe retry instruction
- explicit stop condition

## Context Budgeting

1. Keep system prompt minimal and invariant.
2. Move large guidance into skills loaded on demand.
3. Prefer references to files over inlining long documents.
4. Compact at phase boundaries, not arbitrary token thresholds.

## Architecture Pattern Guidance

- ReAct: best for exploratory tasks with uncertain path.
- Function-calling: best for structured deterministic flows.
- Hybrid (recommended): ReAct planning + typed tool execution.

## Benchmarking

Track:
- completion rate
- retries per task
- pass@1 and pass@3
- cost per successful task

## Anti-Patterns

- Too many tools with overlapping semantics.
- Opaque tool output with no recovery hints.
- Error-only output without next steps.
- Context overloading with irrelevant references.

## References

Load only what the task needs:

- [`references/repository-harness.md`](references/repository-harness.md) — covers Harness Engineering; Summary; Root Cause; Prevention
- [`references/architecture-audit.md`](references/architecture-audit.md) — covers Architecture Audit
- [`references/agentic-engineering.md`](references/agentic-engineering.md) — covers Agentic Engineering; AI-First Engineering
- [`references/multi-agent-systems.md`](references/multi-agent-systems.md) — covers Multi- Systems Architect; AgentsOrchestrator; Current Task Validation Process; Failure Management
- [`references/identity-and-trust.md`](references/identity-and-trust.md) — covers Agentic Identity & Trust Architect
- [`references/harness-tuning.md`](references/harness-tuning.md) — covers harness-optimizer
- [`references/enterprise-operations.md`](references/enterprise-operations.md) — covers Enterprise Ops
- [`references/session-observability/README.md`](references/session-observability/README.md) — upstream hook documentation kept for its policy and pattern catalogue; the hook scripts are not copied. Before running a similar hook, adapt the input parser to your host, redact what it logs and test bypass and fail-closed behaviour; never log prompts or tool input unredacted
- [`references/customizations/README.md`](references/customizations/README.md) — covers Custom File Guidelines; Dynamic Parameters; Your Mission; Variable Resolution Strategy
- [`references/derived-guides.md`](references/derived-guides.md) — sections merged from other collections where this skill had no equivalent: How to work; Choose a route; Shared decision rules

- [`references/event-driven-supervision.md`](references/event-driven-supervision.md) — reviewed event admission, scope/version revalidation, executor ownership and recovery; research defaults do not override host permissions.
