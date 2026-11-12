# Local session measurement pane

Private optional runtime of `agent-engineering:session-observability`, derived from neokn/session-lens 1.2.0 at commit 8067dc061bd89affd2893afdba9b34f2ca847346, MIT (see LICENSE). OpenDigital adaptation 1.2.0-opendigital.1.

This is a native Claude Code mod, not a cross-harness dashboard. It needs Claude Code 2.1.308 or later with function hooks/mods enabled and jq. A macOS Python kqueue watcher is optional; other platforms use its polling fallback. Host API compatibility can change; static validation does not demonstrate an interactive session.

Nothing in the Foundation domain plugin automatically loads this asset. After specific approval of local loading and its data scope, an operator can start a Claude Code session with `claude --plugin-dir /absolute/path/to/this/assets/session-lens` and invoke `/session-lens`. Starting a model session can incur usage; do not do this as a package-validation step. This package has no global installer and no floating marketplace dependency.

## Data and effects to review before loading

The pane reads Claude transcripts/subagents/workflow journals and selected configuration/plugin metadata, observes local process/session files to associate child sessions and stores derived usage state and child-link metadata locally. The child-session resolver can inspect other project/session headers to find related processes; this is broader than opening one selected JSONL file. Do not describe the runtime as filesystem read-only or automatically scan personal records from a skill invocation. The UI can contain snippets from prompts, tool results and filenames; redact before sharing it. No personal transcript is bundled and no external collector is configured.

OpenDigital removes the automatic session-report dependency and report UI/model action, autocompact command/UI/settings helpers, report transcript hardlink/deletion path and maintenance scripts. The pane retains local measurement/state; it is not an immutable-record auditor.

Prices are a dated standard API list-price estimate, not subscription charges, an invoice or an account balance. Models with no exact/version-dated rate remain unpriced. Corrected Fable/Mythos 5.2 and Sonnet 5.5 cache pricing are documented in PROVENANCE/overrides. Fast mode, regional agreements, failed-search billing and missing transcript fields can cause differences. Trust the harness snapshot as its own measurement, with coverage stated, and reconcile billing separately.

Removing `--plugin-dir` from a future launch unloads this local opt-in package; do not delete user state as an automatic rollback. Runtime fixtures in ../../evals/runtime.test.ts use only synthetic data and reviewed pure digest modules.
