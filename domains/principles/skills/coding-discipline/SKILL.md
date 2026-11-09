---
name: coding-discipline
description: Use on any task that writes, fixes or refactors code. Makes the smallest change that fully solves the task, surfaces assumptions before coding, keeps diffs surgical, and defines a verifiable success check. Also use when the user asks for the simplest solution, mentions YAGNI, or complains about over-engineering or bloat.
license: MIT
metadata:
  domain: principles
  status: experimental
---

# Coding discipline

Solve the whole problem with the least new code, and leave a diff a reviewer can trust line by line.

## 1. Think before coding

- State your assumptions. If the request has more than one reasonable reading, name them and ask, or pick the smallest and say so.
- If a simpler approach exists than the one requested, say it before building.
- If something is unclear, stop and name exactly what is unclear. Do not guess silently.

## 2. Map the scope, not the wishlist

Read the task and the code it touches. List every place the change must reach: callers, tests, fixtures, config, exports, docs that describe the behaviour. Check what the change could break: data it could destroy or expose, callers that stop working. That list is the scope. Features nobody asked for are not.

## 3. Take the first option that fully works

1. **Does it need to exist?** Skip options, flags and flexibility nobody asked for; name what you skipped in one line.
2. **Already in this codebase?** Reuse the helper, component or pattern, the way the surrounding code uses it.
3. **Standard library or platform feature?** Use it, unless the project has its own equivalent.
4. **An installed dependency?** Use it. Never add a dependency for a few lines.
5. **One readable line?** Write one line. A one-liner that needs decoding is not short.
6. **Otherwise** write the minimum code that works.

Between options of equal size, take the one that is correct on edge cases.

## 4. Keep the change surgical

- Touch only what the task requires. Match the existing style, layering and conventions, even if you would do it differently.
- Do not refactor, reformat, rename or re-comment code you did not need to change. If you notice something worth fixing outside scope, mention it as a follow-up.
- No abstraction, wrapper, config or "for later" code nobody asked for. Three similar lines beat a premature helper.
- Remove imports, variables and functions that *your* change made unused. Leave pre-existing dead code alone unless asked.
- Bug fix: find every caller of the code you touch, then fix the root cause once, in the shared place.
- Code you move or merge keeps its error handling and validation.
- Comment only the *why* the code cannot show, in one line.

## 5. Never cut

Validation at trust boundaries, error handling that prevents data loss, security, accessibility, and anything the user explicitly asked for. Being lazy about the solution never means being lazy about finishing it: update every caller, test and fixture the change breaks.

## 6. Make success verifiable

Turn the task into a check before you start:

- "Add validation" → tests for invalid inputs, then make them pass.
- "Fix the bug" → a test that reproduces it, then make it pass.
- "Refactor X" → tests pass before and after.

New non-trivial logic (a branch, loop, parser, anything touching money or security) leaves at least one small test. Trivial changes need none.

For multi-step work, state a short plan where each step has its check:

```
1. <step> → verify: <check>
2. <step> → verify: <check>
```

## 7. Record deliberate shortcuts

A shortcut with a known limit gets a one-line comment in this exact form, so it can be listed later:

```
// shortcut: <the limit>, <when to upgrade>
```

## 8. Before you hand back

Walk every changed line and ask: *does the task require this line?* If the honest answer is "no, but it is nicer", delete it. Then end your reply with one or two lines: what you skipped or did not verify, and any risk the user must know.

## Further references

Guides merged from github/awesome-copilot; load only what the task needs:

- [`references/comments.md`](references/comments.md)
