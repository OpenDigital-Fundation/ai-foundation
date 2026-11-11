# Debt ledger — technical debt auditor

Part of `code-quality:debt-ledger`. Adapted reference material; the owner procedure, project conventions, scope and authorization rules take precedence. Examples are not automatically executed.

## Technical Debt Auditor

<!-- source: davila7/claude-code-templates cli-tool/components/skills/development/technical-debt-auditor/SKILL.md#what-you-re-scanning-for -->

### What you're scanning for

| Debt category | What to look for | Why it matters |
|---|---|---|
| **Marker debt** | TODO, FIXME, HACK, XXX, TEMP, WORKAROUND comments | Developers flagged these as known shortcuts — they're self-reported debt |
| **Dead code** | Unused exports, unreachable branches, commented-out code blocks, unused files | Dead code misleads readers, adds cognitive load, and sometimes hides bugs |
| **Dependency debt** | Outdated packages, deprecated APIs, pinned-to-old-major versions, unused deps in package manifest | Stale deps accumulate security vulns and block upgrades |
| **Complexity hotspots** | Large files (>300 lines), large functions (>50 lines), deeply nested logic (>3 levels), high cyclomatic complexity | Complex code is where bugs hide and where changes are slowest |
| **Duplication signals** | Near-identical code blocks, copy-pasted patterns with slight variations | Duplication means bug fixes need to happen in N places instead of 1 |
| **Test gaps** | Missing test files for modules, low assertion density, test files that only test happy paths | Untested code is where regressions slip through |
| **Outdated patterns** | Patterns that contradict the project's own conventions, deprecated language features, legacy API usage | Inconsistency slows onboarding and creates confusion |
| **Config debt** | Stale configs, conflicting settings, environment files with unused variables | Config debt causes "works on my machine" bugs and deploy failures |
