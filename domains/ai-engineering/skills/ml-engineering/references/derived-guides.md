# ML engineering — derived guides

Part of `ai-engineering:ml-engineering`.

## ai-ethics-advisor

<!-- source: davila7/claude-code-templates cli-tool/components/agents/ai-specialists/ai-ethics-advisor.md#regulatory-compliance-framework,agentic-ai-ethics -->

### Regulatory Compliance Framework

#### EU AI Act Compliance
- **Risk Classification**: Minimal, limited, high, unacceptable
- **Conformity Assessment**: Required documentation and testing
- **Transparency Obligations**: User notification requirements
- **Human Oversight**: Meaningful human control mandates
- **Compliance timeline note**: The Digital Omnibus on AI (Regulation (EU) 2026/1744) was adopted on 8 July 2026, published in the Official Journal on 24 July 2026, and entered into force 27 July 2026, formally deferring standalone high-risk (Annex III) provider/deployer obligations to 2 December 2027 and embedded-product (Annex I) obligations to 2 August 2028. This deferral is enacted law, not a pending proposal — do not describe it as pending. Obligations that stayed on the original 2 August 2026 schedule and are already binding: Article 50 transparency/AI-content-labeling duties, GPAI provider obligations (binding since Aug 2025), and the Article 5 prohibited-practices regime (binding since Feb 2025, expanded by the Omnibus to add a new prohibition on AI-generated non-consensual intimate imagery and CSAM). Always re-verify against the official EU AI Act implementation timeline before citing dates in a compliance report, since this area continues to move quickly.

#### US AI Standards (NIST AI RMF)
- **Govern**: Organizational AI governance structures
- **Map**: AI system and context understanding
- **Measure**: Risk and impact quantification  
- **Manage**: Risk response and monitoring
- **Naming note**: NIST's AI Safety Institute was renamed the Center for AI Standards and Innovation (CAISI) in June 2025, alongside a mandate shift away from broad "safety" framing toward security- and innovation-focused testing. The Govern/Map/Measure/Manage structure above is unchanged, but cite "CAISI," not "AI Safety Institute," going forward.

#### NIST AI 600-1 — Generative AI Profile
Published July 2024 as a companion to the core AI RMF, this profile identifies risks specific to generative AI and dual-use foundation models. Apply it whenever the system under review is LLM- or agent-based rather than classical ML. The 12 GenAI-specific risk categories are:
- **CBRN Information or Capabilities Uplift** — lowering barriers to chemical, biological, radiological, or nuclear harm
- **Confabulation** — plausible but false or ungrounded output (a.k.a. hallucination)
- **Dangerous, Violent, or Hateful Content**
- **Data Privacy** — leakage of training data or user inputs, re-identification risk
- **Environmental Impact** — compute and energy footprint of training/inference
- **Harmful Bias and Homogenization** — amplification of bias or reduction of output diversity
- **Human-AI Configuration** — risks from how humans interact with and rely on the system
- **Information Integrity** — generation of mis/disinformation at scale
- **Information Security** — novel attack surfaces (prompt injection, data poisoning, model extraction)
- **Intellectual Property** — infringing or unattributed generated content
- **Obscene, Degrading, or Abusive Content**
- **Value Chain and Component Integration** — risks inherited from third-party models, datasets, plugins, or fine-tunes

#### ISO/IEC 42001 — AI Management System
The world's first certifiable AI management system standard (published 2023). Provides 38 controls across 9 objectives covering:
- AI policy and governance leadership commitment
- Risk-based approach to AI system planning
- Operational controls for AI lifecycle stages
- Performance evaluation and continual improvement
- Supplier and third-party AI system obligations

Use this standard when a client needs a certifiable framework or is entering regulated markets that require demonstrated AI governance maturity.

#### ISO/IEC 42005 — AI System Impact Assessment
Published 2025, this standard defines a structured methodology for conducting impact assessments across the full AI lifecycle:
- Scoping and context establishment
- Stakeholder identification and impact categories
- Assessment of social, economic, and rights impacts
- Documentation and disclosure requirements
- Reassessment triggers (significant system changes, new deployment contexts)

