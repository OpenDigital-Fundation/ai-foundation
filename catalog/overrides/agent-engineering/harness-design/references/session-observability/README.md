# Session observability

Part of `agent-engineering:harness-design`. Adapted from upstream session logging and governance audit documentation. Only the event/logging concepts are retained; no upstream hook, config or prompt-threat detector is distributed or installed.

## Minimal event record

Record a timestamp, event type, stable session identifier and the smallest relevant context. For example:

```json
{"timestamp":"2026-01-01T00:00:00Z","event":"session_start","session_id":"example-session","policy_mode":"observe"}
```

Serialize with a JSON encoder. Do not interpolate environment values into JSON strings, store raw prompts, credentials or full tool arguments, or claim that JSON formatting alone provides redaction.

## Lifecycle

| Event | Useful observation | Limitation |
|---|---|---|
| Session start | Session identity, adapter version and policy mode | A start event does not prove controls are active |
| Prompt submitted | Timestamp and event type, without prompt contents | Metadata cannot detect prompt injection |
| Session end | Counts scoped by session_id and outcome | Reporting after the action cannot prevent a commit or tool call |

Correlate by session_id, not the last timestamp in a shared log. Account for concurrent sessions, missing termination, clock skew and duplicate events. Counts must refer to records, not formatted text lines.

## Privacy and retention

Logging is opt-in. Agree the destination, access restrictions, retention period and deletion procedure before enabling it. Omit private paths when unnecessary; prevent symlink/path escape and uncontrolled growth. A disabled logger should not create directories.

Audit events are observations, not a governance guarantee. The upstream regex prompt detector is not adopted; arbitrary numeric threat scores and absence of alerts are not evidence that a session is safe. Keep permissions and policy enforcement at the tool boundary.

## Verification

Test the logger using harmless synthetic metadata: quoted/newline-containing values, invalid event JSON, simultaneous sessions, full storage, permission errors, and redaction cases. Verify parseable records and bounded failure without exposing raw data.

For a tool-blocking implementation, use `agent-engineering:agent-guardrails` and verify the host-specific pre-action contract separately.
