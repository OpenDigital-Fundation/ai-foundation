# healthcare-emr-patterns — reviewed procedure

Adapted by OpenDigital from `affaan-m/ECC` at `b38be6a`, `skills/healthcare-emr-patterns/SKILL.md#patient-safety-first,single-page-encounter-flow,locked-encounter-pattern,ui-patterns-for-clinical-data,accessibility-for-healthcare,anti-patterns`. See this domain’s PROVENANCE.yaml. This is a reviewed procedure, not an installed upstream tool or a validated runtime example.

Map the encounter lifecycle and clinical owner's requirements before choosing a layout. Preserve source facts, authorization, timestamps, auditability and the relationship between signed records and subsequent addenda. A single-page layout is one option, not a universal clinical UI requirement.

Show units, provenance, missingness and stale/conflicting data clearly. Review alert priority, acknowledgement, override and failure behaviour with clinicians using validated specifications; do not invent thresholds or automatically calculate scores from this reference. Support accessible navigation and alternatives to colour-only meaning. Test concurrency and protected-record integrity without writing real patient data during development.
