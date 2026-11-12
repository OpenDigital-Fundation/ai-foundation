# Unreal World Builder — reviewed procedure

Adapted by OpenDigital from `msitarzewski/agency-agents` at `b859c51`, `game-development/unreal-engine/unreal-world-builder.md#critical-rules-you-must-follow,your-workflow-process`. See this domain’s PROVENANCE.yaml. This is a reviewed procedure, not an installed upstream tool or a validated runtime example.

Start from world scale, traversal speed, density and memory/streaming budgets on target hardware. Choose partition cells and loaded layers from measurements; do not inherit universal cell sizes, landscape-layer counts or HLOD distances from examples.

Define persistent gameplay state, dependencies across streamed regions and exclusion zones for procedural population. Validate terrain resolution/units using the installed engine's tools. Test maximum-speed traversal, boundary crossings, visibility, collisions, loading/unloading and save/reload. Rebuild generated streaming/HLOD assets when their inputs change and compare traces and visual results before approving the change.
