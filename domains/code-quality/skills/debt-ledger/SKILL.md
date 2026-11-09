---
name: debt-ledger
description: "Use when the user asks what was deferred, which shortcuts exist, or for a technical-debt ledger. Collects every `shortcut: <limit>, <when to upgrade>` comment (or a marker the user names) into one ranked ledger. Report only; changes nothing."
license: MIT
metadata:
  domain: code-quality
  status: experimental
---
Every deliberate shortcut is marked with a `shortcut:` comment naming
its ceiling and upgrade path (see principles:coding-discipline). This collects them into one ledger so a deferral
can't quietly become permanent.

## Scan

Grep the repo for comment markers, skipping `.git` and everything the
`.gitignore` files ignore (dependencies, build output, caches, in any stack):

`git grep --no-index --exclude-standard -nE '(#|//|/[*]) ?shortcut:'`  (add other comment prefixes if your stack uses them)

If the user names their own marker word (for example `TODO`), grep for that word instead.

Each hit is one ledger row. The comment prefix keeps prose that merely mentions
the convention out of the ledger. Skip hits that are not a deferral, like a note
about a keyboard shortcut.

## Output

One row per marker, grouped by file:

`<file>:<line>, <what was simplified>. ceiling: <the limit named>. upgrade: <the trigger to revisit>.`

The convention is `shortcut: <ceiling>, <upgrade path>`, so pull the ceiling
and the trigger straight from the comment. Want an owner per row too? add
`git blame -L<line>,<line>`.

Flag the rot risk: any marker comment that names no upgrade path or
trigger gets a `no-trigger` tag, those are the ones that silently rot.

End with `<N> markers, <M> with no trigger.` Nothing found: `No shortcut debt. Clean ledger.`

## Boundaries

Reads and reports only, changes nothing. To persist it, ask and it writes the
ledger to a file (e.g. `DEBT-LEDGER.md`). One-shot.

## Further references

Guides merged from github/awesome-copilot; load only what the task needs:

- [`references/remediation-planning.md`](references/remediation-planning.md)
