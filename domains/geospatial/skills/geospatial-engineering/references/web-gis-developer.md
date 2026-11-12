# Web GIS Developer — reviewed procedure

Adapted by OpenDigital from `msitarzewski/agency-agents` at `b859c51`, `gis/gis-web-gis-developer.md#critical-rules-you-must-follow,your-process`. See this domain’s PROVENANCE.yaml. This is a reviewed procedure, not an installed upstream tool or a validated runtime example.

Specify datasets, audience, permitted access, interactions, devices and freshness. Choose payload format and map library from measured volume and queries: bounded GeoJSON can be appropriate, while larger workloads may need tiles, filtering, paging or clustering.

Provide clear loading, partial-data and error states, attribution and readable legends. Test feature identification, permissions, zoom changes, mobile input, slow networks and memory use. Coordinate cache invalidation with source updates. Pin library versions and verify browser support; a provider/library list is not a universal performance ranking.
