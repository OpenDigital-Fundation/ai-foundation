# Marketing foundations, laws of brand growth and growth metrics

Reference for `marketing:campaign-planning`. Models to plan with and the evidence behind them. Separate empirical regularities (Ehrenberg-Bass laws, Binet and Field) from planning frameworks (4Ps, AIDA, AARRR), and both from the numbers of this business.

## Foundations

| Model | Components | Use |
|---|---|---|
| Marketing mix, 4Ps (McCarthy, popularised by Kotler) | Product, price, place, promotion | Check that every element supports the positioning |
| 7Ps (Booms and Bitner) | 4Ps plus people, process, physical evidence | Services, where delivery is the product |
| 4Cs (Lauterborn) | Consumer, cost, convenience, communication | The 4Ps from the customer's side |
| STP | Segmentation, targeting, positioning | Choose whom to serve and the place to own in their mind |
| 3Cs (Ohmae) | Company, customers, competitors | Situation analysis |
| 5As (Kotler, Marketing 4.0) | Aware, appeal, ask, act, advocate | Map the connected customer path and advocacy |
| Jobs to be done, value proposition canvas | Jobs, pains, gains | See `product:product-management` (`references/strategy-frameworks.md`) |
| Marketing myopia (Levitt) | Define the business by the customer need, not the product | Avoid being displaced by substitutes |

## Laws of brand growth (Ehrenberg-Bass Institute; Byron Sharp, *How Brands Grow*)

| Regularity | What it says | Implication |
|---|---|---|
| Double jeopardy | Smaller brands have far fewer buyers, and those buyers are slightly less loyal | Growth comes mainly from more buyers (penetration), not from more loyalty |
| Duplication of purchase | A brand shares customers with competitors in line with their size | Competition is broader than "our segment"; partitions show only where sharing deviates |
| Mental availability | Being thought of in buying situations | Build and refresh memory structures across many buyers |
| Physical availability | Being easy to find and buy | Distribution, presence and ease of purchase |
| Category entry points (CEPs) | The needs, occasions and cues that start a purchase | Link the brand to many relevant CEPs |
| Distinctive brand assets | Colours, shapes, characters, sounds and taglines that identify the brand | Use them consistently and measure their fame and uniqueness |
| 95-5 rule (B2B, John Dawes) | In many B2B categories only about 5% of buyers are in market in a given quarter | Most spend should build memory among future buyers; the ratio varies by category |

These regularities are well replicated across categories and countries; they describe markets on average and say little about one campaign.

## Brand building and sales activation (Les Binet and Peter Field, IPA)

- **Brand building** creates memory and preference and pays back over months and years; **sales activation** triggers response now and decays quickly.
- Their analyses of IPA effectiveness cases found the best results with roughly **60% brand, 40% activation** for consumer brands, with a lower brand share reported for B2B. The ratio depends on category, brand size and stage; treat it as a starting hypothesis.
- **Excess share of voice (ESOV)** = share of voice − share of market. Brands with positive ESOV tend to gain share over time; their rule of thumb is around half a point of annual share growth per ten points of ESOV.
- Short-term metrics (clicks, ROAS) favour activation by construction; check long-term effects before cutting brand spend.

## Funnels, loops and frameworks for digital growth

| Model | Stages | Use |
|---|---|---|
| AIDA | Attention, interest, desire, action | Structure a message or page |
| AARRR, pirate metrics (Dave McClure) | Acquisition, activation, retention, revenue, referral | Instrument a product's growth; fix retention before buying acquisition |
| RACE (Smart Insights) | Reach, act, convert, engage | Plan digital activity across the lifecycle |
| RFM | Recency, frequency, monetary value | Segment customers for lifecycle marketing |
| Flywheel | Attract, engage, delight, with customers feeding new demand | Relationship-led growth |
| Growth loops | An output (content, invites, data) becomes the next input | Find self-reinforcing mechanisms; measure loop cycle time and conversion |
| Product-led growth | The product drives acquisition, activation and expansion | Self-serve SaaS; needs fast time to value |

## Metrics and their traps

| Metric | Definition | Trap |
|---|---|---|
| CAC | Sales and marketing cost ÷ new customers in the period | Leaving out salaries, tools or onboarding cost |
| LTV (CLV) | Simple form: average revenue per account × gross margin ÷ churn rate | Using revenue instead of margin; assuming churn is constant |
| LTV/CAC | Value per customer over acquisition cost (often 3:1 is cited as healthy) | A ratio without payback time hides cash risk |
| CAC payback | CAC ÷ (monthly revenue per account × gross margin), in months | — |
| ROAS | Attributed revenue ÷ ad spend | Not profit; attribution overstates channels that harvest existing demand |
| ROI | (Gain − cost) ÷ cost | Define gain as margin, not revenue |
| Conversion rate | Completions ÷ eligible visitors or users | Optimising one step can lower downstream quality |
| Churn and retention | Customers or revenue lost (kept) in a period; net revenue retention includes expansion | Logo churn and revenue churn tell different stories |
| NPS | % promoters (9–10) − % detractors (0–6) | Stated intention, not behaviour; small samples swing widely |
| Share of voice / share of market | The brand's share of category advertising or attention / of category sales | Compare with each other (ESOV), not alone |
| Brand awareness | Prompted or unprompted recall among category buyers | Measure among category buyers, linked to CEPs |

Followers are not an audience, and an isolated conversion lift does not prove sustainable growth. Prefer incrementality tests (geo or holdout experiments, media mix models) over last-click attribution for budget decisions.

## How the pieces connect

1. Understand the market: PESTEL, five forces, research, STP.
2. Choose a strategy and position: Ansoff, VRIO, Blue Ocean, value proposition.
3. Build the brand and audience: Ehrenberg-Bass, Binet and Field, brand theory (`brand:brand-identity`, `references/brand-theory.md`).
4. Acquire and keep customers: 4Ps, AIDA, AARRR, CRO, RFM.
5. Measure and improve: the metrics above, incrementality tests, and Goodhart's law (`operations:project-management`).
