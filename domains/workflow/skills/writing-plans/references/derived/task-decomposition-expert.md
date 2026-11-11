# Writing plans — task decomposition expert

Part of `workflow:writing-plans`. Adapted reference material; the owner procedure, project conventions, scope and authorization rules take precedence. Examples are not automatically executed.

## task-decomposition-expert

<!-- source: davila7/claude-code-templates cli-tool/components/agents/ai-specialists/task-decomposition-expert.md#core-analysis-framework -->

### Core Analysis Framework

When requirements are in hand, execute these steps in order:

#### 1. Goal Analysis

Restate the user's objective as a single measurable outcome. Identify:
- **Explicit requirements**: Stated in the user's request
- **Implicit requirements**: Constraints that follow logically (e.g., auth needed if there are users)
- **Out of scope**: What this decomposition explicitly excludes
- **Success metrics**: Quantitative criteria for each major milestone

#### 2. Work Breakdown Structure (WBS)

Decompose the goal into a three-level hierarchy:

```
Level 1: Primary Objectives (high-level outcomes, 3–7 total)
  Level 2: Tasks (supporting activities per objective)
    Level 3: Atomic Actions (specific executable steps, 1–8 hours each)
```

Apply the **8/80 rule**: no atomic action should take fewer than 8 hours or more than 80 hours. If a task exceeds 80 hours, decompose it further. If a task is under 8 hours, aggregate it with a sibling.

#### 3. Dependency Mapping

Produce a dependency graph for all Level 2 tasks using this notation:

```
[TASK-A] → [TASK-B]          # B requires A to be complete
[TASK-A] ⟷ [TASK-B]         # A and B can run in parallel
[TASK-A] ⟹ [TASK-B]         # B is blocked until A delivers a specific artifact
```

Identify the **critical path**: the longest chain of sequential dependencies that determines minimum project duration.

#### 4. Parallelism Map

Group tasks into execution tracks that can proceed simultaneously:

| Track | Tasks | Owner Role | Duration Estimate | Depends On |
|---|---|---|---|---|
| Track A | ... | backend-developer | X days | none |
| Track B | ... | frontend-developer | Y days | Track A milestone 1 |

#### 5. Effort and Complexity Heuristics

For each Level 2 task, assign:
- **Effort** (person-days): Sum of atomic action estimates
- **Complexity** (Low / Medium / High / Very High): Based on unknowns, integration surface, and reversibility
- **Risk rating** (1–5): Likelihood × impact of this task failing

For tasks with Complexity rated Medium or higher, provide three-point (PERT) estimates instead of a single figure — optimistic (O), most likely (M), and pessimistic (P) — and compute the PERT-weighted effort: `(O + 4M + P) / 6`. Flag any task where P > 2× O as high-uncertainty and recommend a spike/discovery task before committing to the estimate.

#### 6. Risk Register

List the top 5 risks in this format:

| Risk | Likelihood | Impact | Mitigation Task | Owner |
|---|---|---|---|---|
| Database migration corrupts records | Low | Critical | Add rollback script + staging dry-run | database-architect |

#### 7. Validation Checkpoints

Define a gate at each major milestone:
- What artifact must exist (e.g., passing test suite, deployed staging endpoint)
- What metric must be met (e.g., P95 latency < 200ms)
- Who approves the gate before the next phase begins
