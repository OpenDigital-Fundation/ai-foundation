# Secrets hygiene — secret scanning

Part of `security:secrets-hygiene`. Adapted reference material; the owner procedure, project conventions, scope and authorization rules take precedence. Examples are not automatically executed.

<!-- source: github/awesome-copilot skills/secret-scanning/SKILL.md#core-workflow-enable-secret-scanning,core-workflow-resolve-blocked-pushes -->

## Repository scanning and blocked pushes

Assess the repository's current scanner and push-protection coverage before proposing changes. Feature availability and billing depend on the hosting plan; settings changes, organization-wide rollout and transmission of private repository data require explicit authorization. Do not enable paid scanning, credential validity checks or AI services by default.

If protection blocks a push, keep the block in place while classifying the finding. Treat an actual exposed credential as compromised: revoke/rotate, review copies and access, then prepare a narrow cleanup. Never solve the block by bypassing it for convenience.

For a verified false positive, document the evidence and use the repository's approved exception process with the smallest scope. Do not exclude whole docs/test directories merely because they contain examples, and do not publish matched values in tickets or logs.

Changing published history, amending commits, granting bypass privileges and retrying a push are separate authorized actions. Preserve signing and review requirements. A clean scan is limited to the content and patterns actually scanned; consult current host documentation before relying on event, API or exception semantics.
