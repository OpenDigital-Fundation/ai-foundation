# External language tools

Tools the language packs point to but this catalog does not vendor. Use them through their own CLI or extension.

| Tool | What it does | Licence | How to use it here |
|---|---|---|---|
| [react-doctor](https://github.com/millionco/react-doctor) | Scans React code for lint, accessibility, performance and correctness problems and explains each diagnostic | Modified MIT: use as AI training, fine-tuning **or evaluation** data, or reselling it as a hosted service, needs written permission from Million Software | Vendored as `languages:react-diagnostics` with its licence, and excluded from evals until written permission is granted |
| [godoctor](https://github.com/danicat/godoctor) | Go development MCP server and Gemini CLI extension: documentation lookup, code review and editing helpers for Go | Apache-2.0 | Install it as an MCP server or extension when working in Go; the Go pack (`languages:go`) covers idioms, tests and review without it |
| [Web Interface Guidelines](https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines) | Vercel's checklist for reviewing UI code (accessibility, focus, forms, motion, typography) | not declared | Read at the source when reviewing UI; `ui:visual-design` and `accessibility:wcag-accessibility` cover the same ground in this catalog |
