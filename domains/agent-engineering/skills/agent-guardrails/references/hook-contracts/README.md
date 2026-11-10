# Hook contracts

Part of `agent-engineering:agent-guardrails`. Adapted from upstream hook authoring guidance and Tool Guardian documentation. Upstream scripts and configs are not distributed by this guide; no installation or execution is implied.

## Bind the contract to the host

Record the host, supported version, lifecycle event, payload schema, response schema, timeout and working directory before implementing a hook. A Copilot event or exit-code convention is not a portable contract for Claude Code, Codex or another host. Check the host documentation and test the behaviour in isolation.

| Boundary | What to verify |
|---|---|
| Input | Parse one bounded JSON payload from stdin; reject malformed or missing required fields |
| Tool arguments | Some Copilot examples encode `toolArgs` as a JSON string and require a second parse; do not substitute `toolInput` without a verified adapter |
| Environment | Configuration variables are process environment, not event arguments; validate values and paths |
| Output | Use a JSON encoder for structured responses; put human diagnostics on stderr |
| Deny | For hosts/events supporting `permissionDecision`, use their documented structured response; verify that denial prevents the action |
| Exit status | Distinguish hook failure from policy denial; non-zero does not universally mean the action was blocked |
| Lifecycle | Use a pre-action event for prevention; a session-end event can only report what already happened |
| Timeout | Bound work and document whether host failure is fail-open or fail-closed |
| Scope | Restrict event/tool matchers and retain in-script validation when the host requires it |

## Authoring rules

- Keep hooks deterministic, local and narrowly scoped; no package downloads or installation at hook execution time.
- Do not trust current working directory, environment, filenames, commands or tool output merely because they came through the host.
- Fail closed for uncertain high-risk decisions; report the reason without logging secrets.
- Do not parse general shell syntax with a few regexes or fall back from JSON to grep/sed.
- Keep allowlists exact and scoped; an allowlisted substring must not exempt the rest of a compound command.
- Ensure every script referenced by a published config is included, reviewed and executable in that package.
- Do not run release, push, destructive cleanup or dependency installation automatically at session end.
- Keep installation opt-in with a reversible change to an explicitly approved host configuration.

## Acceptance evidence

Run only synthetic harmless inputs while developing the adapter. Cover missing/malformed fields, both supported argument encodings, Unicode/quoting, shell wrappers, denied and allowed fixtures, timeouts, unexpected output, and logger failures. Check the actual host result as well as script output.

Record the host version and the fixture's expected/observed decision. A passing unit test of a regex is not proof that the host blocked a real tool call. See [operation policies](../operation-policies/README.md) for the policy catalogue.
