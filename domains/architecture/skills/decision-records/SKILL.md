---
name: decision-records
description: Use when a significant technical decision is made or needs recording (architecture shape, a technology with lock-in, a boundary, a deliberate deviation from the obvious path, a rejected alternative someone will propose again), when the user asks for an ADR, or when existing ADRs must be read, superseded or indexed.
license: MIT
metadata:
  domain: architecture
  status: experimental
---

# Decision records

Record **that** a decision was made and **why**, so nobody re-litigates it and nobody "fixes" something deliberate. One decision per file.

## When a decision deserves an ADR

All three must be true:

1. **Hard to reverse:** changing your mind later costs real time or money.
2. **Surprising without context:** a future reader will wonder why it was done this way.
3. **A real trade-off:** there were genuine alternatives and one was chosen for specific reasons.

Typical cases: architectural shape (monorepo, event-sourced write model), integration patterns between contexts, technologies with lock-in (database, message bus, auth provider, deployment target), ownership and boundary decisions (including the explicit "no"s), deliberate deviations from the obvious path, constraints invisible in the code, and non-obvious rejected alternatives.

**Signals in conversation:** "we chose X over Y because", "let's not use Z", "we'll go with", "the trade-off is", a constraint from compliance or a partner contract. When you hear one, offer to record it; do not write ADRs nobody asked for.

## Where ADRs live

1. Follow the layout the repository already uses (its `AGENTS.md`, an existing `docs/adr/`, or per-context `docs/adr/` folders listed in `GLOSSARY-MAP.md`).
2. With no existing layout, use `docs/<domain>/adr/YYYY-MM-DD-<slug>.md` (cross-domain decisions in `docs/transversal/adr/`) with status and date in the header. Unnumbered names avoid number collisions between parallel branches; ordering comes from the date in the file name.
3. If the repository already numbers ADRs (`0007-slug.md`), keep numbering: scan for the highest number and add one.

Create the directory only when the first ADR is written.

## Format

Start minimal; add sections only when they carry information. See [ADR-FORMAT.md](ADR-FORMAT.md) for the one-paragraph form and [templates/adr.md](templates/adr.md) for the full form:

- **Title** — the decision, stated as a decision ("Use Postgres advisory locks for job claiming").
- **Status** — proposed | accepted | deprecated | superseded by `<path>`; **Date**; **Domain**.
- **Context** — the forces and constraints, in plain words.
- **Decision** — what was chosen.
- **Alternatives considered** — only those worth remembering, with why they lost.
- **Consequences** — what becomes easier, harder, or riskier.

## Lifecycle

- New ADRs start **proposed**; they become **accepted** when the people who own the decision agree.
- Never edit an accepted ADR's decision. To change it, write a new ADR and set the old one to `superseded by <path>`.
- Keep an index (`README.md` next to the ADRs): title, status, date, one-line summary, link.

## Reading ADRs

Before proposing a change in an area, read its ADRs. If your proposal contradicts one, say so explicitly and only push when the friction is real enough to reopen the decision.

## Further references

Guides merged from github/awesome-copilot; load only what the task needs:

- [`references/decision-templates.md`](references/decision-templates.md)
