---
name: compliance-programs
description: "Use when preparing for or checking compliance: SOC 2, ISO 27001, GDPR, CCPA, HIPAA or PCI-DSS readiness, privacy programmes and data processing, control mapping, evidence collection and policy gaps. Not legal advice."
license: MIT
metadata:
  domain: legal-compliance
  status: experimental
---
# Compliance programmes

Get from "we need SOC 2 / ISO 27001 / GDPR" to controls that work and evidence that proves it. This is preparation support, not legal advice.

## 1. Scope
The framework(s), systems, data types and locations in scope, and the deadline or customer driving it.

## 2. Gap assessment
Map each required control to what exists today: policy, technical control, owner, evidence. Mark met, partial or missing. Reuse mappings between frameworks where controls overlap.

## 3. Remediation plan
Missing and partial controls ranked by audit risk and effort, each with an owner and date. Technical items (access reviews, logging, encryption, backups, vulnerability management) go to the engineering backlog; see `security:security-audit`.

## 4. Privacy
Data inventory and flows, lawful basis, retention, processor agreements, data subject requests and breach procedures.

## 5. Evidence
Collect evidence continuously (screenshots, exports, tickets) with dates; keep policies versioned and acknowledged. Before the audit, run a mock review against the control list.

## References

Load only what the task needs:

- [`references/role-guide.md`](references/role-guide.md) — the role profile this skill was distilled from: mission, critical rules, deliverable templates and examples
- [`references/privacy.md`](references/privacy.md) — covers Data Privacy Officer
- [`references/checks.md`](references/checks.md) — covers Legal Compliance Checker; Executive Summary; Detailed Compliance Analysis; Risk Mitigation Strategies
- [`references/dependency-licenses/README.md`](references/dependency-licenses/README.md) — upstream hook documentation kept for its policy and pattern catalogue; the hook scripts are not copied. Before running a similar hook, adapt the input parser to your host, redact what it logs and test bypass and fail-closed behaviour; licence checks by substring are heuristics, not proof of compliance
- `references/pci-compliance/` — Implement PCI DSS compliance requirements for secure handling of payment card data and payment systems. Use when securing payment processing, achieving PCI compliance, or implementing payment card sec
