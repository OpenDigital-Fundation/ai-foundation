---
name: code-review
description: Use when a change needs review - after finishing a plan task or feature, before merging, when stuck, or when the user asks to review a diff, commit, branch or pull request. Pins the range, finds the spec and the repository's standards, dispatches a fresh-context reviewer on two axes (standards and spec), and returns numbered, evidence-backed findings in plain English with a verdict.
license: MIT
metadata:
  domain: code-quality
  status: experimental
---

# Code review

Catch problems before they cascade, with a reviewer that sees the work product and never your session's history.

## When

- **Always:** after each task in `workflow:executing-plans` (subagent mode does this for you), after a feature is complete, and before merging to the main branch.
- **Useful:** when stuck, before a refactor (baseline), after fixing a complex bug.
- Whole-repository audits are a different job: use `code-quality:codebase-audit`.

## 1. Pin the range

Use what the user named: a commit, branch, tag, pull request, or files. Nothing named: the uncommitted changes, or the last commit if there are none.

```bash
BASE=$(git merge-base origin/main HEAD)   # or the fixed point the user gave
HEAD_SHA=$(git rev-parse HEAD)
git rev-parse "$BASE" && git diff --stat "$BASE"...HEAD
```

A bad ref or an empty diff fails here, not inside the reviewer.

## 2. Find the spec

In order: issue references in the commit messages; a path the user passed; the spec folder for this feature (layout from `AGENTS.md`, default `docs/specs/<domain>/<feature>/`); otherwise ask. If there is no spec, the spec axis reports "no spec available".

## 3. Find the standards

Every file that documents how code is written here (`CODING_STANDARDS.md`, `CONTRIBUTING.md`, `AGENTS.md`, linter configs). Add the [smell baseline](references/smell-baseline.md); documented repo standards override it. Skip anything tooling already enforces.

## 4. Dispatch the reviewer

Dispatch the `code-quality:code-reviewer` agent (in harnesses without plugin agents, a general-purpose subagent whose prompt is the body of `agents/code-reviewer.md` in this domain). Give it: what was built, the spec or requirements, `BASE..HEAD`, the standards sources, and the axis.

- **Small change:** one reviewer, axis `both`.
- **Large change or high stakes:** two reviewers in parallel, one `standards` and one `spec`, each with a fresh context; then merge their findings, removing duplicates and keeping the higher severity.

## 5. Act on the findings

- Fix **Must fix** items before going on; fix **Should fix** before merging; note **Nice to have** as follow-ups.
- Answer the review with `code-quality:receiving-code-review`: verify each finding, and push back with evidence when the reviewer is wrong.
- Never skip review because the change "is simple", and never proceed with an unfixed Must fix.

## 6. Report

Relay the reviewer's report to the user unchanged in structure (what the change does, numbered findings, verdict), so they can say "fix 2 and 5".
