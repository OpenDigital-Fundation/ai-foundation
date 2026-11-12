# 3D & Scene Developer — reviewed procedure

Adapted by OpenDigital from `msitarzewski/agency-agents` at `b859c51`, `gis/gis-3d-scene-developer.md#critical-rules-you-must-follow,your-process`. See this domain’s PROVENANCE.yaml. This is a reviewed procedure, not an installed upstream tool or a validated runtime example.

Define coordinate/reference systems, terrain/elevation semantics, units, source licences and target scene clients. Choose levels of detail, tiling, culling and streaming from measured workloads and target devices.

Check placement against known objects and validate transforms, vertical offsets, clipping and occlusion. Handle authentication, permission denial and expired access without exposing tokens or making private scenes public. Test rendering and query behaviour after export and on slow/mobile clients. Keep GIS 3D scene delivery separate from immersive input/comfort design in extended-reality.
