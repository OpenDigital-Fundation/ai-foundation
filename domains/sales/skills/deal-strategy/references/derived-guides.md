# Deal strategy — derived guides

Part of `sales:deal-strategy`.

## customer-success-manager

<!-- source: davila7/claude-code-templates cli-tool/components/agents/business-marketing/customer-success-manager.md#customer-success-reference-points -->

### Customer Success Reference Points

Use the following as illustrative reference points to validate against — or replace with — the customer's own targets; do not assume they are already achieved or universally applicable:
- NPS score, CSAT, and support response time targets
- Churn rate and renewal rate targets
- Adoption rate and time-to-value targets
- Net Revenue Retention (NRR) as a headline expansion/retention metric, alongside upsell and advocacy goals

NRR and GRR formulas (standard SaaS definitions — apply with the customer's own starting ARR and confirmed period figures, never invented ones):
- `NRR = (Starting ARR + Expansion − Contraction − Churn) / Starting ARR`
- `GRR = (Starting ARR − Contraction − Churn) / Starting ARR`

GRR is retention-only (excludes expansion) and caps at 100%, so track it alongside NRR — a healthy NRR can otherwise mask underlying churn that expansion revenue is offsetting.

#### Illustrative Health-Score Rubric

A composite health score is a template to adapt to the customer's own data and priorities — never present it as a fact about a specific account until the user has confirmed the underlying inputs and weighting. A common structure:

| Dimension | Example weight | Signals |
|---|---|---|
| Product usage / adoption | 30% | Login frequency, core-feature usage, active-seat ratio |
| Engagement / relationship | 20% | Meeting cadence, stakeholder breadth, champion responsiveness |
| Sentiment (NPS / CSAT) | 20% | Survey scores, qualitative feedback trend |
| Support health | 15% | Ticket volume, severity mix, escalation velocity, resolution time |
| Commercial / financial | 15% | Payment timeliness, contract status, expansion/contraction history |

Band the resulting composite score (e.g., red/yellow/green or 0-100) against thresholds the user confirms, not assumed defaults.

## sales-automator

<!-- source: davila7/claude-code-templates cli-tool/components/agents/business-marketing/sales-automator.md#compliance-anti-spam-requirements -->

### Compliance & Anti-Spam Requirements

Every email sequence must include:
- Accurate sender name/address (no spoofed domains or generic addresses posing as a company)
- Non-deceptive subject lines (no misleading "Re:", fake urgency, or false claims)
- A physical mailing address (CAN-SPAM requirement)
- A working, one-click or clearly stated opt-out mechanism in every email, honored within 10 business days
- For EU/UK/Canadian recipients: ask the user to confirm the legal basis (GDPR legitimate interest for B2B, or CASL consent/implied consent) before drafting; do not assume compliance
- Never fabricate urgency, false scarcity, or misrepresent the sender's identity/affiliation

If the user hasn't confirmed how the contact list was sourced, ask before drafting — flag purchased/scraped lists as a compliance risk requiring the user's own legal review. Hand off jurisdiction-specific compliance drafting/audits to legal-advisor.

## Enterprise Onboarding

<!-- source: github/awesome-copilot skills/gtm-enterprise-onboarding/SKILL.md#common-mistakes -->

### Common Mistakes

**1. Starting customer onboarding before internal alignment**
   - Wastes first 2-3 weeks, creates confusion, kills credibility

**2. Not identifying real project owner upfront**
   - Discovers it Week 4, has to restart or deal stalls

**3. Overcommitting on timeline without technical requirements**
   - Discovers blockers mid-implementation, misses deadline

**4. No internal communication hub**
   - Decisions don't propagate across teams, rework happens

**5. Treating go-live as project complete**
   - Adoption cliff at Week 12, account at risk

**6. Sequential tracks instead of parallel**
   - Implementation takes twice as long, customer loses momentum

**7. No ongoing metrics post go-live**
   - Discovers adoption issues too late to save account

---
