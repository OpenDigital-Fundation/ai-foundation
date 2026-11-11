# Financial analysis — derived guides

Part of `finance:financial-analysis`.

## Startup Financial Modeling

<!-- source: wshobson/agents plugins/startup-business-analyst/skills/startup-financial-modeling/SKILL.md#core-components -->

### Core Components

#### Revenue Model

**Cohort-Based Projections:**
Build revenue from customer acquisition and retention by cohort.

**Formula:**

```
MRR = Σ (Cohort Size × Retention Rate × ARPU)
ARR = MRR × 12
```

**Key Inputs:**

- Monthly new customer acquisitions
- Customer retention rates by month
- Average revenue per user (ARPU)
- Pricing and packaging assumptions
- Expansion revenue (upsells, cross-sells)

#### Cost Structure

**Operating Expenses Categories:**

1. **Cost of Goods Sold (COGS)**
   - Hosting and infrastructure
   - Payment processing fees
   - Customer support (variable portion)
   - Third-party services per customer

2. **Sales & Marketing (S&M)**
   - Customer acquisition cost (CAC)
   - Marketing programs and advertising
   - Sales team compensation
   - Marketing tools and software

3. **Research & Development (R&D)**
   - Engineering team compensation
   - Product management
   - Design and UX
   - Development tools and infrastructure

4. **General & Administrative (G&A)**
   - Executive team
   - Finance, legal, HR
   - Office and facilities
   - Insurance and compliance

#### Cash Flow Analysis

**Components:**

- Beginning cash balance
- Cash inflows (revenue, fundraising)
- Cash outflows (operating expenses, CapEx)
- Ending cash balance
- Monthly burn rate
- Runway (months of cash remaining)

**Formula:**

```
Runway = Current Cash Balance / Monthly Burn Rate
Monthly Burn = Monthly Revenue - Monthly Expenses
```

#### Headcount Planning

**Role-Based Hiring Plan:**
Track headcount by department and role.

**Key Metrics:**

- Fully-loaded cost per employee
- Revenue per employee
- Headcount by department (% of total)

**Typical Ratios (Early-Stage SaaS):**

- Engineering: 40-50%
- Sales & Marketing: 25-35%
- G&A: 10-15%
- Customer Success: 5-10%

## Startup Metrics Framework

<!-- source: wshobson/agents plugins/startup-business-analyst/skills/startup-metrics-framework/SKILL.md#metric-tracking-best-practices,consumer-mobile-metrics -->

### Consumer/Mobile Metrics

#### Engagement Metrics

**DAU (Daily Active Users)**
Unique users active each day

**MAU (Monthly Active Users)**
Unique users active each month

**DAU/MAU Ratio**

```
DAU/MAU = DAU / MAU
```

**Benchmarks:**

- > 50% = Exceptional (daily habit)
- 20-50% = Good
- < 20% = Weak engagement

**Session Frequency**
Average sessions per user per day/week

**Session Duration**
Average time spent per session

#### Retention Curves

**Day 1 Retention:** % users who return next day
**Day 7 Retention:** % users active 7 days after signup
**Day 30 Retention:** % users active 30 days after signup

**Benchmarks (Day 30):**

- > 40% = Excellent
- 25-40% = Good
- < 25% = Weak

**Retention Curve Shape:**

- Flattening curve = good (users becoming habitual)
- Steep decline = poor product-market fit

#### Viral Coefficient (K-Factor)

```
K-Factor = Invites per User × Invite Conversion Rate
```

**Example:**
10 invites/user × 20% conversion = 2.0 K-factor

**Benchmarks:**

- K > 1.0 = Viral growth
- K = 0.5-1.0 = Strong referrals
- K < 0.5 = Weak virality

### Metric Tracking Best Practices

#### Data Infrastructure

**Requirements:**

- Single source of truth (analytics platform)
- Real-time or daily updates
- Automated calculations
- Historical tracking

**Tools:**

- Mixpanel, Amplitude (product analytics)
- ChartMogul, Baremetrics (SaaS metrics)
- Looker, Tableau (BI dashboards)

#### Reporting Cadence

**Daily:**

- MRR, active users
- Sign-ups, conversions

**Weekly:**

- Growth rates
- Retention cohorts
- Sales pipeline

**Monthly:**

- Full metric suite
- Board reporting
- Investor updates

**Quarterly:**

- Trend analysis
- Benchmarking
- Strategy review

#### Common Mistakes

**Mistake 1: Vanity Metrics**
Don't focus on:

- Total users (without retention)
- Page views (without engagement)
- Downloads (without activation)

Focus on actionable metrics tied to value.

**Mistake 2: Too Many Metrics**
Track 5-7 core metrics intensely, not 50 loosely.

**Mistake 3: Ignoring Unit Economics**
CAC and LTV are critical even at seed stage.

**Mistake 4: Not Segmenting**
Break down metrics by customer segment, channel, cohort.

**Mistake 5: Gaming Metrics**
Optimize for real business outcomes, not dashboard numbers.
