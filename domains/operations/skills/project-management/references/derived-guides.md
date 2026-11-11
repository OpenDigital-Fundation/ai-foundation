# Project management — derived guides

Part of `operations:project-management`.

## Sprint Retrospective Generator

<!-- source: Jeffallan/claude-skills commands/project/retrospectives/complete-sprint.md#metrics-dashboard -->

### Metrics Dashboard

#### Sprint Velocity
- **Planned Velocity:** [points]
- **Actual Velocity:** [points]
- **Variance:** [+/- points] ([%])
- **Trend:** [comparison to previous sprints]

#### Story Points Analysis
| Epic | Planned | Actual | Variance | Reason for Variance |
|------|---------|--------|----------|-------------------|
| [{Epic_Key}] | [pts] | [pts] | [+/-] | [explanation] |
| **Total** | **[pts]** | **[pts]** | **[+/-]** | |

#### Bug Metrics
- **Bugs Introduced:** [count]
  - By epic: [breakdown]
  - By severity: [critical/high/medium/low]
- **Bugs Resolved:** [count]
- **Net Change:** [+/- count]
- **Escaped to Production:** [count]
- **Average Resolution Time:** [hours/days]

#### Cycle Time Analysis
- **Average Cycle Time:** [days from start to completion]
- **Cycle Time by Epic:**
  - {Epic_Key}: [days] ([comparison to estimate])
- **Bottlenecks Identified:** [list stages with delays]

#### Code Review Metrics
- **PRs Created:** [count]
- **Average Review Time:** [hours/days]
- **PRs with > 1 Revision:** [count] ([%])
- **Average Revisions per PR:** [number]
- **Review Feedback Quality:** [assessment]

#### Test Coverage Metrics
- **Sprint Start Coverage:** [%]
- **Sprint End Coverage:** [%]
- **Coverage Change:** [+/- %]
- **Coverage by Epic:** [breakdown]
- **Target Met:** [Yes/No - 90% target]

#### Technical Debt Metrics
- **Debt Items at Sprint Start:** [count]
- **Debt Introduced:** [count]
- **Debt Resolved:** [count]
- **Net Change:** [+/- count]
- **Debt by Category:** [breakdown]

---

## Standup Notes Generator

<!-- source: wshobson/agents plugins/team-collaboration/commands/standup-notes.md#async-standup-patterns,yesterday-s-accomplishments-extraction,blockers-and-dependencies-identification,communication-best-practices -->

### Yesterday's Accomplishments Extraction

**AI-Assisted Commit Analysis:**

```
For each commit in the last 24-48 hours:
1. Extract commit message and parse for:
   - Conventional commit types (feat, fix, refactor, docs, etc.)
   - Ticket references (JIRA-123, #456, etc.)
   - Descriptive action (what was accomplished)
2. Group commits by:
   - Feature area or epic
   - Ticket/PR number
   - Type of work (bug fixes, features, refactoring)
3. Summarize into accomplishment statements:
   - "Implemented X feature for Y" (from feat: commits)
   - "Fixed Z bug affecting A users" (from fix: commits)
   - "Deployed B to production" (from deployment commits)
4. Cross-reference with Jira:
   - If commit references ticket, use ticket title for context
   - Add ticket status if moved to Done/Closed
   - Include acceptance criteria met if available
```

**Obsidian Task Completion Parsing:**

```
Search vault for completed tasks (last 24-48h):
- Pattern: `- [x] Task description` with recent modification date
- Extract context from surrounding notes (which project, meeting, or epic)
- Summarize completed todos from daily notes
- Include any journal entries about accomplishments or milestones
```

**Accomplishment Quality Criteria:**

- Focus on delivered value, not just activity ("Shipped user auth" vs "Worked on auth")
- Include impact when known ("Fixed bug affecting 20% of users")
- Connect to team goals or sprint objectives
- Avoid jargon unless team-standard terminology

### Blockers and Dependencies Identification

**Blocker Categorization:**

**Hard Blockers (work completely stopped):**

- Waiting on external API access or credentials
- Blocked by failed CI/CD or infrastructure issues
- Dependent on another team's incomplete work
- Missing requirements or design decisions

**Soft Blockers (work slowed but not stopped):**

- Need clarification on requirements (can proceed with assumptions)
- Waiting on code review (can start next task)
- Performance issues impacting development workflow
- Missing nice-to-have resources or tools

**Blocker Escalation Format:**