Reference this standard when producing Algorithmic Impact Assessments or when clients need lifecycle-spanning governance documentation.

#### UNESCO Recommendation on the Ethics of AI
Adopted in 2021 by all 193 UNESCO member states, this is the first global normative framework for AI ethics. It defines 10 core principles:

1. **Proportionality and Do No Harm** — AI capabilities must be proportionate to their stated purpose
2. **Safety and Security** — Unwanted harms and security risks must be assessed throughout the lifecycle
3. **Fairness and Non-Discrimination** — AI must not perpetuate or amplify discrimination
4. **Sustainability** — AI development must consider environmental impact
5. **Privacy and Data Protection** — Right to privacy must be protected by design
6. **Human Oversight and Determination** — Humans must retain meaningful agency over AI decisions
7. **Transparency and Explainability** — AI processes must be interpretable by relevant stakeholders
8. **Responsibility and Accountability** — Clear lines of responsibility for AI outcomes
9. **Awareness and Literacy** — Public and developer education on AI capabilities and limits
10. **Multi-Stakeholder and Adaptive Governance** — Inclusive governance with continuous adaptation

Reference this framework when working with public-sector clients or multinational deployments where a universally recognized ethical baseline is required.

#### Industry-Specific Requirements
- **Healthcare**: HIPAA, FDA AI/ML guidance
- **Finance**: Fair Credit Reporting Act, Equal Credit Opportunity Act, GDPR
- **Employment**: Equal Employment Opportunity laws
- **Education**: FERPA, algorithmic accountability

**US State AI Laws:** State-level AI regulation now directly bears on this agent's own example domains (hiring, healthcare, credit) and should be checked whenever the "jurisdiction" from the initial requirements gathering includes the US:
- **Colorado**: The original Colorado AI Act (SB 24-205) was repealed and replaced by SB 26-189 (signed 14 May 2026); the new framework takes effect 1 January 2027.
- **Texas**: The Texas Responsible AI Governance Act (TRAIGA) has been enforced since January 2026.
- **California**: The California AI Transparency Act and the Generative AI Training Data Transparency Act both took effect 1 January 2026.

Verify current requirements for the specific state(s) in scope before citing them in a compliance report — state AI legislation is moving quickly and this list is not exhaustive.

### Agentic AI Ethics

Classical ML bias frameworks were designed for batch-inference models. AI agents introduce a distinct set of ethical risks that require dedicated analysis. In addition to the OWASP Top 10 for LLM Applications, OWASP also publishes a dedicated **Top 10 for Agentic Applications** (ASI01–ASI10, published 9 December 2025, updated to v2.01 on 1 June 2026) covering risks specific to autonomous agents — planning, tool use, memory, identity, and multi-agent coordination — that the LLM-focused list does not capture. The subsections below map to both frameworks where relevant.

#### Goal Manipulation Resistance
- **Prompt injection**: Can the agent's objective be hijacked via crafted tool outputs or user messages? Maps to **OWASP LLM01:2026 Prompt Injection** in the OWASP Top 10 for LLM Applications, and also to **ASI01 Agent Goal Hijack** in the OWASP Top 10 for Agentic Applications when the goal itself, not just a single response, is redirected.
- **Objective drift**: Does extended multi-turn context shift the agent's effective goal?
- **Mitigation**: Treat all external content as untrusted input; apply input sanitization and output validation at tool boundaries.

#### Minimal Footprint
- The agent should request only the permissions necessary for the current task. Maps to **OWASP LLM03:2026 Excessive Agency** (moved from rank 6 in the 2025 edition to rank 3 in the 2026 edition) — excessive permissions, functionality, or autonomy granted to the agent — and to **ASI03 Identity & Privilege Abuse** in the OWASP Top 10 for Agentic Applications.
- Credentials, filesystem access, and network scope must be scoped to the minimum required
- Review permission requests against the principle of least privilege before deployment
- Bash access, when granted, should be scoped to running bias-detection and fairness libraries (e.g. `aif360`, `fairlearn`) rather than open-ended shell use — request only what the assessment task requires

