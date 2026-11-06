---
name: handoff
description: Use when work must pause and be resumed by another session, another agent or another person - the user says "handoff", "pass the baton", "document where we stopped", "I'll pause here", the context window is nearly full, a long session is ending, or before switching machine, branch or owner. Also use to resume from an existing handoff document.
license: MIT
metadata:
  domain: workflow
  status: experimental
---

# Handoff

Write a document that lets a cold reader (a new session, another agent, a colleague) **resume the work without re-deriving anything**. A handoff is not a summary of what happened; it is the next concrete step plus the minimum context to take it with confidence.

## Principle

The reader has none of your memory, only what you write. Prefer verifiable facts and concrete actions over narrative: exact file paths, commit SHAs, commands ready to paste, real function names. "Adjust the auth" fails; "edit `packages/core/src/middleware.ts:27` to redirect to `/` instead of `/dashboard`" works.

Always separate **done and verified**, **done but not verified**, and **pending**. The most expensive lie in a handoff is saying something works without having run it.

Do not duplicate what other artifacts already record (specs, plans, ADRs, issues, commits, diffs): link them by path or URL. Redact secrets, credentials and personal data.

## 1. Collect the real state

Gather live state before writing; do not trust memory alone. For every repository involved:

```bash
git -C <repo> rev-parse --abbrev-ref HEAD
git -C <repo> status --short
git -C <repo> log --oneline -15
git -C <repo> diff --stat
```

Also collect: background jobs (builds, deploys, test runs) and where their logs are; the session's task list (done, in progress); worktrees you created and their state; and anything the project's memory or notes already record, so you do not duplicate it.

Never invent SHAs or statuses. If a test was not run, the handoff says "not tested".

## 2. Write the document

Use [`templates/handoff.md`](templates/handoff.md). Cut sections that do not apply: a short, true handoff beats a full one with placeholders. The **TL;DR** and **Where I stopped** sections are mandatory. Write in the language the user is working in.

Content rules:

- **Next steps** are imperative and targeted: "run X", "edit Y:line", "confirm Z with the user". Never a bare "improve", "review", "adjust".
- Record the context that is *not* in the repository: the why, the next step, the trap.
- Mark assumptions as assumptions.
- Add a **Suggested skills** line naming the skills the next session should load.
- If the user said what the next session is for, tailor the document to that.

## 3. Save and report

- Inside a repository: `docs/handoffs/YYYY-MM-DD-HHMM-<slug>.md` in the main repository of the work (get the time with `date +%Y-%m-%d-%H%M`; slug is 2-4 kebab-case words), unless the repository's `AGENTS.md` says otherwise.
- Outside a repository: `HANDOFF-<slug>.md` in the current working directory.
- The user's preferred location always wins.

Then show the user the file path plus the TL;DR and next steps inline, and ask whether to adjust anything.

## Resuming from a handoff

1. Read the handoff, then every artifact it links.
2. Re-collect the live state (step 1) and compare it with the document. Report any drift (new commits, a different branch, a finished or failed background job) before acting.
3. Load the suggested skills, then start from **Where I stopped**.

## Handoffs and memory

A handoff is the state of *this* pass (short-lived, specific); project memory holds what stays true across sessions (durable, general). If you notice a durable fact while writing a handoff, such as an architecture decision or a user preference, suggest recording it in memory, and keep the two in separate files.
