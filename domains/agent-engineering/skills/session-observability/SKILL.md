---
name: session-observability
description: 'Use when explicitly measuring selected agent sessions and skill/tool usage: scoped counts, tokens, latency and cost provenance, with an optional local Claude Code session pane. Not live Codex/Orca telemetry.'
license: MIT
---

# Session observability

## Select evidence and scope

Identify harness/version, selected sessions or explicit record paths, period/timezone, intended comparison and what data may be read. Do not discover all personal transcripts or enable a collector by default. For a quick current-context request, use agent-engineering:context-management and its native meter instead.

## Measure without overclaiming

1. Record whether each figure is harness-reported, counted from selected records, estimated from text/rates, or unavailable. Keep missing values distinct from zero.
2. Count unique requests and tool-use IDs; distinguish retries from repeated fragments of the same response. Attribute main/subagent events once. State whether totals are lifetime, since compaction, selected period or a current window.
3. Separate tool calls, Skill invocations and MCP calls. A skill discovered/installed/read is not necessarily invoked. Keep raw runtime identifiers; map a namespace/name to a catalog ID only when there is evidence, preserving unknowns.
4. Report input/output/cache categories and time units explicitly. Do not add cumulative context-window snapshots or interpret local byte counts as exact live tokens. Unobserved host work can make records incomplete.
5. Label prices with date/currency/rate source and scope. Preserve unknown model pricing and estimated coverage; list-price estimates do not represent a subscriber's charge. Do not fabricate per-skill billable cost when requests include several skills or shared context.
6. Compare matched tasks and sampling periods before ranking agents. Usage, latency and calls describe work; task success and skill quality require separate evaluations. Route controlled comparisons to agent-engineering:agent-evaluation and failure diagnosis to agent-engineering:agent-debugging.

## Optional Claude Code pane

Read [the local integration guide](assets/session-lens/README.md) before considering Session Lens. It explains runtime data access, local state, compatibility and exact opt-in loading. The native asset is not auto-enabled by this skill or by installing the domain. Its report/model and autocompact write actions are disabled. Do not launch a new agent, install globally or read private records just to show a sample.

## Output

Scope/denominator, period, source/coverage, descriptive counts by agent and skill, token/cost classification, unknowns and the next evidence needed. Use synthetic data for demonstrations and label it.
