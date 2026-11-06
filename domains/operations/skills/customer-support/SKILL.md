---
name: customer-support
description: "Use for customer support and success work: answering tickets, writing help-center replies and macros, escalations, onboarding and health checks for accounts, and turning support trends into product feedback."
license: MIT
metadata:
  domain: operations
  status: experimental
---
# Customer support

Resolve the customer's problem on the first reply when you can, and leave a trail the next person can follow.

## Each ticket

1. **Understand:** restate the problem in one line; find the account, plan, history and any open incident before replying. Ask only for what you cannot look up.
2. **Classify:** question, bug, billing, access, feature request or complaint; and urgency (blocked, degraded, inconvenienced).
3. **Resolve or route:** answer with exact steps and links; if it is a bug, reproduce it and file it with steps, expected and actual behaviour (`workflow:issue-triage`); billing goes to `finance:billing-operations`; security reports go to `security:security-audit` and are never discussed publicly.
4. **Reply:** plain language, the answer first, one action per step, honest about what you do not know and when they will hear back. Never promise dates or refunds you cannot authorise.
5. **Close the loop:** confirm resolution, tag the ticket, and update the help-center article or macro if the answer was missing.

## Patterns

- Repeated questions become help-center articles or macros.
- Trends (top contact reasons, rising bugs) go to product weekly with counts and example tickets.
- Accounts at risk (repeated issues, usage drop, negative replies) go to customer success with a short history.

Detailed response playbooks, tone guides, customer-success health checks and onboarding are in the references.

## References

Load only what the task needs:

- [`references/responding.md`](references/responding.md)
- [`references/service.md`](references/service.md)
- [`references/customer-success.md`](references/customer-success.md)
