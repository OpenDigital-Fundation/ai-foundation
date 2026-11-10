# Source research — derived guides

Part of `research:source-research`.

## competitive-intelligence-analyst

<!-- source: davila7/claude-code-templates cli-tool/components/agents/deep-research-team/competitive-intelligence-analyst.md#specialized-analysis-techniques,core-intelligence-framework -->

### Core Intelligence Framework

#### Market Research Methodology
- **Competitive Landscape Mapping**: Industry player identification, market share analysis, positioning strategies
- **SWOT Analysis**: Strengths, weaknesses, opportunities, threats assessment for target entities
- **Porter's Five Forces**: Competitive dynamics, supplier power, buyer power, threat analysis
- **Market Segmentation**: Customer demographics, psychographics, behavioral patterns
- **Trend Analysis**: Industry evolution, emerging technologies, regulatory changes

#### Intelligence Gathering Sources
- **Public Company Data**: Annual reports (10-K, 10-Q), SEC filings, investor presentations
- **News and Media**: Press releases, industry publications, trade journals, news articles
- **Social Intelligence**: Social media monitoring, executive communications, brand sentiment
- **Patent Analysis**: Innovation tracking, R&D direction, competitive moats
- **Job Postings**: Hiring patterns, skill requirements, strategic direction indicators
- **Web Intelligence**: Website analysis, SEO strategies, digital marketing approaches

### Specialized Analysis Techniques

#### Patent Intelligence Analysis
```python
def analyze_patent_landscape(self, technology_domain, competitor_list):
    """
    Patent analysis for competitive intelligence
    """
    patent_intelligence = {
        'innovation_trends': {
            'filing_patterns': [],
            'technology_focus_areas': [],
            'invention_velocity': [],
            'collaboration_networks': []
        },
        'competitive_moats': {
            'strong_patent_portfolios': [],
            'patent_gaps': [],
            'freedom_to_operate': [],
            'licensing_opportunities': []
        },
        'future_direction_signals': {
            'emerging_technologies': [],
            'r_and_d_investments': [],
            'strategic_partnerships': [],
            'acquisition_targets': []
        }
    }
    
    return patent_intelligence
```

#### Social Media Intelligence
```python
def monitor_social_sentiment(self, brand_list, monitoring_keywords):
    """
    Social media sentiment and brand perception analysis
    """
    social_intelligence = {
        'brand_sentiment': {
            'overall_sentiment_score': {},
            'sentiment_trends': {},
            'key_conversation_topics': [],
            'influencer_opinions': []
        },
        'competitive_comparison': {
            'mention_volume': {},
            'engagement_rates': {},
            'share_of_voice': {},
            'sentiment_comparison': {}
        },
        'crisis_monitoring': {
            'negative_sentiment_spikes': [],
            'controversy_detection': [],
            'reputation_risks': [],
            'response_strategies': []
        }
    }
    
    return social_intelligence
```

## first-principles-thinking

<!-- source: VoltAgent/awesome-claude-code-subagents categories/10-research-analysis/first-principles-thinking.md#the-5-step-first-principles-method -->

### The 5-Step First Principles Method

#### Step 1: Define the Problem Precisely
Strip out solution framing and get to the real problem.
- Weak: "We need a better onboarding flow"
- Strong: "New users fail to reach their first value moment within 7 days"

#### Step 2: Identify All Current Assumptions
List every assumption baked into the current approach:
- Technology assumptions ("it requires a form")
- Process assumptions ("users need to sign up first")
- Business assumptions ("we charge per seat")
- User assumptions ("users know what they want")

#### Step 3: Challenge Each Assumption
For each assumption, ask:
- Is this actually true?
- What evidence supports it?
- What would happen if we reversed it?
- Who proved this was necessary?

#### Step 4: Identify the Fundamental Truths
What facts remain after stripping all assumptions?
- Physics or technical constraints
- True user needs (not stated preferences)
- Economic realities
- Irreducible facts about the domain

#### Step 5: Rebuild from Scratch
Starting only from fundamental truths:
- What's the simplest possible solution?
- What becomes possible when assumptions are removed?
- What would a new entrant with no legacy do?

**Classic example**: Elon Musk on battery costs — instead of accepting "batteries are expensive because they always have been," break the battery into raw materials, price each on commodity markets, and build up from there. The assumption was the cost, not the physics.

## research-synthesizer

<!-- source: davila7/claude-code-templates cli-tool/components/agents/deep-research-team/research-synthesizer.md#phased-execution-workflow -->

### Phased Execution Workflow

#### Phase 1 — Input Discovery
Identify all available researcher output files, list them, and note which researchers are present and which are missing.

#### Phase 2 — Parallel Extraction
For each researcher output, extract:
- Major claims and conclusions
- Evidence items and supporting data
- All citations (format as given by the researcher)
- Confidence signals (explicit ratings or hedging language)

Flag any items where the researcher's confidence appears low or where evidence is sparse.

#### Phase 3 — Cross-Source Integration
- Group findings by theme across all sources
- Detect overlaps and near-duplicate claims; merge them while preserving the originating sources
- Surface direct contradictions between sources
- Assess relative evidence quality: peer-reviewed > technical documentation > web sources > unverified claims

#### Phase 4 — Output and Self-Review
1. Write the `synthesis_summary` field content as a standalone markdown file first (`synthesis-summary.md`), then produce the full JSON written to `synthesis.json`.
2. Run the Quality Verification Checklist (see below) before finalizing.
