# Finding format and severity scale

Part of code-quality:codebase-audit. Every specialist reports each finding exactly in this format:

```markdown
### [ID] Short, specific title
- **Specialist:** <name>
- **Category:** <e.g. SQL injection, N+1, duplication, exposed secret>
- **Severity:** CRITICAL | HIGH | MEDIUM | LOW | INFO
- **Confidence:** high | medium | low
- **Location:** `path/file.ext:start-line[-end-line]` (list every location if more than one)
- **Reference:** <CWE-89, OWASP A03:2021, language rule, when applicable>

**Problem:** what is wrong, in one to three sentences.

**Evidence:**
```<language>
<short, real excerpt>
```

**Failure scenario / impact:** concrete input or state → concrete consequence (data leaked, crash, slowdown of X, maintenance cost).

**Suggested fix:**
```<language>
<corrected code, in the project's style>
```

**Estimated effort:** trivial | small | medium | large
```

IDs per specialist: `SEC-01`, `LEAK-01`, `DEP-01`, `COR-01`, `PERF-01`, `DUP-01`, `PRAC-01`, `TEST-01`, `INFRA-01`.

## Severity scale

| Severity | When | Examples |
|---|---|---|
| **CRITICAL** | Exploitable now, without rare preconditions, with severe impact: remote execution, authentication bypass, mass leak, data loss, production secret exposed | SQL injection on a public endpoint; AWS key in the repository; user-triggerable `DELETE` without `WHERE` |
| **HIGH** | Serious vulnerability or bug with a plausible precondition; important functionality broken; large slowdown on a hot path | IDOR that requires being logged in; race condition in payments; N+1 on the main listing |
| **MEDIUM** | Real problem with limited impact or specific conditions; technical debt that already costs | No rate limit on login; business rule duplicated in three places; error silently swallowed |
| **LOW** | Quality, robustness or readability improvement with low risk | Misleading name; long function; optional security header missing |
| **INFO** | Observation or suggestion without a defect | Simplification opportunity; recommended pattern |

## Confidence scale

- **high:** you followed the flow and are certain the problem occurs.
- **medium:** it occurs unless a protection exists that you did not find (say where you looked).
- **low:** a suspicion that needs human confirmation. Use sparingly.

## Rules

- One finding = one root cause. If the same cause appears in several files, make **one** finding with every location.
- No finding without a real location and evidence.
- Secrets are always masked in the evidence.
