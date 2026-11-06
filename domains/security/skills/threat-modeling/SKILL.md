---
name: threat-modeling
description: Use when designing a new system or feature that handles sensitive data, money, identity or untrusted input, before a security review, or when the user asks for a threat model. Maps data flows and trust boundaries, runs STRIDE per component, inventories the attack surface, and ranks threats by likelihood and impact into mitigations and security tests.
license: MIT
metadata:
  domain: security
  status: experimental
---

# Threat modeling

Find what can go wrong **before** it is built or shipped, and turn each credible threat into a mitigation and a test. A threat model is a design artefact: it lives next to the spec and changes with it.

## Adversarial questions

Ask these of every component:

1. **What can be abused?** Every feature is attack surface.
2. **What happens when this fails?** Assume each component fails; it must fail closed and securely.
3. **Who benefits from breaking this?** Motivation sets priority.
4. **What is the blast radius?** One compromised component must not take the rest with it.

## Procedure

1. **Scope.** Name the system or feature, the spec it belongs to, and what is out of scope. Read the code, configuration and infrastructure definitions that exist; do not model from imagination when the system is already there.
2. **Data flows.** Trace where sensitive data enters, moves, is stored and leaves. Classify it: credentials, personal data, financial, health, public.
3. **Trust boundaries.** List every place control changes hands: internet to app, app to services, service to database, service to service, user to admin, agent to tool. For each, record the controls that exist today.
4. **STRIDE per component.** For each component crossing a boundary, check Spoofing, Tampering, Repudiation, Information disclosure, Denial of service and Elevation of privilege. Write a concrete attack scenario for each credible threat; skip categories with no credible scenario rather than padding the table.
5. **Attack surface.** External (public APIs, auth flows, uploads, websockets), internal (RPC, queues, caches), data (queries, logs, backups), infrastructure (CI/CD, secrets, DNS) and supply chain (dependencies, CDN scripts, third-party APIs, agent tools and MCP servers).
6. **Rank.** Likelihood (how easy to exploit) × impact (what is at stake). Critical and high threats need a mitigation before release.
7. **Mitigate and test.** For each ranked threat: the smallest effective control, its owner, and a failing security test that demonstrates the threat (write it test-first with `testing:test-driven-development`).
8. **Record.** Write the model with [templates/threat-model.md](templates/threat-model.md) next to the spec (default `docs/specs/<domain>/<feature>/threat-model.md`). Decisions with lasting trade-offs go to `architecture:decision-records`.

## Security test checklist

Make sure tests exist for each applicable class:

- **Authentication:** missing or expired token, algorithm confusion, wrong issuer or audience.
- **Authorization:** IDOR, vertical and horizontal privilege escalation, mass assignment.
- **Input:** boundary values, special characters, oversized payloads, unexpected fields.
- **Injection:** SQL, XSS, command, SSRF, path traversal, template injection.
- **Headers and transport:** CSP, HSTS, content-type sniffing, framing, CORS.
- **Secrets:** none in code, logs, URLs, client bundles or image layers (see `security:secrets-hygiene`).

## Hand-off

To verify an existing implementation against the model, use `security:security-audit`. For agents and tool-using systems, add the boundaries in `security:agent-security`.
