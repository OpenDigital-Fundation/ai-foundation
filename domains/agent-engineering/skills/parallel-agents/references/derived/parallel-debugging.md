# Parallel agents — parallel debugging

Part of `agent-engineering:parallel-agents`. Adapted reference material; the owner procedure, project conventions, scope and authorization rules take precedence. Examples are not automatically executed.

## Parallel Debugging

<!-- source: wshobson/agents plugins/agent-teams/skills/parallel-debugging/SKILL.md#evidence-collection-standards,hypothesis-generation-framework -->

### Hypothesis Generation Framework

Generate hypotheses across 6 failure mode categories:

#### 1. Logic Error

- Incorrect conditional logic (wrong operator, missing case)
- Off-by-one errors in loops or array access
- Missing edge case handling
- Incorrect algorithm implementation

#### 2. Data Issue

- Invalid or unexpected input data
- Type mismatch or coercion error
- Null/undefined/None where value expected
- Encoding or serialization problem
- Data truncation or overflow

#### 3. State Problem

- Race condition between concurrent operations
- Stale cache returning outdated data
- Incorrect initialization or default values
- Unintended mutation of shared state
- State machine transition error

#### 4. Integration Failure

- API contract violation (request/response mismatch)
- Version incompatibility between components
- Configuration mismatch between environments
- Missing or incorrect environment variables
- Network timeout or connection failure

#### 5. Resource Issue

- Memory leak causing gradual degradation
- Connection pool exhaustion
- File descriptor or handle leak
- Disk space or quota exceeded
- CPU saturation from inefficient processing

#### 6. Environment

- Missing runtime dependency
- Wrong library or framework version
- Platform-specific behavior difference
- Permission or access control issue
- Timezone or locale-related behavior

### Evidence Collection Standards

#### What Constitutes Evidence

| Evidence Type     | Strength | Example                                                         |
| ----------------- | -------- | --------------------------------------------------------------- |
| **Direct**        | Strong   | Code at `file.ts:42` shows `if (x > 0)` should be `if (x >= 0)` |
| **Correlational** | Medium   | Error rate increased after commit `abc123`                      |
| **Testimonial**   | Weak     | "It works on my machine"                                        |
| **Absence**       | Variable | No null check found in the code path                            |

#### Citation Format

Always cite evidence with file:line references:

```
**Evidence**: The validation function at `src/validators/user.ts:87`
does not check for empty strings, only null/undefined. This allows
empty email addresses to pass validation.
```

#### Confidence Levels

| Level               | Criteria                                                                            |
| ------------------- | ----------------------------------------------------------------------------------- |
| **High (>80%)**     | Multiple direct evidence pieces, clear causal chain, no contradicting evidence      |
| **Medium (50-80%)** | Some direct evidence, plausible causal chain, minor ambiguities                     |
| **Low (<50%)**      | Mostly correlational evidence, incomplete causal chain, some contradicting evidence |
