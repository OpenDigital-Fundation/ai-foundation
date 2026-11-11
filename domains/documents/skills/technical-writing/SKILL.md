---
name: technical-writing
description: "Use when writing or updating developer documentation: READMEs, API references, guides, tutorials, runbooks, architecture overviews or code maps, and keeping docs in sync after code changes."
license: MIT
metadata:
  domain: documents
  status: experimental
---
# Technical writing

Write documentation that lets a reader succeed at a task without asking anyone.

## 1. Know the reader and the task
Who reads it (new user, integrator, operator, maintainer) and what they are trying to do. Pick the type: tutorial (learn), how-to (do), reference (look up), explanation (understand).

## 2. Structure
Lead with the outcome and prerequisites; one task per section; numbered steps with the exact commands and expected output; examples that run.

## 3. Write
Short sentences, active voice, consistent terms (the project glossary wins), no marketing language. Every code sample is copied from something that was run.

## 4. Verify
Follow the doc from a clean environment; fix every step that failed or needed knowledge it did not give.

## 5. Keep it current
Update docs in the same change as the code they describe; find stale docs by searching for changed names; record breaking changes in the changelog.

## References

Load only what the task needs:

- [`references/role-guide.md`](references/role-guide.md) — the role profile this skill was distilled from: mission, critical rules, deliverable templates and examples
- [`references/keeping-docs-current.md`](references/keeping-docs-current.md) — covers Documentation & Codemap Specialist; Architecture; Key Modules; Data Flow
- [`references/documentation-quality/README.md`](references/documentation-quality/README.md) — covers Technical Content Evaluator; REQUIRED WORKFLOW; EDITORIAL STANDARDS; REVIEW PROCESS
- [`references/derived-guides.md`](references/derived-guides.md) — sections merged from other collections where this skill had no equivalent: Converting Markdown to HTML; The Seven Sweeps Framework; Evidence Standards
