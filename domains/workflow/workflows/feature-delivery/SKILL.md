---
name: feature-delivery
description: Use when the user wants a feature, behaviour change or new project taken all the way from idea to a merge-ready branch. Orchestrates the delivery skills in order (design, spec, plan, isolated execution with TDD, verification, review, branch completion) and enforces the approval gate between each stage.
license: MIT
metadata:
  domain: workflow
  status: experimental
---

# Feature delivery

The end-to-end path for building something. Each stage is owned by one skill; this workflow only decides **which stage you are in, what must exist to leave it, and who approves**. Do not repeat a stage's procedure here: load its skill.

Repository rules (`AGENTS.md`) and the user's instructions override this workflow, including where documents go and what needs approval.

## Stages

| # | Stage | Skill | Exit gate | Approver |
|---|---|---|---|---|
| 1 | Understand and design | `workflow:brainstorming` (use `workflow:grilling` if the user brings a plan to attack; `workflow:initiative-mapping` if it is too big for one session) | `spec.md` written in the spec folder | **User approves the spec** |
| 2 | Plan | `workflow:writing-plans` | `plan.md` and `tasks.md` next to the spec; self-review done | **User approves the plan and picks subagent or inline mode** |
| 3 | Isolate | `workflow:git-worktrees` | Clean worktree or branch from the right base; baseline tests pass | — |
| 4 | Build | `workflow:executing-plans` (each task via `testing:test-driven-development`; failures via `debugging:systematic-debugging`) | Every task done with evidence in the ledger; final branch review passed | — (rulings recorded, four stop conditions respected) |
| 5 | Verify | `testing:verification-before-completion` | Fresh run of the full check suite, output read, claims match evidence | — |
| 6 | Review | `code-quality:code-review`; answer findings with `code-quality:receiving-code-review` | No open critical or important finding | — |
| 7 | Finish | `workflow:finishing-a-branch` | Branch merged, PR opened, kept, or discarded as the user chose; own worktrees listed for cleanup | **User chooses the outcome; destructive cleanup needs explicit approval** |

## Shortcuts

- **Small, fully specified change** (everything that matters is in the request): stage 1 produces a short design inside the reply; stages 2-3 may collapse into a one-task plan on the current branch if the repository allows it. Stages 5-6 never collapse.
- **Spike requested**: build it in a throwaway location under stage 1, skip stages 2-7, and bring what it taught back to stage 1. Keeping spike code is a new request.
- **Work spans several domains or repositories**: stop at stage 1 and split it into one spec each, plus a short `docs/transversal/specs/ROADMAP.md` with their order and dependencies. Run this workflow once per spec.

## Status line

At every stage change, tell the user in one line: the stage you finished, its evidence (file path, test result), and the next stage with its gate.

## Pausing

If the session must end mid-way, use `workflow:handoff`; the stage table above is the first thing the handoff records.
