---
name: health-informatics
description: "Use when designing or reviewing EHR/EMR systems, health-data interoperability, clinician workflows or clinical decision-support software architecture and validation."
license: MIT
metadata:
  domain: healthcare
  status: experimental
---
# Health informatics

## Define intended use and authority
Record users, clinical setting, software function, jurisdiction, data class, clinical owner and authorized processing environment. A catalogue skill is not a validated clinical system or a regulatory determination.

## Engineering workflow
1. Map the encounter and data lifecycle: capture, verification, correction, professional sign-off, addendum, exchange and retention. Keep decision authority explicit.
2. Declare the interoperability version and implementation guide, terminology versions, identifiers, units, timestamps and provenance. Validate both schema and domain meaning; FHIR conformance does not establish clinical safety.
3. Use synthetic fixtures for development. Keep identifiers, raw records and secrets out of prompts, logs, URLs and browser storage. Minimize data and apply tenant/facility authorization and an appropriate audit trail.
4. Separate clinician-authored rules from model suggestions. Model missing, stale, conflicting or unavailable data explicitly; a technical error must not silently become a reassuring clinical result.
5. Plan validation against the intended population and workflow, including false positives/negatives, subgroup effects, usability, alert fatigue, concurrency and sign-off/addendum integrity. Coverage or a claim of zero missed alerts is not proof of safety.
6. Review changes with the accountable clinical, privacy/security and regulatory owners before use affecting care. Production writes and integrations require specific authorization.

## Handoff
An intended-use statement, data/interop contract, risk and validation plan, evidence log and human approval boundary. Use healthcare:clinical-evidence for evidence synthesis and healthcare:clinical-documentation for drafting supplied facts. Biomedical research analysis remains in science. Current external references: [HL7 FHIR R4](https://hl7.org/fhir/R4/overview.html), [WHO health-AI guidance](https://www.who.int/publications/i/item/9789240084759) and [FDA CDS guidance, January 2026](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-decision-support-software). Confirm the required FHIR version/profile and applicable local requirements separately.

An original, empty [review manifest](assets/review-manifest.example.json) records evidence and approval boundaries without patient data. It grants no authorization.

## References

Load only what the task needs:

- [`references/healthcare-emr-patterns.md`](references/healthcare-emr-patterns.md) — Reviewed adaptation: healthcare-emr-patterns; version and approval assumptions are explicit.
- [`references/healthcare-reviewer.md`](references/healthcare-reviewer.md) — Reviewed adaptation: healthcare-reviewer; version and approval assumptions are explicit.
