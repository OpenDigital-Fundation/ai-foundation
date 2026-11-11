# People operations — derived guides

Part of `operations:people-operations`.

## Brag Sheet — Work Impact Writer

<!-- source: github/awesome-copilot skills/brag-sheet/SKILL.md#performance-review-prep,entry-format -->

### Entry Format

Every entry uses impact-first framing with three required parts:

```
Did [action] → [result/impact] → [evidence]
```

**Do not output an entry unless it includes all three parts.** If evidence is missing, ask for it or mark as "(evidence needed)".

#### Anti-Patterns

| ❌ Don't | ✅ Do instead |
|---------|--------------|
| "Fixed a bug in auth" | "Fixed token refresh race condition → eliminated 401s affecting 12% of API calls → PR #247" |
| "Worked on dashboards" | "Built latency dashboard in Grafana → on-call detects P95 spikes in <2min → deployed to prod" |
| Invent a metric: "saved 40% of eng time" | Ask: "Do you have a rough estimate, or should I keep this qualitative?" |
| One entry per commit | Group related commits into one entry with highest-impact framing |
| Passive voice: "The pipeline was improved" | Active voice: "Built CI matrix → caught Windows-only bug before release" |
| List technologies used | State the outcome: "Migrated 4 services to IaC → deploy time 45min → 8min" |
| Silently drop weak entries | Mark `(evidence needed)` and present for user to fill in |

### Performance Review Prep

When the user is preparing for a performance review (Connect, annual review, etc.):

#### Structure

1. **Gather** — collect entries from the work log (or backfill using the workflow above)
2. **Select** — pick the top 3–5 highest-impact items
3. **Rewrite** each item with three parts:
   - **What I did** — the specific action
   - **Why it mattered** — who benefited, what changed
   - **Proof** — PR number, metric delta, dashboard link, customer outcome
4. **Organize** by impact theme (not chronologically):
   - Delivering results / operational excellence
   - Customer / team impact
   - Collaboration / mentoring / leadership
   - Growth / learning
5. **Ask for gaps** — if evidence is missing, prompt the user: "What metric changed?", "Who was unblocked?", "What's the PR or incident ID?"

#### Strong vs weak entries

| ✅ Strong | ❌ Weak |
|----------|--------|
| Outcome-first, quantified | Activity list ("worked on X") |
| Tied to customer/team impact | No beneficiary mentioned |
| Includes evidence (PR, metric) | No measurable result |
| Shows ownership or leadership | Pure task completion |

#### Narrative format

For longer narrative sections, use STAR: **S**ituation → **T**ask → **A**ction → **R**esult.

For Microsoft employees using the Connect preset, frame entries around Core Priorities: delivering results, customer obsession, teamwork, and growth mindset.

## Mentoring Socratique

<!-- source: github/awesome-copilot skills/mentoring-juniors/SKILL.md#teaching-techniques -->

### Teaching Techniques

#### Rubber Duck Debugging
> "Explain your code to me line by line, as if I were a rubber duck."

The act of verbalizing forces the learner to think critically about each step and often reveals the bug on its own.

#### The 5 Whys
> "The code crashes → Why? → The variable is null → Why? → It wasn't initialized → Why? → ..."

Keep asking "why" until the root cause is found. Usually 5 levels deep is enough.

#### Minimal Reproducible Example
> "Can you isolate the problem in 10 lines of code or less?"

Forces the learner to strip away irrelevant complexity and focus on the core issue.

#### Guided Red-Green-Refactor
> "First, write a test that fails. What should it check for?"

1. **Red**: Write a failing test that defines the expected behavior
2. **Green**: Write the minimum code to make the test pass
3. **Refactor**: Improve the code while keeping tests green

---
