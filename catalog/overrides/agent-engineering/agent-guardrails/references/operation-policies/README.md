# Operation policies

Part of `agent-engineering:agent-guardrails`. Adapted from the upstream Tool Guardian policy catalogue; its script is not distributed here. This document does not install a hook or provide a working security boundary.

## Policy catalogue

| Operation | Evidence to inspect | Required decision |
|---|---|---|
| Recursive deletion | Exact paths, expansion, symlinks, repository boundaries | Show the affected paths and obtain explicit approval; deny ambiguous targets |
| Git history/ref changes | Refs, shared status, force/reset/clean flags | Preserve work and require approval for the exact destructive operation |
| Database destruction | Target environment, affected rows, transaction and recovery plan | Read-only diagnostics first; require an approved migration before writes |
| Permission escalation | Target resource, owner and requested access | Use the least privilege needed; require approval for permission changes |
| Remote code or uploads | Endpoint, payload, pinned source and authorization | Do not fetch-and-execute unreviewed code or send data without authorization |
| Publishing | Repository/registry, exact commits or version, visibility | Require approval of the concrete destination and content |

Patterns are leads for policy decisions, not a complete shell parser. Simple substring allowlists cannot safely authorize compound commands, substitutions, wrappers or encoded payloads. Do not suggest force-with-lease as permission to rewrite shared history.

## Implementation gate

Use an opt-in hook only after explicit installation approval and review of its local implementation. Follow [the hook contract guide](../hook-contracts/README.md). Parse the documented host payload strictly, normalize commands with a parser appropriate to the host, and deny uncertain high-risk input. Do not log raw command arguments or credentials.

The original example has incompatible payload assumptions and record separators; it is not an implementation template. Reusing its threat labels does not establish bypass resistance.

## Verification cases

Use synthetic fixtures, never destructive commands, for: allowed reads; explicitly approved writes; malformed JSON; missing command fields; argument reordering; wrappers; command substitution; quoted metacharacters; compound commands; path traversal; and exact-scope allowlist decisions.

A denied fixture must produce the host's documented deny response and prevent the action in an isolated host test. A parser failure must not silently allow a high-risk operation. Verify timeout/failure behaviour rather than inferring it from a non-zero exit.
