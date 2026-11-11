---
name: scientific-writing
description: "Use when writing or reviewing scientific work: manuscripts and reports in IMRaD or journal formats, peer-review reports, grant proposals, venue and journal templates, posters, research talks and publication-quality figures."
license: MIT
metadata:
  domain: science
  status: experimental
---
# Scientific writing

Communicate research accurately, in the venue's format, with figures that do not mislead.

## Procedure

1. **Fix the claim and audience:** one-sentence main finding, the evidence for it, the venue and its requirements (length, structure, reporting guideline such as CONSORT, PRISMA or ARRIVE).
2. **Outline from evidence:** each result paragraph points to a figure, table or analysis that exists. Never invent data, statistics or references; mark missing evidence instead.
3. **Write plainly:** define terms once, keep tense and units consistent, separate results from interpretation, state limitations.
4. **Make figures honest:** appropriate chart type, labelled axes with units, error bars defined, colour-blind-safe palettes, no truncated axes that exaggerate effects.
5. **Review before submission:** check claims against results, numbers against tables, references against sources (`research:literature-review`), and the venue checklist.
6. **Peer review:** summarise the contribution, separate major from minor issues, tie each issue to evidence, and keep the tone constructive.

## Working rules

- **Pick one guide.** Load only the reference for the tool the task uses (list below). If two tools fit, say why you chose one.
- **Pin and record versions** of every library, model, database release and reference genome or dataset used; results depend on them.
- **Never fabricate data, results, identifiers or citations.** If a database query, file or run is unavailable, say so and stop at that step.
- **Run locally and boundedly.** Inspect inputs (shape, units, missing values, coordinate system, identifiers) before any transform; avoid jobs whose cost or duration you cannot estimate; ask before using paid services or cloud resources.
- **Validate before reporting:** sanity checks, controls, known reference values, or a re-run on a subset.
- **Report** the question, inputs (with versions and provenance), method and parameters, results with uncertainty, checks performed, and limitations. Keep scripts and seeds so the analysis can be reproduced.

Further detail files of the merged guides:

- [`references/research-grants/references/README.md`](references/research-grants/references/README.md)
- [`references/latex-posters/references/README.md`](references/latex-posters/references/README.md)

## External publisher templates

The Elsevier elsarticle bibliography styles and template files declare LPPL rather than the collection's MIT licence. Those six files are not bundled. Obtain the official package from its publisher or TeX distribution and review its licence before use; do not substitute the collection's licence. The remaining venue guidance and permissive scaffolds are available below.

## References

Load only what the task needs:

- `references/scientific-writing/` — Drafts, revises, and audits scientific manuscripts or reports with explicit evidence provenance, reporting-guideline coverage, authorship accountability, confidentiality controls, 
- `references/peer-review/` — Prepares evidence-bounded, constructive peer-review drafts and structured manuscript assessments. Supports authorized review of scientific manuscripts, protocols, preprints, or res
- `references/venue-templates/` — Prepares journal manuscripts, conference papers, research posters, and grant documents using venue-specific formatting guidance and bundled LaTeX scaffolds. Supports selecting an o
- `references/research-grants/` — Supports research proposal preparation and review for NSF, NIH, DOE, DARPA, and Taiwan NSTC, including opportunity-specific requirements, aims, review criteria, budgets, broader im
- `references/latex-posters/` — Creates research posters in LaTeX using beamerposter, tikzposter, or baposter. Use for conference posters, academic presentations, multi-column scientific layouts, figure integrati
- `references/pptx-posters/` — Creates and audits editable scientific posters in macro-free PowerPoint (.pptx) from author-approved local content and assets. Used when the requested deliverable is a PowerPoint r
- `references/scientific-slides/` — Builds slide decks and presentations for research talks. Used for making PowerPoint slides, conference presentations, seminar talks, research presentations, thesis defense slides, 
- `references/scientific-visualization/` — Creates and audits truthful, accessible, publication-ready scientific figures with Matplotlib, Seaborn, or Plotly. Use it for figure design, multi-panel layouts, uncertainty and mi
- `references/matplotlib/` — Creates and customizes scientific plots with Matplotlib. Used for fine-grained control over plot elements, novel plot types, and scientific workflows. Export to PNG/PDF/SVG for pub
- `references/seaborn/` — Creates Seaborn statistical visualizations with pandas integration for distributions, relationships, categorical comparisons, regression displays, pair plots, and heatmaps. Support
- `references/scholar-evaluation/` — Provides qualitative-first, evidence-traceable developmental review of scholarly works and audit low-stakes research-assessment rubrics with optional local quality controls. Never 
