---
name: usability-review
description: Use when evaluating whether an existing interface, flow or prototype is easy to use without running a study - a heuristic evaluation, a cognitive or persona walkthrough of a task, a review of a sign-up, checkout or onboarding flow, or finding where users would get stuck, confused or make errors.
license: MIT
metadata:
  domain: ux
  status: experimental
---

# Usability review

Find where a real person would get stuck, before they do. This is an expert review, not a substitute for testing with users (`ux:user-research`); say so in the report.

## 1. Fix the scope

Name the flow (e.g. "first purchase on mobile"), the persona attempting it, their goal and context (device, rush, expertise), and the start and success states. Get the interface itself: a URL, a running app, screenshots or the code that renders it.

## 2. Walk the task

For each step, as the persona, ask the four walkthrough questions:

1. Will they try to do the right thing (do they know this step is needed)?
2. Will they notice the control that does it?
3. Will they connect that control with their goal (labels, icons, placement)?
4. After acting, will they see that it worked and what comes next?

Any "no" is a finding. The full persona method is in [references/persona-walkthrough.md](references/persona-walkthrough.md).

## 3. Check the heuristics

Then sweep the screens against Nielsen's ten heuristics: visibility of system status; match with the real world; user control and freedom (undo, cancel, back); consistency and standards; error prevention; recognition over recall; flexibility and efficiency; aesthetic and minimalist design; help users recognise, diagnose and recover from errors; help and documentation.

For implementation-level interaction rules (navigation, forms, feedback, loading and empty states), query the guideline database in `ui:design-system` (`--domain ux`).

Each finding names its heuristic, principle or law; the tables, the evidence weight of each kind and the caveats are in [references/heuristics-and-laws.md](references/heuristics-and-laws.md).

## 4. Report

For each finding: where (screen, element), what happens, which persona and step it blocks, the heuristic or walkthrough question it fails, severity (blocker, major, minor) and the smallest fix. Order by severity, then by how early in the flow it occurs. End with what works well and what only a real test can answer.
