---
name: email-marketing
description: "Use when planning or writing marketing email: lifecycle and nurture sequences, newsletters, segmentation, deliverability, subject lines and A/B tests, and operating email tools."
license: MIT
metadata:
  domain: marketing
  status: experimental
---
# Email marketing

Send fewer, more relevant emails that people expect and act on.

## 1. Define the programme
Goal per flow (activation, retention, conversion, win-back), audience segment, trigger or cadence, and the metric (clicks, conversions, revenue per send; opens are directional only).

## 2. Build the sequence
For each email: one purpose, one call to action, subject line and preview text, timing relative to the trigger, and the exit condition (converted, unsubscribed, moved segment). Map branches for engaged versus silent recipients.

## 3. Write
Lead with the reader's benefit, keep it scannable, make the CTA a verb, and match the brand voice (`brand:brand-voice`). Write two subject-line variants for testing.

## 4. Protect deliverability
Consent and easy unsubscribe, authenticated domain (SPF, DKIM, DMARC), list hygiene (suppress bounces and long-inactive contacts), and steady sending volume.

## 5. Test and report
A/B test one variable at a time with enough volume to decide; report against the goal metric and roll the winner into the default.

## References

Load only what the task needs:

- [`references/role-guide.md`](references/role-guide.md) — the role profile this skill was distilled from: mission, critical rules, deliverable templates and examples
- [`references/operations.md`](references/operations.md) — covers Email Ops
- [`references/derived-guides.md`](references/derived-guides.md) — sections merged from other collections where this skill had no equivalent: Email Sequence Strategy; Email Copy Guidelines
