# Verification before completion — doublecheck

Part of `testing:verification-before-completion`. Adapted reference material; the owner procedure, project conventions, scope and authorization rules take precedence. Examples are not automatically executed.

## Doublecheck

<!-- source: github/awesome-copilot skills/doublecheck/SKILL.md#layer-3-adversarial-review,layer-1-self-audit,layer-2-source-verification,domain-specific-guidance -->

### Layer 1: Self-Audit

Re-read the target text with a critical lens. Your job in this layer is extraction and internal analysis -- no web searches yet.

#### Step 1: Extract Claims

Go through the target text sentence by sentence and pull out every statement that asserts something verifiable. Categorize each claim:

| Category | What to look for | Examples |
|----------|-----------------|---------|
| **Factual** | Assertions about how things are or were | "Python was created in 1991", "The GPL requires derivative works to be open-sourced" |
| **Statistical** | Numbers, percentages, quantities | "95% of enterprises use cloud services", "The contract has a 30-day termination clause" |
| **Citation** | References to specific documents, cases, laws, papers, or standards | "Under Section 230 of the CDA...", "In *Mayo v. Prometheus* (2012)..." |
| **Entity** | Claims about specific people, organizations, products, or places | "OpenAI was founded by Sam Altman and Elon Musk", "GDPR applies to EU residents" |
| **Causal** | Claims that X caused Y or X leads to Y | "This vulnerability allows remote code execution", "The regulation was passed in response to the 2008 financial crisis" |
| **Temporal** | Dates, timelines, sequences of events | "The deadline is March 15", "Version 2.0 was released before the security patch" |

Assign each claim a temporary ID (C1, C2, C3...) for tracking through subsequent layers.

#### Step 2: Check Internal Consistency

Review the extracted claims against each other:
- Does the text contradict itself anywhere? (e.g., states two different dates for the same event)
- Are there claims that are logically incompatible?
- Does the text make assumptions in one section that it contradicts in another?

Flag any internal contradictions immediately -- these don't need external verification to identify as problems.

#### Step 3: Initial Confidence Assessment

For each claim, make an initial assessment based only on your own knowledge:
- Do you recall this being accurate?
- Is this the kind of claim where models frequently hallucinate? (Specific citations, precise statistics, and exact dates are high-risk categories.)
- Is the claim specific enough to verify, or is it vague enough to be unfalsifiable?

Record your initial confidence but do NOT report it as a finding yet. This is input for Layer 2, not output.

---

### Layer 2: Source Verification

For each extracted claim, search for external evidence. The purpose of this layer is to find URLs the user can visit to verify claims independently.

#### Search Strategy

For each claim:

1. **Formulate a search query** that would surface the primary source. For citations, search for the exact title or case name. For statistics, search for the specific number and topic. For factual claims, search for the key entities and relationships.

2. **Run the search** using `web_search`. If the first search doesn't return relevant results, reformulate and try once more with different terms.

3. **Evaluate what you find:**
   - Did you find a primary or authoritative source that directly addresses the claim?
   - Did you find contradicting information from a credible source?
   - Did you find nothing relevant? (This is itself a signal -- real things usually have a web footprint.)

4. **Record the result** with the source URL. Always provide the URL even if you also summarize what the source says.

#### What Counts as a Source

Prefer primary and authoritative sources:
- Official documentation, specifications, and standards
- Court records, legislative texts, regulatory filings
- Peer-reviewed publications
- Official organizational websites and press releases
- Established reference works (encyclopedias, legal databases)

Note when a source is secondary (news article, blog post, wiki page) vs. primary. The user can weigh accordingly.

#### Handling Citations Specifically

Citations are the highest-risk category for hallucinations. For any claim that cites a specific case, statute, paper, standard, or document:

1. Search for the exact citation (case name, title, section number).
2. If you find it, confirm the cited content actually says what the target text claims it says.
3. If you cannot find it at all, flag it as FABRICATION RISK. Models frequently generate plausible-sounding citations for things that don't exist.

---

### Layer 3: Adversarial Review

Switch your posture entirely. In Layers 1 and 2, you were trying to understand and verify the output. In this layer, **assume the output contains errors** and actively try to find them.

#### Hallucination Pattern Checklist

Check for these common patterns:

1. **Fabricated citations** -- The text cites a specific case, paper, or statute that you could not find in Layer 2. This is the most dangerous hallucination pattern because it looks authoritative.

2. **Precise numbers without sources** -- The text states a specific statistic (e.g., "78% of companies...") without indicating where the number comes from. Models often generate plausible-sounding statistics that are entirely made up.

3. **Confident specificity on uncertain topics** -- The text states something very specific about a topic where specifics are genuinely unknown or disputed. Watch for exact dates, precise dollar amounts, and definitive attributions in areas where experts disagree.

4. **Plausible-but-wrong associations** -- The text associates a concept, ruling, or event with the wrong entity. For example, attributing a ruling to the wrong court, assigning a quote to the wrong person, or describing a law's provision incorrectly while getting the law's name right.

5. **Temporal confusion** -- The text describes something as current that may be outdated, or describes a sequence of events in the wrong order.

6. **Overgeneralization** -- The text states something as universally true when it applies only in specific jurisdictions, contexts, or time periods. Common in legal and regulatory content.

7. **Missing qualifiers** -- The text presents a nuanced topic as settled or straightforward when significant exceptions, limitations, or counterarguments exist.

#### Adversarial Questions

For each major claim that passed Layers 1 and 2, ask:
- What would make this claim wrong?
- Is there a common misconception in this area that the model might have picked up?
- If I were a subject matter expert, would I object to how this is stated?
- Is this claim from before or after my training data cutoff, and might it be outdated?

#### Red Flags to Escalate

If you find any of these, flag them prominently in the report:
- A specific citation that cannot be found anywhere
- A statistic with no identifiable source
- A legal or regulatory claim that contradicts what authoritative sources say
- A claim that has been stated with high confidence but is actually disputed or uncertain

---

### Domain-Specific Guidance

#### Legal Content

Legal content carries elevated hallucination risk because:
- Case names, citations, and holdings are frequently fabricated by models
- Jurisdictional nuances are often flattened or omitted
- Statutory language may be paraphrased in ways that change the legal meaning
- "Majority rule" and "minority rule" distinctions are often lost

For legal content, give extra scrutiny to: case citations, statutory references, regulatory interpretations, and jurisdictional claims. Search legal databases when possible.

#### Medical and Scientific Content

- Check that cited studies actually exist and that the results are accurately described
- Watch for outdated guidelines being presented as current
- Flag dosages, treatment protocols, or diagnostic criteria -- these change and errors can be dangerous

#### Financial and Regulatory Content

- Verify specific dollar amounts, dates, and thresholds
- Check that regulatory requirements are attributed to the correct jurisdiction and are current
- Watch for tax law claims that may be outdated after recent legislative changes

#### Technical and Security Content

- Verify CVE numbers, vulnerability descriptions, and affected versions
- Check that API specifications and configuration instructions match current documentation
- Watch for version-specific information that may be outdated
