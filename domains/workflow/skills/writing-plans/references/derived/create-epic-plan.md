# Writing plans — create epic plan

Part of `workflow:writing-plans`. Adapted reference material; the owner procedure, project conventions, scope and authorization rules take precedence. Examples are not automatically executed.

## Epic Planning Document Generator

<!-- source: Jeffallan/claude-skills commands/project/planning/create-epic-plan.md#risk-assessment-framework -->

### Risk Assessment Framework

Evaluate each technical change across 7 dimensions (score 1-3 each):

| Dimension | Low (1) | Medium (2) | High (3) |
|-----------|---------|------------|----------|
| **Scope** | ≤3 files, isolated change | 4-10 files, single feature | 10+ files, cross-cutting |
| **Dependencies** | All prerequisites exist | Some foundation work needed | Requires significant groundwork |
| **Blocking Factor** | Independent work | Soft dependency for 1-2 tickets | Hard blocker for multiple streams |
| **Stability** | Well-defined, existing patterns | Some unknowns, new patterns | Novel approach, high uncertainty |
| **UX Impact** | Backend/internal only | Secondary flows affected | Core user journey affected |
| **Testing Complexity** | Simple assertions, existing fixtures | New mocks/fixtures needed, async flows | Complex integration, E2E required, hard to isolate |
| **Reversibility** | Easily reverted, no data changes | Moderate effort to rollback | Database migrations, breaking API changes, one-way door |

**Risk Levels:**
- **7-11 (Low):** Proceed with standard implementation
- **12-16 (Medium):** Incremental delivery, extra code review
- **17-21 (High):** Spike/POC first, decompose further, architectural review required

---
