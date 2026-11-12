# GIS QA Engineer — reviewed procedure

Adapted by OpenDigital from `msitarzewski/agency-agents` at `b859c51`, `gis/gis-qa-engineer.md#critical-rules-you-must-follow,your-qa-process,qa-report-template`. See this domain’s PROVENANCE.yaml. This is a reviewed procedure, not an installed upstream tool or a validated runtime example.

Define acceptance checks before processing: CRS/coordinate plausibility, extent, schema, geometry/topology, feature identity, nulls, completeness, timestamps and provenance. Classify severity from the intended use and cite reproducible feature IDs or locations.

After transformations, verify counts and spatial relationships; assess positional accuracy against appropriate independent reference/control data. For services, check permissions, responses, rendering and representative load. Report pass, conditional pass, fail or not assessed with evidence and scope. Re-run failed checks after correction; a clean schema is not proof of geographic accuracy.
