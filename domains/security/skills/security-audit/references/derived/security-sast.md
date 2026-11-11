# Security audit — security sast

Part of `security:security-audit`. Adapted reference material; the owner procedure, project conventions, scope and authorization rules take precedence. Examples are not automatically executed.

<!-- source: wshobson/agents plugins/security-scanning/commands/security-sast.md#multi-language-scanner-implementation -->

## Common SAST finding record

Normalize findings across locally approved scanners without treating tool output as a proven exploit. Useful fields are scanner/version, rule, severity, category, file/line, diagnostic, CWE or supplied taxonomy, confidence, evidence and validation status. Keep scanner execution status separate from findings.

## Execution and evidence contract

- Map languages/manifests before choosing an installed, version-fixed scanner and locally reviewed ruleset. Do not download rules or packages implicitly during an audit.
- Bound runtime and output, keep errors visible, and record unsupported languages or failed scans as incomplete coverage.
- Do not present an illustrative code skeleton as a complete scanner: the upstream example calls methods it does not implement and catches errors without a failed-scan result. It is not distributed here as executable tooling.
- Deduplicate by evidence/location, verify the trust boundary and distinguish confirmed impact from a pattern match. A sum of severity weights is not calibrated business risk.
- Follow security-audit for authorized scope and the final report; never report zero findings as proof of security when a tool failed.
