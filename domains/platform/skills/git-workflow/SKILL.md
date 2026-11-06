---
name: git-workflow
description: "Use when choosing a branching strategy, writing commit messages, tidying history before a merge, resolving conflicts, rebasing versus merging, or setting up pre-commit hooks with formatting, type checks and tests."
license: MIT
metadata:
  domain: platform
  status: experimental
---
# Git workflow

Keep history readable and every change reviewable. The repository's own conventions (`AGENTS.md`, `CONTRIBUTING.md`) always win; read them first.

## Branching

- Work on a short-lived branch from the current main; never commit directly to the main branch unless the repository says so. For parallel or isolated work use `workflow:git-worktrees`.
- Prefer trunk-based development with small pull requests; use release branches only when the product ships versions that need maintenance.

## Commits

- One logical change per commit, with tests and code together. Write messages in the repository's style; without one, use Conventional Commits (`feat(scope): imperative summary`, body explaining why).
- Keep the author identity and signing the repository requires. Never bypass hooks or signing to make a commit pass.

## Before merging

- Tidy local history (squash fixups, reorder) only on commits that were never shared. Rewriting shared history, force-pushing and deleting branches are destructive: present the exact refs and get explicit approval first.
- Rebase onto main for a linear history when the team prefers it; merge when the branch is shared. Resolve conflicts by understanding both sides, then re-run the tests.

## Hooks

Run formatting, type checks and fast tests before each commit with a pre-commit framework; keep the slow suite in CI. Setup steps are in the pre-commit reference.

## References

Load only what the task needs:

- [`references/branching-and-history.md`](references/branching-and-history.md) — covers Git Workflow Patterns; What; Why; How
- [`references/practices.md`](references/practices.md) — covers Git Workflow Master
- [`references/pre-commit.md`](references/pre-commit.md) — covers Setup Pre-Commit Hooks
