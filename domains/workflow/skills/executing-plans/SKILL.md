---
name: executing-plans
description: Use when an approved implementation plan (plan.md and tasks.md) exists and it is time to build it. Runs the tasks to completion either by dispatching a fresh implementer and reviewer subagent per task, or inline in the current session, with TDD per task, a ledger that survives context loss, and one fresh-context review of the whole branch at the end.
license: MIT
metadata:
  domain: workflow
  status: experimental
---

# Executing plans

Build an approved plan exactly, prove every step, and leave a record that survives your own forgetting. Paths in this skill and its mode files are relative to this skill's directory.

**Inputs.** A plan written by `workflow:writing-plans` lives next to its spec as `plan.md` (architecture and global constraints) and `tasks.md` (the `### Task N` sections). Wherever the mode files say `PLAN_FILE`, pass `tasks.md`; read `spec.md` and `plan.md` before the first task, and treat `plan.md`'s Global Constraints as part of every task's requirements. A single-file plan from elsewhere works too: pass that file.

## Pick the mode

| Situation | Mode |
|---|---|
| Subagent tool available, tasks mostly independent, and the user did not ask for inline | **Subagent** — read [`modes/subagent.md`](modes/subagent.md) |
| The user asked for inline execution, the harness has no subagent tool, or the run must be cheap | **Inline** — read [`modes/inline.md`](modes/inline.md) |
| Tasks are tightly coupled, or there is no approved plan | Stop. Go back to `workflow:writing-plans` (or `workflow:brainstorming` if there is no approved spec). |

Say which mode you picked and why in one line, then follow that file from the top. Subagent mode costs more (a fresh implementer and reviewer per task) and buys a second pair of eyes on every task; inline mode costs one context plus one final reviewer and relies on TDD as the per-task gate.

## Rules for both modes

**Work in isolation.** Run on a feature branch or worktree (`workflow:git-worktrees`), never directly on the main branch.

**Continuous execution.** Do not pause between tasks to ask "should I continue?" or to post progress summaries. Execute every task in the plan. Narrate at most one short line between tool calls; the ledger carries the record.

**Rulings, not stalls.** Conflicts, ambiguities and plan defects are yours to decide. The spec is the binding authority, the plan is its argument, and your judgment settles what neither answers. Record each decision in the ledger as:

```
Ruling: <what you decided> — <why> — <what it costs if wrong>
```

**Only four things stop you:**

1. An irreversible or destructive operation.
2. A security-sensitive action.
3. A side effect outside the worktree that norms say you ask about first (merge, push to a shared branch, publish, deploy).
4. A plan so broken that every path forward is a guess.

For those, stop and ask. Repository rules (`AGENTS.md`) and the user's instructions about approvals always win over this skill.

**Shared tooling.** `scripts/` holds the workspace, brief and review-package helpers both modes use; `prompts/` holds the implementer and reviewer prompts; `references/` holds preflight, batching, fix-loop, resuming and final-review procedures.

## Finish

After the final review passes, use `testing:verification-before-completion`, then `workflow:finishing-a-branch`.
