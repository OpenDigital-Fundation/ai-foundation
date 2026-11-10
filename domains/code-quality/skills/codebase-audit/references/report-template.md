# Final report template

Part of code-quality:codebase-audit. Use this structure in `docs/code-review/REPORT-<YYYY-MM-DD>.md`.

```markdown
# Code review report — <project>

**Date:** <YYYY-MM-DD> · **Scope:** <project | diff base..HEAD | path> · **Mode:** <full | quick | focus:x>
**Commit reviewed:** <short hash, if a git repository> · **Specialists run:** <list>

## 1. Executive summary

**Overall grade:** <A, B, C, D or F> — <one sentence why>

| Dimension | Grade | Short comment |
|---|---|---|
| Security | A–F | |
| Data protection | A–F | |
| Dependencies | A–F | |
| Correctness | A–F | |
| Performance | A–F | |
| Architecture / duplication | A–F | |
| Practices | A–F | |
| Tests | A–F | |
| Infrastructure / configuration | A–F | |

| Severity | Count |
|---|---|
| CRITICAL | n |
| HIGH | n |
| MEDIUM | n |
| LOW | n |
| INFO | n |

**Top 5 most urgent actions:**
1. [ID] … — why it is urgent

## 2. Project overview
Summary of the project map (stack, architecture, trust boundaries) in up to ten lines.

## 3. Findings by severity
### 3.1 Critical
(findings in the standard format, with the verifier status: CONFIRMED / LIKELY)
### 3.2 High
### 3.3 Medium
### 3.4 Low
### 3.5 Informational

## 4. Suggested action plan
- **Now (before the next deploy):** confirmed critical and high IDs
- **Next cycle:** medium
- **Quality backlog:** low and info
Group fixes that can be done together (same file or same cause).

## 5. Strengths
What the project does well (worth keeping).

## 6. Review limitations
Areas not covered, assumptions, things that depend on production configuration, tools that could not be run.

## Appendix A — Findings dismissed by the verifier
- [ID] title — reason (one line)

## Appendix B — Recommended commands
Tools the team can run to keep quality up (e.g. `npm audit`, `pip-audit`, `gitleaks`, `semgrep`, linters), suited to the detected stack.
```

## Grading criteria

- **A:** no critical or high; few medium.
- **B:** no critical; up to ~3 high with low reach.
- **C:** a relevant high or many medium.
- **D:** a critical or several high.
- **F:** several critical, or one trivially exploitable critical in production.
