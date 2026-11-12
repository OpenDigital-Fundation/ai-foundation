# Geoprocessing Specialist — reviewed procedure

Adapted by OpenDigital from `msitarzewski/agency-agents` at `b859c51`, `gis/gis-geoprocessing-specialist.md#critical-rules-you-must-follow,your-process`. See this domain’s PROVENANCE.yaml. This is a reviewed procedure, not an installed upstream tool or a validated runtime example.

Translate the manual spatial operation into an input/parameter/output contract with CRS, extent, resolution, optional dependencies and acceptance checks. Validate parameters and licences before processing. Keep workspace and environment settings explicit and restore/release acquired resources.

Write outputs separately and restrict cleanup to known generated scratch paths, with appropriate authorization. Test empty, invalid, large and interrupted inputs; provide progress and actionable errors. A toolbox or script wrapper must package the helpers it actually needs instead of pointing to files absent from the installed skill.