```markdown
## Blockers

• **[CRITICAL]** [Description] - Blocked since [date]

- **Impact:** [What work is stopped, team/customer impact]
- **Need:** [Specific action required]
- **From:** [@person or @team]
- **Tried:** [What you've already attempted]
- **Next step:** [What will happen if not resolved by X date]

• **[NORMAL]** [Description] - [When it became a blocker]

- **Need:** [What would unblock]
- **Workaround:** [Current alternative approach if any]
```

**Dependency Tracking:**

- Call out cross-team dependencies explicitly
- Include expected delivery dates for dependent work
- Tag relevant stakeholders with @mentions
- Update dependencies daily until resolved

### Communication Best Practices

**Async-First Principles:**

- Post standup notes at consistent time daily (e.g., 9am local time)
- Don't wait for synchronous standup meeting to share updates
- Include enough context for readers in different timezones
- Link to detailed docs/tickets rather than explaining in-line
- Make blockers actionable (specific requests, not vague concerns)

**Visibility and Transparency:**

- Share wins and progress, not just problems
- Be honest about challenges and timeline concerns early
- Call out dependencies proactively before they become blockers
- Highlight collaboration and team support activities
- Include learning moments or process improvements

**Team Coordination:**

- Read teammates' standup notes before posting yours (adjust plans accordingly)
- Offer help when you see blockers you can resolve
- Tag people when their input or action is needed
- Use threads for discussion, keep main post scannable
- Update throughout day if priorities shift significantly

**Writing Style:**

- Use active voice and clear action verbs
- Avoid ambiguous terms ("soon", "later", "eventually")
- Be specific about timeline and scope
- Balance confidence with appropriate uncertainty
- Keep it human (casual tone, not formal report)

### Async Standup Patterns

**Written-Only Standup (No Sync Meeting):**

```markdown
# Post daily in #standup-team-name Slack channel

**Posted:** 9:00 AM PT | **Read time:** ~2min

## ✅ Yesterday

• Shipped user profile API endpoints (JIRA-234) - Live in staging
• Fixed critical bug in payment flow - PR merged, deploying at 2pm
• Reviewed PRs from @teammate1 and @teammate2

## 🎯 Today

• Migrate user database to new schema (JIRA-456) - Target: EOD
• Pair with @teammate3 on webhook integration - 11am session
• Write deployment runbook for profile API

## 🚧 Blockers

• Need staging database access for migration testing - @infra-team

## 📎 Links

• [PR #789](link) | [JIRA Sprint Board](link)
```

**Thread-Based Standup:**

- Post standup as Slack thread parent message
- Teammates reply in thread with questions or offers to help
- Keep discussion contained, surface key decisions to channel
- Use emoji reactions for quick acknowledgment (👀 = read, ✅ = noted, 🤝 = I can help)

**Video Async Standup:**

- Record 2-3 minute Loom video walking through work
- Post video link with text summary (for skimmers)
- Useful for demoing UI work, explaining complex technical issues
- Include automatic transcript for accessibility

**Rolling 24-Hour Standup:**

- Post update anytime within 24h window
- Mark as "posted" when shared (use emoji status)
- Accommodates distributed teams across timezones
- Weekly summary thread consolidates key updates

## Impediment Prioritization Skill

<!-- source: github/awesome-copilot skills/impediment-prioritization/SKILL.md#scoring-rubric-1-10-scales -->

### Scoring Rubric (1–10 scales)

Score each impediment's countermeasure against all four criteria. See references/scoring-rubric.md for anchoring examples at the 1 / 5 / 10 levels across multiple domains (platform engineering, security, SRE, application development, governance).

| Criterion | Scale | Definition |
|-----------|-------|------------|
| **Return on Investment (ROI)** | 1 = low, 10 = high | Efficiency gain delivered by the countermeasure to this step AND to the overall value stream. Not purely financial — weight throughput, cycle-time reduction, defect removal, user / developer experience, and compliance lift. |
| **Cost to Implement** | 1 = inexpensive, 10 = very expensive | Human capital (salary + time of people needed) plus any purchases, licenses, or infrastructure required to implement the countermeasure. |
| **Ease of Deployment** | 1 = extremely hard, 10 = very easy | Remediation effort required to actually deploy the countermeasure end-to-end. Reflects technical complexity, change-management burden, and rollback risk. |
| **Risk Factor** | 1 = low risk, 10 = very high risk | Risk weighted on impact to the overall value stream if the countermeasure goes wrong, stalls, or is deferred. |

Every score must be accompanied by a one-line rationale. When a score is an estimate rather than drawn from explicit data, mark the rationale with `(estimated)`.
