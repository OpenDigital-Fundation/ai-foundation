# Debt ledger — dependency upgrade

Part of `code-quality:debt-ledger`. Adapted reference material; the owner procedure, project conventions, scope and authorization rules take precedence. Examples are not automatically executed.

<!-- source: wshobson/agents plugins/framework-migration/skills/dependency-upgrade/SKILL.md#breaking-change-handling,testing-strategy,staged-upgrade-strategy -->

## Upgrade risk and validation plan

Use these stages to describe a proposed remediation ticket; debt-ledger remains report-only.

1. Inventory exact current and target versions, compatibility constraints, changelog/migration evidence and affected boundaries. Distinguish a security fix from a feature upgrade.
2. Separate small compatible changes from major migrations, and name dependency ordering, rollback conditions and ownership. Do not write a lockfile or run codemods while collecting debt.
3. Define acceptance evidence: affected unit tests, integration/contract compatibility, visual regression where relevant, and production signals that would reveal a regression.
4. Specify the exact project-compatible versions and reviewed migration tools. Floating versions, bulk updates and suppressed installer failures are not a reproducible plan.
5. Hand the approved implementation to the language/framework owner and normal delivery workflow; record completed evidence only after it exists.
