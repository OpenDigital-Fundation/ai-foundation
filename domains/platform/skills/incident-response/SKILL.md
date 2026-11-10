---
name: incident-response
description: "Use when production is down or degraded, an alert fires, a breach is suspected, or a postmortem is due: assess severity, coordinate responders, communicate status, contain, recover, preserve evidence and write a blameless postmortem."
license: MIT
metadata:
  domain: platform
  status: experimental
---
# Incident response

Restore service first, communicate clearly throughout, and learn without blame afterwards.

## 1. Declare and assess
Declare an incident as soon as users are affected. Assign severity from impact (who, how many, which function) and name an incident commander, a communicator and responders.

## 2. Stabilise
Mitigate before diagnosing: roll back the last change, fail over, scale, or disable the feature flag. Every action in production follows the team's change rules; destructive or irreversible steps need the commander's explicit go.

## 3. Communicate
Status updates at a fixed cadence to stakeholders and customers: what is affected, what is being done, next update time. No speculation about cause.

## 4. Resolve and verify
Confirm recovery with the same signals that detected the incident; keep watching for a while before closing.

## 5. Postmortem
Blameless timeline, impact, root cause and contributing factors, what went well, and action items with owners and dates. Suspected security incidents follow the security reference: preserve evidence, contain, and involve the security owner.

## References

Load only what the task needs:

- [`references/role-guide.md`](references/role-guide.md) — the role profile this skill was distilled from: mission, critical rules, deliverable templates and examples
- [`references/security-incidents.md`](references/security-incidents.md) — covers Incident Responder; SEV1 Critical (Response Immediate, 24/7); SEV2 High (Response Same business day); SEV3 Medium (Response Next business day)
- [`references/dependency-outages/README.md`](references/dependency-outages/README.md) — covers Cloud and SaaS Outage Triage
- [`references/derived-guides.md`](references/derived-guides.md) — sections merged from other collections where this skill had no equivalent: Fast Decision Flow; Post-Incident Process; Immediate Actions (First 5 minutes); SRE Best Practices
- `references/postmortem-writing/` — Write effective blameless postmortems with root cause analysis, timelines, and action items. Use when conducting incident reviews, writing postmortem documents, or improving incident response processe
- `references/incident-runbook-templates/` — Create structured incident response runbooks with step-by-step procedures, escalation paths, and recovery actions. Use this skill when building a service outage runbook for a payment processing system
- `references/on-call-handoff-patterns/` — Master on-call shift handoffs with context transfer, escalation procedures, and documentation. Use this skill when transitioning on-call responsibilities between engineers and ensuring the incoming re
