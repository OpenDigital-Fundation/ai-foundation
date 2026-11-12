---
name: clinical-documentation
description: "Use when drafting or checking clinical notes, structured reports, handoffs or documentation of plans already supplied by a qualified clinician, with field-level traceability and professional review."
license: MIT
metadata:
  domain: healthcare
  status: experimental
---
# Clinical documentation

## Input gate
Confirm purpose, requester authority, minimum necessary facts, privacy-reviewed data class and responsible reviewer. Prefer synthetic or documented de-identified structured facts; do not take unreviewed raw patient narratives or send clinical content to remote services by default.

## Draft from facts, not plausibility
1. Build a source-fact manifest: fact ID, source locator, date, units, verification state and reviewer role. A hash is integrity metadata, not de-identification.
2. Select the requested clinical structure, such as an encounter note, handoff or report scaffold. A manuscript or case-report publication uses science:scientific-writing for writing conventions.
3. Populate only facts and professional assessments/decisions explicitly supplied and verified. Preserve uncertainty, negation, dates and units. Missing content stays missing; do not infer diagnosis, stage, treatment, dose or follow-up interval.
4. Keep draft and source record separate. Check internal consistency, attribution, duplicate facts and conflicts without silently reconciling them. Preserve the clinician's intended meaning.
5. For a supplied treatment plan, transcribe only the authorized decisions and ownership. Do not generate options, check suitability or invent monitoring thresholds.
6. Maintain a separate review manifest for clinical, privacy, statistical or regulatory checks as applicable. Operational drafts remain clearly drafts; do not sign, file, amend a live chart or submit on another person's behalf.

## Deliverable
The requested note/report, fact-ID map, unresolved conflicts and named approval boundary. For manuscripts, keep project status and pending checks in the review record rather than the work's prose. This workflow formats and checks documentation; it does not establish clinical appropriateness or regulatory compliance.

An original, empty [review manifest](assets/review-manifest.example.json) records evidence and approval boundaries without patient data. It grants no authorization.

## References

Load only what the task needs:

- [`references/clinical-reports.md`](references/clinical-reports.md) — Reviewed adaptation: clinical-reports; version and approval assumptions are explicit.
- [`references/treatment-plans.md`](references/treatment-plans.md) — Reviewed adaptation: treatment-plans; version and approval assumptions are explicit.
