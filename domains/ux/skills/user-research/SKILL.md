---
name: user-research
description: Use when the team needs evidence about users before or after building - planning interviews, usability tests or surveys, recruiting participants, writing a study protocol, synthesising findings into personas, journeys and insights, or deciding what to build next from observed behaviour rather than opinion.
license: MIT
metadata:
  domain: ux
  status: experimental
---

# User research

Replace opinions about users with evidence from users. Research is worth doing when its answer would change what gets built; otherwise skip it and say why.

## 1. Frame the question

Write the decision the research must inform and the one to three questions that decide it ("Do first-time buyers understand delivery fees before checkout?"). If no decision depends on the answer, stop.

## 2. Pick the method

| Need | Method |
|---|---|
| Why people do something; unknown problems | Interviews (5–8 per segment) |
| Whether people can do something | Moderated or unmoderated usability test (5 per round finds most issues) |
| How many people think or do something | Survey or product analytics (needs a large enough sample) |
| How people group or name things | Card sorting, tree testing |
| How behaviour unfolds over time | Diary study, session replays |

Prefer observing behaviour over asking for opinions or predictions.

## 3. Plan the study

Write the plan with [references/research-playbook.md](references/research-playbook.md): objectives, participant criteria and screener, protocol (tasks or interview guide with neutral, open questions), consent and data handling, schedule. Ask the user for access to real participants; never fabricate participants, quotes or results.

## 4. Run and record

Stay neutral: do not lead, do not explain the design, ask "what are you expecting here?" instead of "is that clear?". Record what people did and said, separately from your interpretation. Redact personal data in notes.

## 5. Synthesise

Cluster observations into themes, count how many participants showed each, and separate:

- **Findings** — what was observed, with frequency and evidence.
- **Insights** — why it happens.
- **Recommendations** — what to change, ranked by severity and frequency.

Produce personas or journey maps only when a decision needs them, built from the data you collected.

## 6. Hand off

Feed recommendations into `workflow:brainstorming` or the relevant spec. Interface-level problems go to `ux:usability-review`; visual ones to `ui:visual-design`; accessibility barriers to `accessibility:wcag-accessibility`.

## Further references

Guides merged from github/awesome-copilot; load only what the task needs:

- [`references/jobs-and-journeys.md`](references/jobs-and-journeys.md)
- [`references/ux-measurement.md`](references/ux-measurement.md) — task success, time on task, SEQ, SUS, UEQ, HEART, and where measurement fits in the design process
