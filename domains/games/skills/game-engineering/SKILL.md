---
name: game-engineering
description: "Use when implementing and profiling a game runtime: scenes, entity state, save systems, engine integration, game audio, networking or a packaged game build."
license: MIT
metadata:
  domain: games
  status: experimental
---
# Game engineering

## Fix the target
Identify engine and exact version, language, target hardware, build configuration, input devices and multiplayer topology. Read the target repository before selecting an API. Source examples are design references, not a claim that code compiles against every engine version.

## Implement a vertical slice
1. Define scene/entity ownership, lifecycle, state transitions and save-data versioning. Keep gameplay rules testable outside rendering and editor state where practical.
2. Choose the smallest composition model that fits the engine. Establish explicit initialization, subscriptions, cleanup and asset lifetime; avoid hidden cross-scene dependencies.
3. For multiplayer, distinguish server authority, client presentation and prediction. Validate identity, authorization, rate, bounds and state transitions at the authoritative boundary.
4. Set CPU, GPU, memory, storage, networking and audio budgets from measured target hardware. Profile a representative packaged build before changing architecture for presumed performance.
5. For assets and large worlds, define import validation, streaming/LOD policy, collision and persistence requirements. Authorize destructive editor operations separately.
6. Test scene reload, save/load migration, disconnect/rejoin, latency/loss, long sessions and resource cleanup. Record tools, versions, fixture, build and measurement.

## Handoff
Deliver the change, reproduction scene, tests, profile comparison and known target limitations. General code review belongs to code-quality:code-review; use security:security-audit for security review. Engine-specific references below do not mandate a single engine, middleware product or programming style.

## References

Load only what the task needs:

- [`references/unity-architect.md`](references/unity-architect.md) — Reviewed adaptation: Unity Architect; version and approval assumptions are explicit.
- [`references/godot-gameplay-scripter.md`](references/godot-gameplay-scripter.md) — Reviewed adaptation: Godot Gameplay Scripter; version and approval assumptions are explicit.
- [`references/godot-multiplayer-engineer.md`](references/godot-multiplayer-engineer.md) — Reviewed adaptation: Godot Multiplayer Engineer; version and approval assumptions are explicit.
- [`references/unreal-systems-engineer.md`](references/unreal-systems-engineer.md) — Reviewed adaptation: Unreal Systems Engineer; version and approval assumptions are explicit.
- [`references/unreal-world-builder.md`](references/unreal-world-builder.md) — Reviewed adaptation: Unreal World Builder; version and approval assumptions are explicit.
- [`references/game-audio-engineer.md`](references/game-audio-engineer.md) — Reviewed adaptation: Game Audio Engineer; version and approval assumptions are explicit.
- [`references/roblox-systems-scripter.md`](references/roblox-systems-scripter.md) — Reviewed adaptation: Roblox Systems Scripter; version and approval assumptions are explicit.
