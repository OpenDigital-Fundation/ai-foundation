# Campaign planning — derived guides

Part of `marketing:campaign-planning`.

## marketing-attribution-analyst

<!-- source: davila7/claude-code-templates cli-tool/components/agents/business-marketing/marketing-attribution-analyst.md#technical-implementation -->

### Technical Implementation

#### 1. Tracking Infrastructure Setup

As of 2026, third-party cookie deprecation in Chrome has been reversed (Google abandoned Privacy Sandbox's forced deprecation in 2024/2025, and shut down Privacy Sandbox trials in October 2025) — Chrome no longer blocks third-party cookies by default, while Safari and Firefox continue to block them by default. This means signal loss is real but uneven across browsers, not the universal "cookiepocalypse" once expected. The practical response is the same regardless: reduce reliance on third-party cookies via first-party data, server-side tracking, and consent-aware measurement.

Confirm with the user whether these are already in place before assuming a client-side-only setup:
- **Server-side tagging** (e.g., server-side Google Tag Manager) to reduce data loss from ad blockers and browser restrictions, and to control what leaves the first-party domain.
- **Google Consent Mode v2** — required by Google for applicable Google Ads and Analytics features serving EEA traffic; it is not a universal legal requirement for every EEA-facing site. Confirm which Google products and consent-mode implementation the user has, then verify that the consent management platform sends the required signals, including `ad_user_data`, `ad_personalization`, `analytics_storage`, and `ad_storage`, correctly.
- **Enhanced Conversions / server-side conversion APIs** (Google Ads Enhanced Conversions, Meta Conversions API, TikTok Events API) — where consent and applicable regional rules permit, these can improve match rate and signal quality by sending hashed first-party identifiers server-to-server. Confirm that the implementation propagates consent state and suppresses ineligible events and identifiers; hashing and server-side delivery do not bypass consent requirements.

```javascript
// Google Analytics 4 Enhanced Ecommerce tracking
gtag('event', 'purchase', {
  transaction_id: '12345',
  value: 25.42,
  currency: 'USD',
  items: [{
    item_id: 'SKU123',
    item_name: 'Product Name',
    category: 'Category',
    quantity: 1,
    price: 25.42
  }]
});

// UTM parameter tracking for campaign attribution
function trackCampaignSource() {
  const urlParams = new URLSearchParams(window.location.search);
  const attribution = {
    utm_source: urlParams.get('utm_source'),
    utm_medium: urlParams.get('utm_medium'),
    utm_campaign: urlParams.get('utm_campaign'),
    utm_content: urlParams.get('utm_content'),
    utm_term: urlParams.get('utm_term')
  };
  
  // Store attribution data for later conversion tracking
  localStorage.setItem('attribution', JSON.stringify(attribution));
}
```

#### 2. Multi-Touch Attribution Analysis
```sql
-- Customer journey attribution analysis
WITH customer_touchpoints AS (
    SELECT 
        customer_id,
        channel,
        campaign,
        touchpoint_timestamp,
        conversion_timestamp,
        revenue,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id 
            ORDER BY touchpoint_timestamp
        ) as touchpoint_sequence
    FROM marketing_touchpoints
    WHERE touchpoint_timestamp <= conversion_timestamp
),
attribution_weights AS (
    SELECT 
        customer_id,
        channel,
        campaign,
        revenue,
        -- Time-decay attribution (exponential decay)
        revenue * EXP(-0.1 * (conversion_timestamp - touchpoint_timestamp) / 86400) as attributed_revenue,
        -- U-shaped attribution
        CASE 
            WHEN touchpoint_sequence = 1 THEN revenue * 0.4  -- First touch
            WHEN touchpoint_sequence = MAX(touchpoint_sequence) OVER (PARTITION BY customer_id) THEN revenue * 0.4  -- Last touch
            ELSE revenue * 0.2 / (COUNT(*) OVER (PARTITION BY customer_id) - 2)  -- Middle touches
        END as u_shaped_revenue
    FROM customer_touchpoints
)
SELECT 
    channel,
    campaign,
    SUM(attributed_revenue) as time_decay_attributed_revenue,
    SUM(u_shaped_revenue) as u_shaped_attributed_revenue,
    COUNT(DISTINCT customer_id) as attributed_conversions
FROM attribution_weights
GROUP BY channel, campaign
ORDER BY time_decay_attributed_revenue DESC;
```

#### 3. Marketing Mix Modeling (MMM)

Modern MMM tooling is now the dominant approach in practice over ad hoc custom models, since purpose-built packages incorporate prior knowledge about known effects like saturation and adstock along with validated uncertainty estimates. The two current standard open-source tools take different approaches: **Google Meridian** (GA'd 2024-2025 as the recommended successor to LightweightMMM, with a no-code Scenario Planner released February 2026) is a genuinely Bayesian MMM that reports posterior credible intervals, while **Meta's Robyn** uses ridge regression with automated hyperparameter optimization and reports bootstrapped confidence intervals rather than Bayesian credible intervals — choose between them based on the user's data and whether they need explicit Bayesian priors. The illustrative RandomForest snippet below is useful for a quick feature-importance read on smaller datasets, but for a production MMM recommend Meridian or Robyn rather than a custom model, since both include adstock/saturation transforms and validated diagnostics out of the box.

```python
# Statistical modeling for marketing attribution
# Illustrative example only — for production MMM, prefer Google Meridian
# (github.com/google/meridian, Bayesian with posterior credible intervals) or
# Meta's Robyn (ridge regression with bootstrapped confidence intervals) —
# both include validated adstock/saturation transforms out of the box.
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

def build_marketing_mix_model(marketing_data):
    """
    Build MMM to understand incremental impact of each channel
    """
    # Feature engineering
    features = [
        'tv_spend', 'digital_spend', 'social_spend', 'search_spend',
        'display_spend', 'email_spend', 'influencer_spend'
    ]
    
    # Missing weekly spend observations must be resolved before adstock: calculate_adstock
    # carries values forward recursively, so a single NaN poisons every subsequent period.
    # Do not silently impute — a missing observation (unavailable data) is not the same as
    # confirmed zero spend, and treating them the same can materially bias the attribution.
    if marketing_data[features].isna().any().any():
        raise ValueError(
            "Missing spend observations detected. Confirm with the data source whether "
            "each gap is genuinely zero spend or unavailable data, then either fill "
            "confirmed-zero periods explicitly (fillna(0)) or exclude/impute unavailable "
            "periods using a documented policy before running this model."
        )

    # Add adstock/carryover effects
    for feature in features:
        marketing_data[f'{feature}_adstock'] = calculate_adstock(
            marketing_data[feature], decay_rate=0.7
        )
    
    # Add saturation curves
    for feature in features:
        marketing_data[f'{feature}_saturated'] = apply_saturation(
            marketing_data[f'{feature}_adstock'], saturation_point=0.8
        )
    
    # Model training
    saturated_features = [f'{f}_saturated' for f in features]
    X = marketing_data[saturated_features]
    y = marketing_data['conversions']
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Calculate feature importance (incremental impact)
    feature_importance = dict(zip(features, model.feature_importances_))
    
    return model, feature_importance

def calculate_adstock(spend_series, decay_rate):
    """Apply adstock transformation for carryover effects"""
    adstocked = np.zeros_like(spend_series)
    adstocked[0] = spend_series.iloc[0]
    
    for i in range(1, len(spend_series)):
        adstocked[i] = spend_series.iloc[i] + decay_rate * adstocked[i-1]
    
    return adstocked

def apply_saturation(adstocked_series, saturation_point):
    """Apply diminishing-returns (Hill-style) saturation transform"""
    max_adstock = adstocked_series.max()
    if max_adstock == 0:
        return np.zeros_like(adstocked_series, dtype=float)
    return 1 - np.exp(-saturation_point * adstocked_series / max_adstock)
```

## Marketing Psychology & Mental Models

<!-- source: davila7/claude-code-templates cli-tool/components/skills/business-marketing/marketing-psychology/SKILL.md#understanding-buyers-human-psychology -->

### Understanding Buyers & Human Psychology

These models explain how customers think, decide, and behave.

#### Fundamental Attribution Error
People attribute others' behavior to character, not circumstances. "They didn't buy because they're not serious" vs. "The checkout was confusing."

**Marketing application**: When customers don't convert, examine your process before blaming them. The problem is usually situational, not personal.

#### Mere Exposure Effect
People prefer things they've seen before. Familiarity breeds liking.

**Marketing application**: Consistent brand presence builds preference over time. Repetition across channels creates comfort and trust.

#### Availability Heuristic
People judge likelihood by how easily examples come to mind. Recent or vivid events seem more common.

**Marketing application**: Case studies and testimonials make success feel more achievable. Make positive outcomes easy to imagine.

#### Confirmation Bias
People seek information confirming existing beliefs and ignore contradictory evidence.

**Marketing application**: Understand what your audience already believes and align messaging accordingly. Fighting beliefs head-on rarely works.

#### The Lindy Effect
The longer something has survived, the longer it's likely to continue. Old ideas often outlast new ones.

**Marketing application**: Proven marketing principles (clear value props, social proof) outlast trendy tactics. Don't abandon fundamentals for fads.

#### Mimetic Desire
People want things because others want them. Desire is socially contagious.

**Marketing application**: Show that desirable people want your product. Waitlists, exclusivity, and social proof trigger mimetic desire.

#### Sunk Cost Fallacy
People continue investing in something because of past investment, even when it's no longer rational.

**Marketing application**: Know when to kill underperforming campaigns. Past spend shouldn't justify future spend if results aren't there.

#### Endowment Effect
People value things more once they own them.

**Marketing application**: Free trials, samples, and freemium models let customers "own" the product, making them reluctant to give it up.

#### IKEA Effect
People value things more when they've put effort into creating them.

**Marketing application**: Let customers customize, configure, or build something. Their investment increases perceived value and commitment.

#### Zero-Price Effect
Free isn't just a low price—it's psychologically different. "Free" triggers irrational preference.

**Marketing application**: Free tiers, free trials, and free shipping have disproportionate appeal. The jump from $1 to $0 is bigger than $2 to $1.

#### Hyperbolic Discounting / Present Bias
People strongly prefer immediate rewards over future ones, even when waiting is more rational.

**Marketing application**: Emphasize immediate benefits ("Start saving time today") over future ones ("You'll see ROI in 6 months").

#### Status-Quo Bias
People prefer the current state of affairs. Change requires effort and feels risky.

**Marketing application**: Reduce friction to switch. Make the transition feel safe and easy. "Import your data in one click."

#### Default Effect
People tend to accept pre-selected options. Defaults are powerful.

**Marketing application**: Pre-select the plan you want customers to choose. Opt-out beats opt-in for subscriptions (ethically applied).

#### Paradox of Choice
Too many options overwhelm and paralyze. Fewer choices often lead to more decisions.

**Marketing application**: Limit options. Three pricing tiers beat seven. Recommend a single "best for most" option.

#### Goal-Gradient Effect
People accelerate effort as they approach a goal. Progress visualization motivates action.

**Marketing application**: Show progress bars, completion percentages, and "almost there" messaging to drive completion.

#### Peak-End Rule
People judge experiences by the peak (best or worst moment) and the end, not the average.

**Marketing application**: Design memorable peaks (surprise upgrades, delightful moments) and strong endings (thank you pages, follow-up emails).

#### Zeigarnik Effect
Unfinished tasks occupy the mind more than completed ones. Open loops create tension.

**Marketing application**: "You're 80% done" creates pull to finish. Incomplete profiles, abandoned carts, and cliffhangers leverage this.

#### Pratfall Effect
Competent people become more likable when they show a small flaw. Perfection is less relatable.

**Marketing application**: Admitting a weakness ("We're not the cheapest, but...") can increase trust and differentiation.

#### Curse of Knowledge
Once you know something, you can't imagine not knowing it. Experts struggle to explain simply.

**Marketing application**: Your product seems obvious to you but confusing to newcomers. Test copy with people unfamiliar with your space.

#### Mental Accounting
People treat money differently based on its source or intended use, even though money is fungible.

**Marketing application**: Frame costs in favorable mental accounts. "$3/day" feels different than "$90/month" even though it's the same.

#### Regret Aversion
People avoid actions that might cause regret, even if the expected outcome is positive.

**Marketing application**: Address regret directly. Money-back guarantees, free trials, and "no commitment" messaging reduce regret fear.

#### Bandwagon Effect / Social Proof
People follow what others are doing. Popularity signals quality and safety.

**Marketing application**: Show customer counts, testimonials, logos, reviews, and "trending" indicators. Numbers create confidence.

---
