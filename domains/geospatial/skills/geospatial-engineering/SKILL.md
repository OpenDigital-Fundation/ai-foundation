---
name: geospatial-engineering
description: "Use when building GIS data pipelines, spatial services, map applications, BIM/GIS integration, geoprocessing tools or scalable map delivery."
license: MIT
metadata:
  domain: geospatial
  status: experimental
---
# Geospatial engineering

## Contract first
Inventory source/target CRS, vertical datum, schema, geometry types, resolution, temporal semantics, licences, access rights and delivery format. Identify required clients, query patterns, update frequency and acceptance tolerances.

## Build the spatial product
1. Preserve inputs and define a read → transform → validate → versioned-output pipeline. Make paths, transformations and credentials explicit configuration.
2. Validate geometry, attributes, feature identity, extent and row counts at each boundary. Retain lineage, rejected features and repair decisions.
3. Choose storage and indexes from actual spatial queries and volume. Benchmark bounding-box filtering, exact predicates, simplification and pagination with representative data.
4. For maps, choose GeoJSON, vector/raster tiles or services from measured payload and interaction requirements. Define loading/error states, attribution, permissions, zoom-dependent detail and cache invalidation.
5. For BIM/3D integration, verify units, axis conventions, origin, vertical reference and level-of-detail mapping with known control objects.
6. Test empty and malformed layers, large extents, antimeridian cases, concurrent updates, permission failures and mobile/slow-network delivery.

## Handoff
Deliver schema/CRS contract, transformation configuration, QA evidence, service or application build, operational ownership and rollback. Generic ETL, deployment and reliability remain in data and platform; this domain owns their spatial constraints.

## References

Load only what the task needs:

- [`references/spatial-data-engineer.md`](references/spatial-data-engineer.md) — Reviewed adaptation: Spatial Data Engineer; version and approval assumptions are explicit.
- [`references/web-gis-developer.md`](references/web-gis-developer.md) — Reviewed adaptation: Web GIS Developer; version and approval assumptions are explicit.
- [`references/geoprocessing-specialist.md`](references/geoprocessing-specialist.md) — Reviewed adaptation: Geoprocessing Specialist; version and approval assumptions are explicit.
- [`references/bim-gis-specialist.md`](references/bim-gis-specialist.md) — Reviewed adaptation: BIM/GIS Specialist; version and approval assumptions are explicit.
- [`references/3d-scene-developer.md`](references/3d-scene-developer.md) — Reviewed adaptation: 3D & Scene Developer; version and approval assumptions are explicit.
