# Unity Architect — reviewed procedure

Adapted by OpenDigital from `msitarzewski/agency-agents` at `b859c51`, `game-development/unity/unity-architect.md#critical-rules-you-must-follow,your-workflow-process`. See this domain’s PROVENANCE.yaml. This is a reviewed procedure, not an installed upstream tool or a validated runtime example.

Choose the architecture for the project's pinned Unity version and target, after inspecting the existing scene, prefab and asset workflow. Define component responsibilities, initialization order, ownership and cleanup; use data assets or services where they remove coupling rather than mandating a pattern everywhere.

Keep gameplay rules testable and avoid hidden global-state dependencies. Profile representative player builds before introducing ECS, pooling, async loading or editor tooling for performance. Check scene transitions, duplicate initialization, subscriptions, object lifetime and save compatibility. Document editor-only assumptions and validate on the lowest supported target.
