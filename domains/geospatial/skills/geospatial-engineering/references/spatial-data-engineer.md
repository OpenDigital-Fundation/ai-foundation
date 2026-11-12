# Spatial Data Engineer — reviewed procedure

Adapted by OpenDigital from `msitarzewski/agency-agents` at `b859c51`, `gis/gis-spatial-data-engineer.md#critical-rules-you-must-follow,your-process`. See this domain’s PROVENANCE.yaml. This is a reviewed procedure, not an installed upstream tool or a validated runtime example.

Declare source/target schema, CRS, datum, geometry, time semantics and update contract. Preserve originals and write versioned outputs. Parameterize paths and transformations; record row counts, extent, rejected records and lineage without leaking sensitive attributes.

Validate after each spatial transformation, including invalid/empty geometry, schema loss and coordinate shifts. Design idempotence and restart behaviour explicitly. Choose database/file/index formats from consumer queries and volume. Test representative edge cases using authorized or synthetic data; generic pipeline/deployment practices remain owned by data and platform.
