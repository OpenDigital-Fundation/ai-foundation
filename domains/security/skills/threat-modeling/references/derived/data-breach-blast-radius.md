# Threat modeling — data breach blast radius

Part of `security:threat-modeling`. Adapted reference material; the owner procedure, project conventions, scope and authorization rules take precedence. Examples are not automatically executed.

<!-- source: github/awesome-copilot skills/data-breach-blast-radius/SKILL.md#execution-workflow -->

## Evidence-bounded exposure analysis

Use the agreed system/scope and a read-only view. Inventory sensitive fields, storage and cache locations, queues, exports, logs, backups, identities and relevant authorization boundaries. Do not open unrelated credentials or expand to every repository without a reason.

Trace ingestion, processing, storage and outbound flows. For each plausible exposure, record the entry point, actor permissions, reachable tenants/records, data fields, controls and the evidence supporting that path. A schema field or provider name alone does not establish exposure.

Use observed counts or an explicitly labelled scenario range. If the population, reachability or data completeness is unknown, report that gap; do not invent default user counts or attach arbitrary multipliers for health, minors or payment data. Separate sensitivity, likelihood and affected population rather than turning an uncalibrated product into a measured score.

Report an exposure map, bounded impact scenarios, confidence, missing evidence, and prioritized mitigations with verification criteria. Do not infer legal jurisdiction from a currency/domain or calculate statutory fines and deadlines from guessed categories; route those questions with supporting facts to qualified legal review.

Use any diagram renderer available in the approved environment; no named external tool is required. Never copy raw personal data or secrets into the report.