#### Human Oversight Checkpoints
- Define explicit gates where a human must approve before irreversible actions (data deletion, financial transactions, external API calls with side effects)
- Checkpoints should be meaningful — provide enough context for a human to make an informed decision, not just a rubber-stamp confirmation
- Treat **ASI08 Cascading Failures** and **ASI10 Rogue Agents** (OWASP Top 10 for Agentic Applications) as escalation triggers: an agent whose behavior deviates from its authorized scope, or whose errors are propagating to other agents/systems, should hit a human checkpoint automatically rather than continue autonomously

#### Inter-Agent Trust Boundaries
- When one agent invokes another, verify the downstream agent's identity and authorization scope
- Outputs from subordinate agents should be treated with the same skepticism as external user input
- Document trust hierarchies explicitly in system design
- Maps to **ASI07 Insecure Inter-Agent Communication** and **ASI09 Human-Agent Trust Exploitation** in the OWASP Top 10 for Agentic Applications

**Memory and Context Integrity:**
- Persistent memory and RAG context can be shaped over time to bias future agent decisions — a distinct ethics risk from a single manipulated response, since it degrades behavior gradually and can be harder to detect in a point-in-time audit
- Maps to **ASI06 Memory & Context Poisoning** in the OWASP Top 10 for Agentic Applications
- Audit what gets written to long-term memory/vector stores, from what sources, and whether untrusted content (tool outputs, retrieved documents, other agents' outputs) can influence it without validation
- Cross-reference **ASI04 Agentic Supply Chain Vulnerabilities** with the NIST AI 600-1 "Value Chain and Component Integration" category above — both cover risk inherited from third-party models, plugins, or data sources feeding the agent

#### Tool Misuse Surface
- For each tool an agent can invoke, assess the harm potential if that tool is called with malicious or erroneous parameters
- Rank tools by blast radius and apply additional constraints to high-risk tools (confirmation prompts, rate limits, audit logging)
- Regularly audit the tool inventory — remove tools not required for the agent's stated purpose
- Maps to **ASI02 Tool Misuse** in the OWASP Top 10 for Agentic Applications, and to **ASI05 Unexpected Code Execution** where the tool surface includes sandboxing or code execution

## ML Paper Writing for Top AI Conferences

<!-- source: davila7/claude-code-templates cli-tool/components/skills/ai-research/ml-paper-writing/SKILL.md#writing-philosophy-for-top-ml-conferences -->

### Writing Philosophy for Top ML Conferences

**This section distills the most important writing principles from leading ML researchers.** These aren't optional style suggestions—they're what separates accepted papers from rejected ones.

> "A paper is a short, rigorous, evidence-based technical story with a takeaway readers care about." — Neel Nanda

#### The Sources Behind This Guidance

This skill synthesizes writing philosophy from researchers who have published extensively at top venues:

| Source | Key Contribution | Link |
|--------|-----------------|------|
| **Neel Nanda** (Google DeepMind) | The Narrative Principle, What/Why/So What framework | [How to Write ML Papers](https://www.alignmentforum.org/posts/eJGptPbbFPZGLpjsp/highly-opinionated-advice-on-how-to-write-ml-papers) |
| **Sebastian Farquhar** (DeepMind) | 5-sentence abstract formula | [How to Write ML Papers](https://sebastianfarquhar.com/on-research/2024/11/04/how_to_write_ml_papers/) |
| **Gopen & Swan** | 7 principles of reader expectations | [Science of Scientific Writing](https://cseweb.ucsd.edu/~swanson/papers/science-of-writing.pdf) |
| **Zachary Lipton** | Word choice, eliminating hedging | [Heuristics for Scientific Writing](https://www.approximatelycorrect.com/2018/01/29/heuristics-technical-scientific-writing-machine-learning-perspective/) |
| **Jacob Steinhardt** (UC Berkeley) | Precision, consistent terminology | [Writing Tips](https://bounded-regret.ghost.io/) |
| **Ethan Perez** (Anthropic) | Micro-level clarity tips | [Easy Paper Writing Tips](https://ethanperez.net/easy-paper-writing-tips/) |
| **Andrej Karpathy** | Single contribution focus | Various lectures |

**For deeper dives into any of these, see:**
- references/writing-guide.md - Full explanations with examples
- references/sources.md - Complete bibliography

#### Time Allocation (From Neel Nanda)

Spend approximately **equal time** on each of:
1. The abstract
2. The introduction
3. The figures
4. Everything else combined

**Why?** Most reviewers form judgments before reaching your methods. Readers encounter your paper as: **title → abstract → introduction → figures → maybe the rest.**

#### Writing Style Guidelines

##### Sentence-Level Clarity (Gopen & Swan's 7 Principles)

These principles are based on how readers actually process prose. Violating them forces readers to spend cognitive effort on structure rather than content.

| Principle | Rule | Example |
|-----------|------|---------|
| **Subject-verb proximity** | Keep subject and verb close | ❌ "The model, which was trained on..., achieves" → ✅ "The model achieves... after training on..." |
| **Stress position** | Place emphasis at sentence ends | ❌ "Accuracy improves by 15% when using attention" → ✅ "When using attention, accuracy improves by **15%**" |
| **Topic position** | Put context first, new info after | ✅ "Given these constraints, we propose..." |
| **Old before new** | Familiar info → unfamiliar info | Link backward, then introduce new |
| **One unit, one function** | Each paragraph makes one point | Split multi-point paragraphs |
| **Action in verb** | Use verbs, not nominalizations | ❌ "We performed an analysis" → ✅ "We analyzed" |
| **Context before new** | Set stage before presenting | Explain before showing equation |

**Full 7 principles with detailed examples:** See references/writing-guide.md

##### Micro-Level Tips (Ethan Perez)

These small changes accumulate into significantly clearer prose:

- **Minimize pronouns**: ❌ "This shows..." → ✅ "This result shows..."
- **Verbs early**: Position verbs near sentence start
- **Unfold apostrophes**: ❌ "X's Y" → ✅ "The Y of X" (when awkward)
- **Delete filler words**: "actually," "a bit," "very," "really," "basically," "quite," "essentially"

**Full micro-tips with examples:** See references/writing-guide.md

##### Word Choice (Zachary Lipton)

- **Be specific**: ❌ "performance" → ✅ "accuracy" or "latency" (say what you mean)
- **Eliminate hedging**: Drop "may" and "can" unless genuinely uncertain
- **Avoid incremental vocabulary**: ❌ "combine," "modify," "expand" → ✅ "develop," "propose," "introduce"
- **Delete intensifiers**: ❌ "provides *very* tight approximation" → ✅ "provides tight approximation"

##### Precision Over Brevity (Jacob Steinhardt)

- **Consistent terminology**: Different terms for same concept creates confusion. Pick one and stick with it.
- **State assumptions formally**: Before theorems, list all assumptions explicitly
- **Intuition + rigor**: Provide intuitive explanations alongside formal proofs

#### What Reviewers Actually Read

Understanding reviewer behavior helps prioritize your effort:

| Paper Section | % Reviewers Who Read | Implication |
|---------------|---------------------|-------------|
| Abstract | 100% | Must be perfect |
| Introduction | 90%+ (skimmed) | Front-load contribution |
| Figures | Examined before methods | Figure 1 is critical |
| Methods | Only if interested | Don't bury the lede |
| Appendix | Rarely | Put only supplementary details |

**Bottom line**: If your abstract and intro don't hook reviewers, they may never read your brilliant methods section.

---
