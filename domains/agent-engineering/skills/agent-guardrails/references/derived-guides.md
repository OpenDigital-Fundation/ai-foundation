# Agent guardrails — derived guides

Part of `agent-engineering:agent-guardrails`.

## Session Guard

<!-- source: wshobson/agents plugins/skill-forge-essentials/skills/session-guard/SKILL.md#context-anchoring-anti-compaction -->

### Context Anchoring (anti-compaction)

When compaction has occurred (sudden loss of earlier context, or after /compact):

1. RE-READ the project's rules file immediately
2. RECITE the 3-5 critical rules aloud in your response
3. VERIFY your planned next action matches those rules before executing
4. If uncertain about ANY prior decision, RE-READ the source file - don't guess

#### What survives compaction:
- Most recent user messages (high priority)
- Currently-invoked skill body (capped at 5K tokens, oldest dropped first)
- Git status and project structure
- File contents read AFTER compaction

#### What gets LOST in compaction:
- Decisions made early in conversation
- Architectural rules stated only verbally (not in files)
- Context from tool outputs (file reads, command outputs)

#### Compaction-Safe Pattern
Keep critical instructions in FILES (CLAUDE.md, CONTEXT.md), NOT in conversation. If a rule matters, it must live in a file the agent can re-read - not in something agreed on earlier.
