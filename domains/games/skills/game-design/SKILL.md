---
name: game-design
description: "Use when designing game mechanics, player loops, progression, economies, narrative systems or levels and planning playtests. Use game-engineering for engine implementation."
license: MIT
metadata:
  domain: games
  status: experimental
---
# Game design

## Establish the playable question
Record audience, platform, session length, accessibility constraints, design pillars and the intended player decision. Identify whether the task concerns mechanics, progression, economy, narrative or level flow; do not replace a design question with engine code.

## Build and test
1. Draw the core loop as player action → feedback → state change → next decision. Define win, loss, retry and stopping conditions.
2. Specify each mechanic with inputs, rules, state, feedback, edge cases and acceptance examples. Separate cosmetic rewards from competitive advantage.
3. For progression and currencies, map sources, sinks, pacing and exchange rules. Simulate newcomer, typical and extreme behaviours; record assumptions instead of treating example numbers as calibrated defaults.
4. For levels, sketch traversal, landmarks, encounter pacing and readable affordances. For narrative, track prerequisites, branch state and re-entry behaviour.
5. Prototype the riskiest interaction with the smallest playable slice. Observe consenting playtesters; separate observed behaviour from preference and interpretation.
6. Change one design hypothesis, repeat the relevant playtest and retain the result, including null or adverse findings.

## Deliverable
A versioned mechanic/level brief, state or economy model, prototype scope, playtest script, observations and the next falsifiable design change. Do not use manipulative monetisation or fabricated retention results. Route implementation to games:game-engineering, general visual assets to creative-media and interface conformance to accessibility.

## References

Load only what the task needs:

- [`references/game-designer.md`](references/game-designer.md) — Reviewed adaptation: Game Designer; version and approval assumptions are explicit.
- [`references/economy-designer.md`](references/economy-designer.md) — Reviewed adaptation: Economy Designer; version and approval assumptions are explicit.
- [`references/level-designer.md`](references/level-designer.md) — Reviewed adaptation: Level Designer; version and approval assumptions are explicit.
- [`references/narrative-designer.md`](references/narrative-designer.md) — Reviewed adaptation: Narrative Designer; version and approval assumptions are explicit.
