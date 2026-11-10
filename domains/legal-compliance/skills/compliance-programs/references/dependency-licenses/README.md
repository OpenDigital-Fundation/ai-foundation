# Dependency licence evidence

Part of `legal-compliance:compliance-programs`. Adapted from upstream dependency-checking documentation. The heuristic shell checker and session-end config are not distributed; this is an evidence/policy checklist, not a legal conclusion.

## Inventory the resolved dependency

Record ecosystem, exact version or commit, lockfile identity, direct/transitive relationship, retrieved source and the nearest applicable licence/notice. Include package-level exceptions and embedded third-party declarations; a repository-level label alone is not enough.

Read already available, version-matched metadata and licence files first. Do not query a registry's current package version or choose an arbitrary module-cache directory as evidence for the version actually shipped. Do not install or execute dependencies to identify their licence.

## Evaluate the policy

Use the project's approved licence policy. Parse SPDX expressions with an appropriate parser, including AND/OR and exceptions; substring matching cannot decide compatibility or licence obligations. Distinguish technical detection from the maintainer's acceptance/legal review.

An absent or ambiguous licence is UNKNOWN and requires review, not an automatic pass. Record narrow exceptions with owner, reason, exact version and review date. Do not assume a permissive root licence overrides a restricted embedded source.

## Evidence and enforcement

Report package/version, licence evidence path, policy result and unresolved questions without credentials or raw environment data. Preserve required attributions and notices in the delivered package. A scan report is not proof of legal compliance.

A session-end warning is observational; it does not guarantee that an earlier commit was prevented. If enforcement is required, use a reviewed local checker at the appropriate pre-action/CI boundary, with explicit installation approval and fixtures for unknown licences, compound SPDX, cache/version mismatch and checker failure.
