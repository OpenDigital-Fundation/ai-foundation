# Parallel agents — multi reviewer patterns

Part of `agent-engineering:parallel-agents`. Adapted reference material; the owner procedure, project conventions, scope and authorization rules take precedence. Examples are not automatically executed.

## Multi-Reviewer Patterns

<!-- source: wshobson/agents plugins/agent-teams/skills`code-quality:code-review`er-patterns/SKILL.md#review-dimension-allocation,severity-calibration -->

### Review Dimension Allocation

#### Available Dimensions

| Dimension         | Focus                                   | When to Include                             |
| ----------------- | --------------------------------------- | ------------------------------------------- |
| **Security**      | Vulnerabilities, auth, input validation | Always for code handling user input or auth |
| **Performance**   | Query efficiency, memory, caching       | When changing data access or hot paths      |
| **Architecture**  | SOLID, coupling, patterns               | For structural changes or new modules       |
| **Testing**       | Coverage, quality, edge cases           | When adding new functionality               |
| **Accessibility** | WCAG, ARIA, keyboard nav                | For UI/frontend changes                     |

#### Recommended Combinations

| Scenario               | Dimensions                                   |
| ---------------------- | -------------------------------------------- |
| API endpoint changes   | Security, Performance, Architecture          |
| Frontend component     | Architecture, Testing, Accessibility         |
| Database migration     | Performance, Architecture                    |
| Authentication changes | Security, Testing                            |
| Full feature review    | Security, Performance, Architecture, Testing |

### Severity Calibration

#### Severity Criteria

| Severity     | Impact                                        | Likelihood             | Examples                                     |
| ------------ | --------------------------------------------- | ---------------------- | -------------------------------------------- |
| **Critical** | Data loss, security breach, complete failure  | Certain or very likely | SQL injection, auth bypass, data corruption  |
| **High**     | Significant functionality impact, degradation | Likely                 | Memory leak, missing validation, broken flow |
| **Medium**   | Partial impact, workaround exists             | Possible               | N+1 query, missing edge case, unclear error  |
| **Low**      | Minimal impact, cosmetic                      | Unlikely               | Style issue, minor optimization, naming      |

#### Calibration Rules

- Security vulnerabilities exploitable by external users: always Critical or High
- Performance issues in hot paths: at least Medium
- Missing tests for critical paths: at least Medium
- Accessibility violations for core functionality: at least Medium
- Code style issues with no functional impact: Low
