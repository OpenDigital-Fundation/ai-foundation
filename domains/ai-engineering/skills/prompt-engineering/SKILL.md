---
name: prompt-engineering
description: "Use when writing, testing or optimising prompts for an LLM feature: system prompts, few-shot examples, structured output, prompt evaluation sets, prompt caching for cost and latency, and deciding whether a regex or parser beats an LLM for structured text."
license: MIT
metadata:
  domain: ai-engineering
  status: experimental
---
# Prompt engineering

Treat prompts as code: specified, tested against cases, and changed one variable at a time.

## 1. Specify
The task, inputs, the exact output format, and what good looks like. Collect 20 or more realistic test inputs, including edge cases and adversarial ones.

## 2. Draft
Clear role and goal, the context the model needs, explicit constraints, a few varied examples when the format is subtle, and structured output (JSON schema or tool calls) when code consumes it. Put stable content first so it can be cached.

## 3. Evaluate
Run the test set; grade with code checks where possible and a versioned rubric (LLM-as-judge) otherwise. Record pass rate, cost and latency.

## 4. Iterate
Fix the failure categories one at a time; keep a changelog of prompt versions and their scores. Consider whether a parser, regex or smaller model solves part of the task more reliably.

## 5. Ship
Pin the model version, cache the static prefix, monitor quality on production samples, and rerun the evaluation before any model or prompt change. For the Claude API specifics, use `ai-engineering:claude-api`.

## References

Load only what the task needs:

- [`references/role-guide.md`](references/role-guide.md) — the role profile this skill was distilled from: mission, critical rules, deliverable templates and examples
- [`references/prompt-caching.md`](references/prompt-caching.md) — covers Prompt Caching Strategy
- [`references/regex-or-llm.md`](references/regex-or-llm.md) — covers Regex vs LLM for Structured Text Parsing
- [`references/prompt-design/README.md`](references/prompt-design/README.md) — covers Prompt Builder Instructions; Prompt Builder Researching Topic for Prompt Enhancement; Prompt Engineer; Guidelines
- `references/prompt-optimization/`
