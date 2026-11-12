# Godot Gameplay Scripter — reviewed procedure

Adapted by OpenDigital from `msitarzewski/agency-agents` at `b859c51`, `game-development/godot/godot-gameplay-scripter.md#critical-rules-you-must-follow,your-workflow-process`. See this domain’s PROVENANCE.yaml. This is a reviewed procedure, not an installed upstream tool or a validated runtime example.

For the pinned Godot version, define reusable scene boundaries, data resources, signals and ownership. Use type information where it improves correctness and tooling; do not equate @tool with a language type-checking mode or impose engine-version-specific signal syntax without checking it.

Acquire node references at a valid lifecycle phase, document dependencies and release subscriptions/resources with their actual lifetime. Keep autoloads limited to intentional cross-scene state. Test each scene independently, missing nodes, reloads and repeated initialization. Deliver a small scene/state diagram and editor/runtime checks for the installed version.
