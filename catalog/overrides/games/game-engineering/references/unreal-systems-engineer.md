# Unreal Systems Engineer — reviewed procedure

Adapted by OpenDigital from `msitarzewski/agency-agents` at `b859c51`, `game-development/unreal-engine/unreal-systems-engineer.md#critical-rules-you-must-follow,your-workflow-process`. See this domain’s PROVENANCE.yaml. This is a reviewed procedure, not an installed upstream tool or a validated runtime example.

Record engine version, platform, module boundaries and the intended C++/Blueprint division. Keep designer-facing interfaces clear and move work between layers according to measured cost and maintainability, not a blanket rule that every Tick must be C++.

Choose UObject ownership/reference types deliberately for garbage collection and lifetime; not every raw pointer has the same ownership role. Verify reflection, modules, gameplay tags and ability-system integration in the target project. Test packaged builds, replication, object destruction and upgrade compatibility. Treat Nanite/Lumen capabilities and numeric limits as version-specific facts to verify, not universal constraints.
