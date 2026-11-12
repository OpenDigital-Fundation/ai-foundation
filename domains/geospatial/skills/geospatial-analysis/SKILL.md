---
name: geospatial-analysis
description: "Use when analysing geographic vector/raster data, selecting coordinate reference systems, making analytical maps, validating spatial accuracy or interpreting spatial statistics."
license: MIT
metadata:
  domain: geospatial
  status: experimental
---
# Geospatial analysis

## Define the spatial claim
Record question, study area, time range, spatial support, units, resolution, coordinate reference system (CRS), data licence and privacy constraints. Distinguish a descriptive map from a statistical or causal claim.

## Analytical workflow
1. Inspect schema, geometry, extent, timestamps, missingness, sampling and provenance. Verify coordinate meaning against control locations; a CRS label alone is not evidence.
2. Choose an appropriate working CRS and distance/area model. Assigning a CRS declares coordinate meaning; reprojecting transforms coordinates. Never confuse the two. Account for antimeridian and polar cases.
3. Check geometry validity and topology before joins, overlay or buffering. Document repairs, changed feature counts and precision; preserve originals.
4. For raster work, align CRS, resolution, extent, grid origin and nodata policy. Resampling changes information and must be recorded.
5. Examine spatial dependence, aggregation-boundary sensitivity and sampling bias. Use spatially appropriate validation; quantify uncertainty where the method supports it and disclose where it does not.
6. Produce a map with source/date, units, legend, appropriate scale and readable symbology. Validate against independent observations or checkpoints appropriate to the intended accuracy.

## Deliverable and boundary
Provide reproducible parameters, output layers, QA findings, map and interpretation limits. Existing GeoPandas guides remain owned by science:scientific-computing; reuse that installed pack for library details rather than creating a second copy here. GIS services and pipeline delivery belong to geospatial:geospatial-engineering.

## References

Load only what the task needs:

- [`references/gis-analyst.md`](references/gis-analyst.md) — Reviewed adaptation: GIS Analyst; version and approval assumptions are explicit.
- [`references/cartography-designer.md`](references/cartography-designer.md) — Reviewed adaptation: Cartography Designer; version and approval assumptions are explicit.
- [`references/spatial-data-scientist.md`](references/spatial-data-scientist.md) — Reviewed adaptation: Spatial Data Scientist; version and approval assumptions are explicit.
- [`references/gis-qa-engineer.md`](references/gis-qa-engineer.md) — Reviewed adaptation: GIS QA Engineer; version and approval assumptions are explicit.
- [`references/drone-reality-mapping-specialist.md`](references/drone-reality-mapping-specialist.md) — Reviewed adaptation: Drone/Reality Mapping Specialist; version and approval assumptions are explicit.
