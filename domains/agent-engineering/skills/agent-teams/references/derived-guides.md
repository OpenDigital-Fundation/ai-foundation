# Agent teams — derived guides

Part of `agent-engineering:agent-teams`.

## team-reviewer

<!-- source: wshobson/agents plugins/agent-teams/agents`code-quality:code-review`er.md#review-dimensions -->

### Review Dimensions

#### Security

- Input validation and sanitization
- Authentication and authorization checks
- SQL injection, XSS, CSRF vulnerabilities
- Secrets and credential exposure
- Dependency vulnerabilities (known CVEs)
- Insecure cryptographic usage
- Access control bypass vectors
- API security (rate limiting, input bounds)

#### Performance

- Database query efficiency (N+1, missing indexes, full scans)
- Memory allocation patterns and potential leaks
- Unnecessary computation or redundant operations
- Caching opportunities and cache invalidation
- Async/concurrent programming correctness
- Resource cleanup and connection management
- Algorithm complexity (time and space)
- Bundle size and lazy loading opportunities

#### Architecture

- SOLID principle adherence
- Separation of concerns and layer boundaries
- Dependency direction and circular dependencies
- API contract design and versioning
- Error handling strategy consistency
- Configuration management patterns
- Abstraction appropriateness (over/under-engineering)
- Module cohesion and coupling analysis

#### Testing

- Test coverage gaps for critical paths
- Test isolation and determinism
- Mock/stub appropriateness and accuracy
- Edge case and boundary condition coverage
- Integration test completeness
- Test naming and documentation clarity
- Assertion quality and specificity
- Test maintainability and brittleness

#### Accessibility

- WCAG 2.1 AA compliance
- Semantic HTML and ARIA usage
- Keyboard navigation support
- Screen reader compatibility
- Color contrast ratios
- Focus management and tab order
- Alternative text for media
- Responsive design and zoom support

## task-distributor

<!-- source: VoltAgent/awesome-claude-code-subagents categories/09-meta-orchestration/task-distributor.md#what-to-design -->

### What to design

#### Queue and ordering conventions

- How tasks enter and are ordered (FIFO, priority-ordered, deadline-ordered).
- Priority tiers and what each means.
- Handling for retries, time-to-live / stale tasks, and a dead-letter destination for tasks that repeatedly fail.
- Batch grouping when tasks share setup cost.

#### Load-balancing approach

Pick and justify a distribution strategy for the workload:

- **Round-robin** — even, stateless spread when tasks are similar.
- **Weighted** — when workers have different capacities.
- **Least-loaded** — assign to the worker with the fewest in-flight tasks.
- **Capability / affinity routing** — route by skill match or by grouping related tasks to one worker.
- **Consistent hashing** — stable task-to-worker mapping across a changing worker set.

Note the trade-offs of the chosen strategy rather than claiming one is universally best.

#### Priority and deadline handling

- How high-priority work preempts or jumps ahead of lower-priority work.
- Starvation prevention so low-priority tasks still eventually run.
- What happens when a deadline cannot be met (escalate, drop, reassign) — make the policy explicit.

#### Capacity and fallback

- How to represent each worker's capacity and current assignment.
- Fallback when a worker is unavailable or a task fails: reassign, retry with backoff, or route to dead-letter.

## team-implementer

<!-- source: wshobson/agents plugins/agent-teams/agents/team-implementer.md#implementation-workflow -->

### Implementation Workflow

#### Phase 1: Understand Assignment

- Read your task description thoroughly
- Identify owned files and directories
- Review interface contracts with adjacent components
- Understand acceptance criteria

#### Phase 2: Plan Implementation

- Design your component's internal architecture
- Identify integration points with other teammates' components
- Plan your implementation sequence (dependencies first)
- Note any blockers or questions for the team lead

#### Phase 3: Build

- Implement core functionality within owned files
- Follow existing codebase patterns and conventions
- Write code that satisfies the interface contracts
- Keep changes minimal and focused

#### Phase 4: Verify

- Ensure your code compiles/passes linting
- Test integration points match the agreed interfaces
- Verify acceptance criteria are met
- Run any applicable tests

#### Phase 5: Report

- Mark your task as completed via TaskUpdate
- Message the team lead with a summary of changes
- Note any integration concerns for other teammates
- Flag any deviations from the original plan

## multi-agent-coordinator

<!-- source: VoltAgent/awesome-claude-code-subagents categories/09-meta-orchestration/multi-agent-coordinator.md#coordination-strategies-to-draw-from -->

### Coordination strategies to draw from

Choose the pattern that fits the dependency structure; do not apply all of them.

- **Sequential pipeline** — agent B consumes agent A's output file. Use when there is a hard dependency chain.
- **Fan-out / fan-in** — the orchestrator invokes several independent agents, then a final agent aggregates their output files. Use when subtasks are independent and results merge at the end.
- **Master–worker** — one coordinating agent splits work into file-based tasks and a later step collects the results.
- **Shared-file state** — agents read and write a common Markdown/JSON file to pass context. Define a single writer per file where possible to avoid conflicts.

For dependencies: sketch the dependency graph, order independent work to run concurrently, and call out any cycle (A needs B and B needs A) as something to break before execution, since it cannot be resolved at runtime here.
