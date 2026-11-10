# Measuring UX

Reference for `ux:user-research`. Pick measures before the study, tie each to a decision, and report them with the number of participants and a confidence interval. Never invent or estimate results that were not collected.

## Task-level measures (usability tests)

| Measure | How | Notes |
|---|---|---|
| Task success rate | Share of participants who complete the task without help, against a success criterion defined beforehand | Report partial success separately; with small samples, give an interval (adjusted Wald) |
| Time on task | Time from start to success, successful attempts only | Skewed: report the geometric mean or median |
| Errors | Count of defined error types per task | Define what counts as an error before the session |
| SEQ (Single Ease Question) | "Overall, how difficult or easy was this task?" on a 7-point scale, right after each task | Cheap and sensitive; compare tasks and versions |

## Questionnaire measures (after a session or in the product)

| Instrument | Format | Scoring |
|---|---|---|
| SUS (System Usability Scale) | 10 statements, 5-point agreement, alternating positive and negative | Odd items: score − 1; even items: 5 − score; sum × 2.5 → 0–100. About 68 is the commonly cited average; it is not a percentage |
| UMUX-Lite | 2 items, 7-point | Short substitute for SUS in product surveys |
| UEQ / UEQ-S | 26 (or 8) semantic-differential items | Attractiveness, perspicuity, efficiency, dependability, stimulation, novelty; compare with the published benchmark |
| NPS | 0–10 likelihood to recommend | Loyalty signal, not usability; do not use it to judge a design change |

## Product-level frameworks

**HEART** (Google): Happiness, Engagement, Adoption, Retention, Task success. For each relevant category, write **Goals → Signals → Metrics**: what the team wants, what behaviour would show it, and the metric that tracks the signal. Skip categories that do not matter to the decision.

Behavioural product metrics (funnels, retention, feature adoption) say *what* happens; pair them with research that says *why*.

## Choosing measures

| Decision | Measures |
|---|---|
| Is the new flow better than the old? | Success rate, time on task, SEQ per task, in a within- or between-subjects comparison |
| Is the product usable overall? | SUS or UMUX-Lite, plus the top task failures |
| Did a release improve the experience? | HEART metrics chosen beforehand, compared with a baseline period |
| Where do people struggle? | Qualitative test findings with severity; numbers only support them |

## Where measurement fits in the design process

1. **Discover** — interviews, observation, jobs to be done and journeys (`references/jobs-and-journeys.md`).
2. **Structure** — information architecture, card sorting, tree testing; Hick's and Jakob's laws guide grouping and conventions.
3. **Interaction** — heuristics and principles (`ux:usability-review`, `references/heuristics-and-laws.md`).
4. **Visual language** — Gestalt, hierarchy and the design system (`ui:visual-design`, `ui:design-system`).
5. **Accessibility** — WCAG 2.2 and local standards (`accessibility:wcag-accessibility`, `references/standards-map.md`).
6. **Validate with people** — task tests and the measures above; repeat after changes.
