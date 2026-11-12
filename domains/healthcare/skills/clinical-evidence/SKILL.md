---
name: clinical-evidence
description: "Use when a healthcare professional needs a source-backed clinical evidence brief, appraisal of a clinical claim or a documented evidence profile; not a patient-specific diagnosis or prescription."
license: MIT
metadata:
  domain: healthcare
  status: experimental
---
# Clinical evidence

## Bound the question
State the professional's question using population, intervention/exposure, comparator and outcomes where appropriate. Record setting, time horizon, exclusions and the intended decision role. Do not turn an evidence brief into a patient-specific recommendation.

## Evidence workflow
1. Search current authoritative guidance and primary research using public, non-identifying terms. Use research:literature-review for a systematic review or a broad search protocol.
2. Verify each source, publication date/version, study population, design, outcome definition, effect estimate, uncertainty and material limitations. Never invent a DOI, trial, statistic or guideline.
3. Separate source findings, internal observations, extrapolations and unsupported claims. Peer review or clinician sign-off alone does not license an unqualified effectiveness or regulatory claim.
4. Assess relevance and risk of bias; distinguish exploratory from confirmatory findings. For GRADE-style profiles, record judgments and rationale by outcome rather than deriving certainty from keywords or p-values.
5. Compare conflicting evidence, applicability and what remains unknown. The responsible professional decides how evidence applies to care; do not calculate patient-specific doses, triage or treatment choices.
6. Produce a concise brief with claim-to-source links, evidence date, applicability limits and reviewer roles. Keep process checklists outside manuscript prose when the output is a publication.

## Boundary
No raw patient data, undisclosed external uploads, autonomous clinical decisions or claims of clinical validation. Route urgent clinical matters through the user's established professional process. Statistical and study-design questions remain in science:experimental-design.

An original, empty [review manifest](assets/review-manifest.example.json) records evidence and approval boundaries without patient data. It grants no authorization.

## References

Load only what the task needs:

- [`references/clinical-evidence-agent.md`](references/clinical-evidence-agent.md) — Reviewed adaptation: Clinical Evidence Agent; version and approval assumptions are explicit.
- [`references/clinical-decision-support.md`](references/clinical-decision-support.md) — Reviewed adaptation: clinical-decision-support; version and approval assumptions are explicit.
