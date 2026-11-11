---
name: financial-analysis
description: "Use for financial modelling and planning: three-statement and unit-economics models, forecasts and budgets, scenario analysis, variance analysis, pricing models and investment memos."
license: MIT
metadata:
  domain: finance
  status: experimental
---
# Financial analysis

Turn numbers into a decision, with assumptions anyone can audit.

## 1. Frame the question
The decision the analysis informs, the horizon, and the output (model, forecast, memo).

## 2. Gather and check inputs
Actuals from the source of truth, with dates; flag gaps and one-offs. Keep inputs separate from calculations.

## 3. Build the model
Assumptions on one sheet, clearly labelled; drivers (volume, price, conversion, churn, headcount) flowing into the statements or unit economics; no hard-coded numbers inside formulas. Check that statements balance.

## 4. Stress it
Base, downside and upside scenarios; sensitivity on the two or three drivers that matter most; break-even and runway.

## 5. Communicate
Lead with the answer and the recommendation, then the drivers, risks and what would change the conclusion. For spreadsheet files use `documents:office-documents`. This is analysis, not investment or tax advice.

## References

Load only what the task needs:

- [`references/role-guide.md`](references/role-guide.md) — the role profile this skill was distilled from: mission, critical rules, deliverable templates and examples
- [`references/fpa.md`](references/fpa.md) — covers FP&A Analyst; 1. Strategic Context; 2. Key Financial Targets; 3. Revenue Plan
- [`references/pricing.md`](references/pricing.md) — covers Pricing Analyst; Executive Summary; Cost Analysis; Market Context
- [`references/investment-research.md`](references/investment-research.md) — covers Investment Researcher; Executive Summary; Investment Thesis; Bear Case & Risk Factors
- [`references/derived-guides.md`](references/derived-guides.md) — sections merged from other collections where this skill had no equivalent: Core Components; Metric Tracking Best Practices; Consumer/Mobile Metrics
