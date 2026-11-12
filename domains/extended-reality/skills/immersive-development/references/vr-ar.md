# vr-ar — reviewed procedure

Adapted by OpenDigital from `davila7/claude-code-templates` at `bf9b0b4`, `cli-tool/components/skills/creative-design/game-development/vr-ar/SKILL.md#2-comfort-principles,4-interaction-principles,5-spatial-design,6-anti-patterns`. See this domain’s PROVENANCE.yaml. This is a reviewed procedure, not an installed upstream tool or a validated runtime example.

Select runtime/device and supported input modes before designing interaction. Define reference spaces, transforms, physical scale and tracking-loss behaviour explicitly. Use reachable controls, legible depth/size, cancellation and alternatives to a single input modality.

Offer appropriate comfort options for seated, standing or room-scale use and avoid unintended camera motion. Derive frame-time and thermal budgets from the actual device/runtime; neither a universal 90-FPS target nor a locomotion pattern guarantees comfort. Validate performance, accessibility and comfort with suitable participants in a safe setup. Keep a non-immersive fallback where the product requires it.

For browser integration, consult the [dated WebXR Device API candidate draft](https://www.w3.org/TR/2026/CRD-webxr-20261109/) and the implemented feature set; draft status does not imply universal browser support.
