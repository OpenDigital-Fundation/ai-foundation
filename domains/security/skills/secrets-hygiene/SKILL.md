---
name: secrets-hygiene
description: Use when a secret, token, key or password may have leaked (committed, logged, shipped in a bundle or image), when setting up secret scanning, or when deciding how an application should store, broker and rotate credentials. Treats any exposed secret as already compromised and drives rotation first, then cleanup, audit and prevention.
license: MIT
metadata:
  domain: security
  status: experimental
---

# Secrets hygiene

A secret that was committed or logged is **already burned**: the old value lives on in history, clones, CI logs and possibly an attacker's hands. Deleting it from the file is never the fix. Rotation at the provider is.

## Rules

- **Never print a secret.** Not in output, logs, errors or reports; redact to its type and last few characters at most.
- **Never ship a secret to a client.** No secrets in bundles, public env prefixes (`NEXT_PUBLIC_`, `VITE_`, `EXPO_PUBLIC_`), mobile apps or image layers. Keep them out of URLs, query strings and analytics.
- **Short-lived and least privilege.** Prefer dynamic, expiring credentials and workload identity or OIDC federation over static keys. One credential per workload and purpose, so revoking one never forces a fleet-wide rotation.
- **Know the public-vs-secret line.** Publishable and anon keys are meant to be public; allowlist them so the scanner stays credible.

## When a secret is exposed

Work in this order. Stopping at step 2 is the most common failure.

1. **Rotate now.** Revoke the exposed credential at the provider and issue a replacement. This is the fix. Tell the user exactly which credential and where to rotate it; rotating usually requires their access.
2. **Replace in code** with a reference to the secret store or environment, and deploy.
3. **Purge from history** only with the user's explicit approval: rewriting history (`git filter-repo`) and force-pushing is destructive and must be coordinated with everyone who has a clone. Present the exact branches and refs first.
4. **Audit usage** during the exposure window, from the commit or log time to the revocation time. Widen the response if the credential was used.
5. **Close the gap.** Why did the gate miss it? Add the pattern to the scanner and make the secure path easier.

The incident is closed when the exposed credential is revoked and a fresh one is in place, not when the code is clean.

## Prevention

1. **Scan before the commit lands** (a pre-commit hook such as gitleaks) **and again in CI**, with a tuned ruleset and allowlist so precision stays high and nobody learns to bypass it.
2. **Inventory and broker.** Find secrets already in play (code, `.env` files, CI variables, images) and move them into a secret manager with access policy and audit logging.
3. **Rotate on a schedule.** Automate where the provider supports it; otherwise write a runbook. Overlap old and new during cutover so rotation is never an outage. Every credential has an owner, a lifetime and a revocation path.

## Secrets that leak through serialization

Generated `__repr__`, `toJSON`, logging and tracing can print a secret no one wrote to a log. To find these in Python or JavaScript/TypeScript code, follow [references/serialization-leaks/README.md](references/serialization-leaks/README.md).

## Hand-off

For a full review of how an application handles credentials, use `security:security-audit`. For agent and MCP credentials, see `security:agent-security`.

## Further references

Guides merged from github/awesome-copilot; load only what the task needs:

- [`references/scanning-recipes.md`](references/scanning-recipes.md)

## Derived guides

Load only the reference needed for the task:

- [`references/derived/secret-scanning.md`](references/derived/secret-scanning.md) — Core Workflow — Enable Secret Scanning; Core Workflow — Resolve Blocked Pushes
- [`references/derived/secrets-management.md`](references/derived/secrets-management.md) — HashiCorp Vault Integration; External Secrets Operator; Secret Rotation
