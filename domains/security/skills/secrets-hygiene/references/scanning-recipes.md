# Secret scanning recipes

Part of `security:secrets-hygiene`. Adapted from the upstream Secrets Scanner policy catalogue. Its shell script and hook config are not distributed here; use a maintained scanner or a reviewed local implementation.

## Detection catalogue

Look for provider token formats, private keys, database connection strings, authentication headers, generic credential assignments and internal endpoints that should not be public. A format match is a lead, not proof that a credential is valid; never call a service to test a suspected secret.

Patterns and placeholder allowlists are incomplete. Do not exempt an entire file or compound finding because it contains words such as test, sample or example. Review false positives narrowly without publishing the matched value.

## Choose the scanned content

- For a commit gate, scan the exact staged/index content, including newly staged files and partially staged edits. A scan of the working copy does not prove the commit is clean.
- For investigation, compare staged, unstaged and untracked content explicitly; include relevant history/artifacts when exposure is suspected.
- Parse filenames with NUL delimiters, handle spaces/newlines and binary files, and do not silently ignore unreadable input or invalid patterns.
- A session-end warning reports a finding after the session; it cannot reliably prevent a commit already made. Enforce an approved pre-commit gate or CI policy separately.

## Handle findings

Redact before logging or returning data to an agent. Report path, line, category and severity without retaining the raw match; for highly sensitive keys, retain no prefix or suffix. Limit log access and retention.

Treat an exposed secret as compromised: revoke/rotate, assess access and downstream copies, then clean up. Do not rewrite shared history or delete artifacts without the required approval.

## Implementation gate

The upstream example has literal-TAB record handling and filename/parser weaknesses. Do not use it as a ready prevention control. Test a reviewed implementation with synthetic secrets only: staged-vs-working-copy mismatch, partial staging, untracked files, unusual filenames, malformed patterns, scanner failure and redaction. A failure to scan must not produce a clean result.
