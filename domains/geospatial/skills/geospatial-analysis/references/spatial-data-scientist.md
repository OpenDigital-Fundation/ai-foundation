# Spatial Data Scientist — reviewed procedure

Adapted by OpenDigital from `msitarzewski/agency-agents` at `b859c51`, `gis/gis-spatial-data-scientist.md#critical-rules-you-must-follow,your-process`. See this domain’s PROVENANCE.yaml. This is a reviewed procedure, not an installed upstream tool or a validated runtime example.

Specify spatial support, sampling, time range, outcome and exploratory versus confirmatory purpose. Examine spatial dependence, aggregation-boundary sensitivity and confounding. Non-spatial methods are not automatically invalid, but their assumptions must be assessed against the spatial structure.

Choose diagnostics and validation that prevent spatial/temporal leakage. Report uncertainty where justified by the method and data, and disclose limits rather than manufacturing confidence bounds. Compare alternative zoning/scales and holdouts. Deliver reproducible transformations, model/method assumptions, diagnostics, null findings and an interpretation that distinguishes association from causation.
