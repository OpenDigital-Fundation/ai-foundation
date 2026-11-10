---
name: codebase-audit
description: Use when the user asks for a thorough review or audit of a whole codebase, a branch or diff, or a folder - "audit this repo", "review the whole project", "find vulnerabilities", "find duplicated code", "optimise the code", "make it production-ready". Orchestrates specialist reviewers (security, data and secret leaks, dependencies, correctness, performance, duplication and architecture, practices, tests, infrastructure) and a sceptical verifier that removes false positives, then writes a prioritised report with fixes.
license: MIT
metadata:
  domain: code-quality
  status: experimental
---

# Codebase audit

You are the **orchestrator** of a high-rigour review. You do not review alone: you coordinate specialists, each with a narrow, deep focus, submit everything to a sceptical verifier and consolidate a report people can trust.

Non-negotiable principles:

1. **Evidence over opinion.** Every finding has a file, a line and a real excerpt. No generic findings ("consider validating input").
2. **No false positives in the final report.** Ten real problems beat fifty doubtful ones; the verifier exists for this.
3. **Read-only while reviewing.** Do not change project files, install packages, run migrations or commit. Allowed: reading, searching, `git log/diff/show/blame`, listing dependencies and, if the user allows it, linters, tests and audits that do not modify the project.
4. **Never expose secrets.** Mask any credential you quote (`sk_live_****9f2a`). Never send project code or secrets to external services.
5. **Prioritise by real impact**, not by count.

## Step 0 — Scope and mode

Infer, and ask only when you cannot:

- **Scope:** `project` (default, the whole repository); `diff` (changes against a base, `git diff <base>...HEAD`, default `main`; specialists may read surrounding code); `path` (a folder or file).
- **Mode:** `full` (default, all specialists); `quick` (mapper, security, data leaks, correctness and verifier; with no subagents available, use [references/quick-audit.md](references/quick-audit.md)); `focus:<area>` (mapper, the specialist for that area, verifier).

Always exclude `node_modules`, `vendor`, `dist`, `build`, `.next`, `target`, `bin/obj`, `__pycache__`, `.venv`, minified files, generated files and lockfiles (except for the dependency specialist).

## Step 1 — Map (sequential, mandatory)

Run the **mapper** ([agents/01-mapper.md](agents/01-mapper.md)) first. It produces the **project map**: stack, structure, entry points, trust boundaries, sensitive data flows and files ranked by risk. Every other specialist receives the map. For large projects (over ~300 source files), use the map to split the code into **batches by module** and give batches to several instances of the same specialist when the platform allows it.

## Step 2 — Specialists (in parallel whenever possible)

| # | Specialist | Instructions | Focus |
|---|---|---|---|
| 02 | Security | [agents/02-security.md](agents/02-security.md) | Injection, authentication, authorisation, cryptography, SSRF, XSS, CSRF, deserialisation, OWASP Top 10 / ASVS |
| 03 | Data and secret leaks | [agents/03-data-leaks.md](agents/03-data-leaks.md) | Credentials in code and git history, personal data in logs, responses that expose data, GDPR/LGPD |
| 04 | Dependencies and supply chain | [agents/04-dependencies.md](agents/04-dependencies.md) | CVEs, abandoned versions, pinning, lockfiles, typosquatting, licences, install scripts |
| 05 | Correctness and logic | [agents/05-correctness.md](agents/05-correctness.md) | Bugs, edge cases, concurrency, error handling, state, broken contracts |
| 06 | Performance | [agents/06-performance.md](agents/06-performance.md) | Complexity, N+1, I/O, memory, caching, rendering, bundles, queries |
| 07 | Duplication and architecture | [agents/07-duplication-architecture.md](agents/07-duplication-architecture.md) | Duplicated and dead code, coupling, layering, wrong abstractions, reuse of existing helpers |
| 08 | Practices and readability | [agents/08-practices.md](agents/08-practices.md) | Language idioms, names, typing, complexity, consistency, documentation |
| 09 | Tests and reliability | [agents/09-tests.md](agents/09-tests.md) | Coverage of critical paths, flaky tests, weak asserts, excessive mocks, observability |
| 10 | Infrastructure and configuration | [agents/10-infrastructure.md](agents/10-infrastructure.md) | Docker, CI/CD, IaC, CORS, headers, TLS, permissions, per-environment configuration |

Each specialist reads its instructions, the project map and [references/finding-format.md](references/finding-format.md); investigates for real (opens files, follows calls, traces data from input to sink) rather than only grepping; and returns **only** its findings in the standard format, plus "Strengths observed" and "Areas not covered" (what it could not analyse and why). Language specifics come from the matching `languages:<language>` pack.

## Step 3 — Sceptical verification (mandatory)

Merge all findings, remove obvious duplicates between specialists (same file, line and cause: keep one, cite the specialists) and send them to the **verifier** ([agents/11-verifier.md](agents/11-verifier.md)). It reopens the code of each finding and marks it `CONFIRMED`, `LIKELY` or `DISMISSED`, adjusting severity when needed. Dismissed findings do not enter the report (one line each in the appendix). With many findings, split verification across several verifiers by specialist or module.

## Step 4 — Final report

Write the report with [references/report-template.md](references/report-template.md) to `docs/code-review/REPORT-<YYYY-MM-DD>.md` in the reviewed project (create the folder; this is the only file you write; the repository's `AGENTS.md` may set another location). Then give the user a summary: overall grade, count by severity and the five most urgent items. Do not apply fixes automatically; offer: "Do you want me to fix the critical and high items now?"

## Running the specialists on each platform

The specialist content is the same everywhere; only the delegation mechanism changes.

- **Claude Code (or any harness with subagents):** dispatch a read-only subagent per specialist whose prompt contains (1) the full specialist file, (2) the project map, (3) the finding format, (4) the scope or batch and (5) the read-only rule. Dispatch all Step 2 specialists in the same message so they run in parallel; wait for all before Step 3.
- **Codex:** use native multi-agent support if enabled; otherwise, if commands are allowed, run each specialist as a non-interactive read-only subprocess (for example `codex exec --sandbox read-only "<specialist prompt>"`), saving each output outside the project; otherwise use sequential mode.
- **Other harnesses (Antigravity, Gemini CLI, OpenCode):** create one parallel task per specialist if the agent manager supports it; otherwise use sequential mode.
- **Sequential mode (universal fallback):** run one specialist at a time; before each, reread its file and take **only** that role; record each specialist's findings in a separate section before moving on; the verifier runs last and reopens the code of every finding as if it trusted nobody.

## Quality rules for every specialist

- Cite the exact location: `path/file.ext:line` (or a range).
- Show the short problematic excerpt and the suggested fix in code.
- Explain the concrete failure scenario: which input or state causes which harm.
- Calibrate severity with the finding format; do not inflate.
- Follow the project's conventions: fixes match its style, libraries and architecture; look for an existing helper before suggesting a new one.
- Do not repeat what a configured linter already catches; if no linter is configured, that is one practices finding.
- State uncertainty: if a finding depends on something outside the code (production configuration, a proxy), say so.

For reviewing a single change rather than a whole codebase, use `code-quality:code-review`; for a deep security-only audit with sandboxed validation, use `security:security-audit`.
