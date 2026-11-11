---
name: threat-modeling
description: Use when designing a new system or feature that handles sensitive data, money, identity or untrusted input, before a security review, or when the user asks for a threat model. Maps data flows and trust boundaries, runs STRIDE per component, inventories the attack surface, and ranks threats by likelihood and impact into mitigations and security tests.
license: MIT
metadata:
  domain: security
  status: experimental
---
<!-- Modified by OpenDigital; procedure merges openai/skills security-threat-model (Apache-2.0). See PROVENANCE.yaml in this domain. -->

# Threat modeling

Find what can go wrong **before** it is built or shipped, and turn each credible threat into a mitigation and a test. A threat model is a design artefact: it lives next to the spec and changes with it.

## Adversarial questions

Ask these of every component:

1. **What can be abused?** Every feature is attack surface.
2. **What happens when this fails?** Assume each component fails; it must fail closed and securely.
3. **Who benefits from breaking this?** Motivation sets priority.
4. **What is the blast radius?** One compromised component must not take the rest with it.

## Procedure

1. **Scope.** Name the system or feature, the spec it belongs to, and what is out of scope. Read the code, configuration and infrastructure definitions that exist; do not model from imagination when the system is already there. Identify how it runs (server, CLI, library, worker) and its entry points, and keep runtime behaviour separate from CI/build tooling and from tests and examples.
   - **Evidence anchors.** Back every claim about a component, flow or control with a path (plus a symbol, config key or short snippet). What has no evidence is an explicit assumption, not a fact.
2. **Data flows.** Trace where sensitive data enters, moves, is stored and leaves. Classify it: credentials, personal data, financial, health, public.
3. **Trust boundaries.** List every place control changes hands: internet to app, app to services, service to database, service to service, user to admin, agent to tool. For each, record the controls that exist today.
4. **STRIDE per component.** For each component crossing a boundary, check Spoofing, Tampering, Repudiation, Information disclosure, Denial of service and Elevation of privilege. Write a concrete attack scenario for each credible threat; skip categories with no credible scenario rather than padding the table.
5. **Attack surface.** External (public APIs, auth flows, uploads, websockets), internal (RPC, queues, caches), data (queries, logs, backups), infrastructure (CI/CD, secrets, DNS) and supply chain (dependencies, CDN scripts, third-party APIs, agent tools and MCP servers).
6. **Attacker capabilities.** From exposure and intended use, describe what a realistic attacker controls — and, explicitly, what they do not (attacker- vs operator- vs developer-controlled input). Threats that need control nobody realistically has are downgraded, not dropped silently.
7. **Rank.** Likelihood (how easy to exploit) × impact (what is at stake), low/medium/high with a one-line justification each, adjusted for controls that exist today. Name the assumptions that most move the ranking. Keep the list short and specific: a few abuse paths tied to assets beat a long generic table. Critical and high threats need a mitigation before release.
   - *High:* pre-auth RCE, auth bypass, cross-tenant access, sensitive-data exfiltration, key or token theft, config or model integrity compromise, sandbox escape.
   - *Medium:* targeted DoS of a critical component, partial data exposure, rate-limit bypass with measurable impact, log poisoning that hides detection.
   - *Low:* low-sensitivity leaks, noisy DoS with an easy fix, issues with unlikely preconditions.
8. **Confirm context.** Before the final write-up, state the assumptions that change scope or ranking and ask the user one to three targeted questions (owner and environment, exposure, auth model, data sensitivity, multi-tenancy). Wait for the answer; if there is none, keep the assumptions visible and mark dependent mitigations as conditional.
9. **Mitigate and test.** Separate controls that exist (with evidence) from recommended ones. For each ranked threat: the smallest effective control at a named component, boundary or entry point (phrasing patterns in [references/assets-and-controls.md](references/assets-and-controls.md)), its owner, and a failing security test that demonstrates the threat (write it test-first with `testing:test-driven-development`).
10. **Check and record.** Confirm every entry point and trust boundary appears in at least one threat, runtime and CI are separated, and open questions are listed. Draw one compact Mermaid flowchart of components and boundaries (plain node IDs, quoted labels, no paths in labels). Write the model with [templates/threat-model.md](templates/threat-model.md) next to the spec (default `docs/specs/<domain>/<feature>/threat-model.md`). Decisions with lasting trade-offs go to `architecture:decision-records`.

## Security test checklist

Make sure tests exist for each applicable class:

- **Authentication:** missing or expired token, algorithm confusion, wrong issuer or audience.
- **Authorization:** IDOR, vertical and horizontal privilege escalation, mass assignment.
- **Input:** boundary values, special characters, oversized payloads, unexpected fields.
- **Injection:** SQL, XSS, command, SSRF, path traversal, template injection.
- **Headers and transport:** CSP, HSTS, content-type sniffing, framing, CORS.
- **Secrets:** none in code, logs, URLs, client bundles or image layers (see `security:secrets-hygiene`).

## Policy for review tools

A threat model records analysis; a `SECURITY_MODEL.md` tells scanners and reviewers what is reportable — invariants with stable IDs, finding classes and severity, narrow exclusions and dated accepted risks. To write or review one, follow [references/security-model/README.md](references/security-model/README.md); to make review procedures read it, see [references/security-model/references/consuming-policy.md](references/security-model/references/consuming-policy.md).

## Hand-off

To verify an existing implementation against the model, use `security:security-audit`. For agents and tool-using systems, add the boundaries in `security:agent-security`.

## Further references

Load only what the task needs:

- [`references/stride-analysis-patterns/README.md`](references/stride-analysis-patterns/README.md) — Apply STRIDE methodology to systematically identify threats. Use when analyzing system security, conducting threat modeling sessions, or creating security documentation.
- [`references/attack-tree-construction/README.md`](references/attack-tree-construction/README.md) — Build comprehensive attack trees to visualize threat paths. Use when mapping attack scenarios, identifying defense gaps, or communicating security risks to stakeholders.
- [`references/threat-mitigation-mapping/README.md`](references/threat-mitigation-mapping/README.md) — Map identified threats to appropriate security controls and mitigations. Use when prioritizing security investments, creating remediation plans, or validating control effectiveness.
- [`references/security-requirement-extraction/README.md`](references/security-requirement-extraction/README.md) — Derive security requirements from threat models and business context. Use when translating threats into actionable requirements, creating security user stories, or building security test cases.

## Derived guides

Load only the reference needed for the task:

- [`references/derived/data-breach-blast-radius.md`](references/derived/data-breach-blast-radius.md) — Execution Workflow
