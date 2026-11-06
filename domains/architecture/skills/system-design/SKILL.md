---
name: system-design
description: "Use when designing a service, system or major feature end to end: components and boundaries, data flow, APIs and contracts, consistency and failure handling, scalability and latency budgets, caching, real-time collaboration and internationalisation concerns, and the trade-offs behind each choice."
license: MIT
metadata:
  domain: architecture
  status: experimental
---
# System design

Choose a structure that meets the requirements with the least complexity, and record why.

## 1. Requirements
Functional scope; non-functional targets with numbers (load, latency, availability, data size, consistency, compliance); constraints (team, budget, existing systems).

## 2. Shape
Components and their responsibilities, data ownership and flows, synchronous versus asynchronous boundaries, and where state lives. Draw it. Prefer the simplest shape that meets the targets: a well-structured monolith beats premature services.

## 3. Interfaces
APIs and events between components with their contracts (`architecture:api-design`), versioning, idempotency and error semantics.

## 4. Failure and scale
What happens when each dependency is slow or down (timeouts, retries with backoff, circuit breakers, queues), how it scales (stateless tiers, partitioning, caching with invalidation), and the latency budget per hop.

## 5. Decide and record
Compare two or three designs on the targets and trade-offs, pick one, and write the hard-to-reverse choices as ADRs (`architecture:decision-records`). Hand the design to `workflow:writing-plans`.

## References

Load only what the task needs:

- [`references/role-guide.md`](references/role-guide.md) — the role profile this skill was distilled from: mission, critical rules, deliverable templates and examples
- [`references/backend-architecture.md`](references/backend-architecture.md) — covers Backend Architect; High-Level Architecture; Service Decomposition; Backend Development Patterns
- [`references/architect-agent.md`](references/architect-agent.md) — covers ADR-001 Use Redis for Semantic Search Vector Storage; Context; Decision; Consequences
- [`references/api-platforms.md`](references/api-platforms.md) — covers API Platform Engineer
- [`references/latency.md`](references/latency.md) — covers Latency Critical Systems
- [`references/error-handling.md`](references/error-handling.md) — covers Error Handling Patterns
- [`references/caching.md`](references/caching.md) — covers Content-Hash File Cache Pattern
- [`references/realtime-collaboration.md`](references/realtime-collaboration.md) — covers Realtime Collaboration Engineer
- [`references/internationalisation.md`](references/internationalisation.md) — covers Internationalization Engineer; i18n Sync
