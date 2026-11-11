---
name: internal-comms
description: "Use when writing internal communications: status reports, leadership updates, incident notices, company newsletters, FAQs and project updates, in the formats and tone a company expects."
license: MIT
metadata:
  domain: documents
  status: experimental
---
<!-- Modified by OpenDigital from anthropics/skills (Apache-2.0). See PROVENANCE.yaml in this domain. -->

# Internal communications

## When to use this skill
To write internal communications, use this skill for:
- 3P updates (Progress, Plans, Problems)
- Company newsletters
- FAQ responses
- Status reports
- Leadership updates
- Project updates
- Incident reports

## How to use this skill

To write any internal communication:

1. **Identify the communication type** from the request
2. **Load the appropriate guideline file** from the `examples/` directory:
    - `examples/3p-updates.md` - For Progress/Plans/Problems team updates
    - `examples/company-newsletter.md` - For company-wide newsletters
    - `examples/faq-answers.md` - For answering frequently asked questions
    - `examples/general-comms.md` - For anything else that doesn't explicitly match one of the above
3. **Follow the specific instructions** in that file for formatting, tone, and content gathering

If the communication type doesn't match any existing guideline, ask for clarification or more context about the desired format.

## Keywords
3P updates, company newsletter, company comms, weekly update, faqs, common questions, updates, internal comms

## References

Load only what the task needs:

- [`references/derived-guides.md`](references/derived-guides.md) — sections merged from other collections where this skill had no equivalent: Common email types; Common Difficult Scenarios; Preparation Phase; SBI Examples for Software Teams; Example Scenarios; Technical vs Non-Technical Communication
