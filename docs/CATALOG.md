# Catálogo de artefatos

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

116 artefatos em 25 domínios. Tipos: 1 agent, 3 knowledge, 111 skill, 1 workflow.

[Início](../README.md) · [Buscar por faceta](FACETS.md) · [Como manter](architecture/repository-layout.md)

## Domínios

- [accessibility](#accessibility) — 4 artefatos
- [agent-engineering](#agent-engineering) — 11 artefatos
- [ai-engineering](#ai-engineering) — 5 artefatos
- [architecture](#architecture) — 7 artefatos
- [brand](#brand) — 2 artefatos
- [code-quality](#code-quality) — 6 artefatos
- [creative-media](#creative-media) — 6 artefatos
- [data](#data) — 3 artefatos
- [debugging](#debugging) — 2 artefatos
- [documents](#documents) — 4 artefatos
- [finance](#finance) — 3 artefatos
- [languages](#languages) — 13 artefatos
- [legal-compliance](#legal-compliance) — 2 artefatos
- [marketing](#marketing) — 5 artefatos
- [operations](#operations) — 3 artefatos
- [platform](#platform) — 5 artefatos
- [principles](#principles) — 1 artefatos
- [product](#product) — 1 artefatos
- [research](#research) — 3 artefatos
- [sales](#sales) — 3 artefatos
- [security](#security) — 5 artefatos
- [testing](#testing) — 4 artefatos
- [ui](#ui) — 4 artefatos
- [ux](#ux) — 2 artefatos
- [workflow](#workflow) — 12 artefatos

## accessibility

[Plugin e instalação](../domains/accessibility/README.md) · [Manifesto editorial](../catalog/curation/domains/accessibility.yaml)

Accessibility conformance and audits - WCAG, ARIA, assistive technology.

| Artefato | Tipo | Capacidade |
|---|---|---|
| [`accessibility:accessibility-audit`](../domains/accessibility/skills/accessibility-audit/SKILL.md) | skill | Use when the user asks for an accessibility audit of a website or web app, a conformance or compliance report (Section 508, EN 301 549, EAA, ADA, AODA, VPAT), an accessibility statement, acc |
| [`accessibility:assistive-technology-testing`](../domains/accessibility/skills/assistive-technology-testing/SKILL.md) | skill | Use when deciding how to test accessibility or running the tests: screen readers (NVDA, JAWS, VoiceOver, Narrator, TalkBack), keyboard-only passes, simulated narration of HTML or JSX, deskto |
| [`accessibility:document-accessibility`](../domains/accessibility/skills/document-accessibility/SKILL.md) | skill | Use when Word, Excel, PowerPoint, PDF, ePub or Markdown files must be accessible: auditing them one by one or as a folder inventory, fixing titles, headings, reading order, tags, alt text an |
| [`accessibility:wcag-accessibility`](../domains/accessibility/skills/wcag-accessibility/SKILL.md) | skill | Use when designing, building or reviewing interfaces for accessibility on web, mobile or desktop: WCAG 2.2 AA (and AAA or WCAG 3 when asked), semantic roles and ARIA, keyboard and focus, for |

## agent-engineering

[Plugin e instalação](../domains/agent-engineering/README.md) · [Manifesto editorial](../catalog/curation/domains/agent-engineering.yaml)

Configuring and operating coding agents - skill authoring, harnesses, orchestration, subagents, loops, memory, context.

| Artefato | Tipo | Capacidade |
|---|---|---|
| [`agent-engineering:agent-debugging`](../domains/agent-engineering/skills/agent-debugging/SKILL.md) | skill | Use when an agent run failed, looped, ignored instructions or produced a bad result and you need to know why: capture the transcript, diagnose the failure, contain and recover, and write an |
| [`agent-engineering:agent-evaluation`](../domains/agent-engineering/skills/agent-evaluation/SKILL.md) | skill | Use when measuring agents rather than a single skill: comparing coding agents or configurations head to head on custom tasks, building an eval harness with pass rate, cost and time, self-eva |
| [`agent-engineering:agent-guardrails`](../domains/agent-engineering/skills/agent-guardrails/SKILL.md) | skill | Use when an agent should be prevented from destructive or risky actions: blocking dangerous git and shell commands (push, reset --hard, clean, rm -rf, --no-verify) with harness hooks, carefu |
| [`agent-engineering:agent-loops`](../domains/agent-engineering/skills/agent-loops/SKILL.md) | skill | Use when designing, running or reviewing an autonomous or long-running agent loop: machine-checkable goals and stop conditions, quality gates and evals inside the loop, operator approval poi |
| [`agent-engineering:agent-memory`](../domains/agent-engineering/skills/agent-memory/SKILL.md) | skill | Use when an agent should learn across sessions: capturing durable lessons and decisions, promoting observations into rules or skills, pruning stale memory, keeping a scoped context file, and |
| [`agent-engineering:agent-teams`](../domains/agent-engineering/skills/agent-teams/SKILL.md) | skill | Use when coordinating several agents as a team on one effort: assigning owners and scope to work items, isolating each agent in its own branch or worktree, tracking state on a board, merge g |
| [`agent-engineering:context-management`](../domains/agent-engineering/skills/context-management/SKILL.md) | skill | Use when an agent session is long, expensive or near its context limit: budgeting tokens, deciding when and how to compact, what to keep in context versus files, and estimating the token cos |
| [`agent-engineering:harness-design`](../domains/agent-engineering/skills/harness-design/SKILL.md) | skill | Use when designing or auditing an AI agent or agentic product: its tools and action space, observation formatting, permissions, identity and trust, multi-agent topology, and the twelve-layer |
| [`agent-engineering:parallel-agents`](../domains/agent-engineering/skills/parallel-agents/SKILL.md) | skill | Dispatch one focused subagent per independent task and integrate their verified results. |
| [`agent-engineering:session-retrospective`](../domains/agent-engineering/skills/session-retrospective/SKILL.md) | skill | Review a coding-agent session and propose ranked improvements to the agent's environment. |
| [`agent-engineering:skill-authoring`](../domains/agent-engineering/skills/skill-authoring/SKILL.md) | skill | Create, test, benchmark and tune skills, with eval loops, pressure tests and catalog placement rules. |

## ai-engineering

[Plugin e instalação](../domains/ai-engineering/README.md) · [Manifesto editorial](../catalog/curation/domains/ai-engineering.yaml)

Building products with LLMs - model APIs, MCP servers, RAG, prompts, product evals, cost.

| Artefato | Tipo | Capacidade |
|---|---|---|
| [`ai-engineering:claude-api`](../domains/ai-engineering/skills/claude-api/SKILL.md) | skill | Use when building with the Claude API or Anthropic SDKs: choosing a model, messages and streaming, tool use, MCP, agents, prompt caching, batch, token counting, error handling, or migrating |
| [`ai-engineering:mcp-server-development`](../domains/ai-engineering/skills/mcp-server-development/SKILL.md) | skill | Use when designing, building, testing or evaluating a Model Context Protocol server: choosing tools, resources and prompts, writing tool schemas and descriptions, transports, auth, error han |
| [`ai-engineering:ml-engineering`](../domains/ai-engineering/skills/ml-engineering/SKILL.md) | skill | Use when adding or operating machine learning in a product: data contracts, features, reproducible training, evaluation and model QA, serving, monitoring and drift, recommendation and rankin |
| [`ai-engineering:prompt-engineering`](../domains/ai-engineering/skills/prompt-engineering/SKILL.md) | skill | Use when writing, testing or optimising prompts for an LLM feature: system prompts, few-shot examples, structured output, prompt evaluation sets, prompt caching for cost and latency, and dec |
| [`ai-engineering:rag-pipelines`](../domains/ai-engineering/skills/rag-pipelines/SKILL.md) | skill | Use when building, debugging or reviewing retrieval-augmented generation or search: chunking, embeddings, hybrid and lexical search, reranking, query rewriting, iterative retrieval for agent |

## architecture

[Plugin e instalação](../domains/architecture/README.md) · [Manifesto editorial](../catalog/curation/domains/architecture.yaml)

System and code design - modules, domain models, ADRs, APIs, boundaries.

| Artefato | Tipo | Capacidade |
|---|---|---|
| [`architecture:api-design`](../domains/architecture/skills/api-design/SKILL.md) | skill | Design or review HTTP APIs: resources, status codes, errors, pagination, auth, rate limits, versioning. |
| [`architecture:architecture-review`](../domains/architecture/skills/architecture-review/SKILL.md) | skill | Scan an existing codebase for deepening opportunities and walk the chosen one with the user. |
| [`architecture:codebase-design`](../domains/architecture/skills/codebase-design/SKILL.md) | skill | Design deep modules at clean seams, including ports and adapters, with a shared vocabulary. |
| [`architecture:codebase-onboarding`](../domains/architecture/skills/codebase-onboarding/SKILL.md) | skill | Use when someone (or an agent) needs to understand an unfamiliar codebase fast: map its structure and entry points, trace a feature end to end, write a guided code tour, recover the intent b |
| [`architecture:decision-records`](../domains/architecture/skills/decision-records/SKILL.md) | skill | Record, supersede, index and read architecture decision records, one decision per file. |
| [`architecture:domain-modeling`](../domains/architecture/skills/domain-modeling/SKILL.md) | skill | Sharpen the domain language with scenarios, keep GLOSSARY.md current, and flag decisions worth an ADR. |
| [`architecture:system-design`](../domains/architecture/skills/system-design/SKILL.md) | skill | Use when designing a service, system or major feature end to end: components and boundaries, data flow, APIs and contracts, consistency and failure handling, scalability and latency budgets, |

## brand

[Plugin e instalação](../domains/brand/README.md) · [Manifesto editorial](../catalog/curation/domains/brand.yaml)

Brand identity, voice and style guides.

| Artefato | Tipo | Capacidade |
|---|---|---|
| [`brand:brand-identity`](../domains/brand/skills/brand-identity/SKILL.md) | skill | Use when defining or applying a brand: discovery interviews, positioning, visual identity (logo direction, colour, typography), messaging framework, brand guidelines, asset management and ch |
| [`brand:brand-voice`](../domains/brand/skills/brand-voice/SKILL.md) | skill | Use when writing should sound like a specific person or company: build a style profile from their real posts, essays, launch notes or docs, then write or edit drafts in that voice and flag l |

## code-quality

[Plugin e instalação](../domains/code-quality/README.md) · [Manifesto editorial](../catalog/curation/domains/code-quality.yaml)

Evaluating and improving existing code - giving and receiving review, simplification, refactoring, debt, repository audits.

| Artefato | Tipo | Capacidade |
|---|---|---|
| [`code-quality:code-review`](../domains/code-quality/skills/code-review/SKILL.md) | skill | Pin a change, gather spec and standards, dispatch a fresh reviewer and act on numbered findings. |
| [`code-quality:code-reviewer`](../domains/code-quality/agents/code-reviewer.md) | agent | Read-only, fresh-context reviewer that reports evidence-backed findings by severity with a verdict. |
| [`code-quality:codebase-audit`](../domains/code-quality/skills/codebase-audit/SKILL.md) | skill | Multi-specialist audit of a repository, diff or folder with a sceptical verifier and a graded, prioritised report. |
| [`code-quality:debt-ledger`](../domains/code-quality/skills/debt-ledger/SKILL.md) | skill | Collect every recorded shortcut comment into one ranked technical-debt ledger. |
| [`code-quality:receiving-code-review`](../domains/code-quality/skills/receiving-code-review/SKILL.md) | skill | Verify review findings before acting, push back with evidence, and fix in severity order. |
| [`code-quality:simplification`](../domains/code-quality/skills/simplification/SKILL.md) | skill | Use when existing code should get simpler without changing behaviour: removing dead code and unused exports, collapsing needless abstraction, clarifying names and types, cleaning comments, a |

## creative-media

[Plugin e instalação](../domains/creative-media/README.md) · [Manifesto editorial](../catalog/curation/domains/creative-media.yaml)

Visual pieces and media - banners, slides, generative art, GIFs, images.

| Artefato | Tipo | Capacidade |
|---|---|---|
| [`creative-media:animated-gifs`](../domains/creative-media/skills/animated-gifs/SKILL.md) | skill | Use when making an animated GIF, especially for Slack or chat: size and frame limits, animation concepts, generation with Python and validation of the result. |
| [`creative-media:banner-design`](../domains/creative-media/skills/banner-design/SKILL.md) | skill | Use when designing banners and promotional graphics: social media posts and covers, display ads, website heroes and print, with several art directions to choose from and platform-correct siz |
| [`creative-media:generative-art`](../domains/creative-media/skills/generative-art/SKILL.md) | skill | Use when the user asks for art made with code: generative or algorithmic art in p5.js with seeded randomness, flow fields, particle systems and interactive parameters. |
| [`creative-media:image-prompting`](../domains/creative-media/skills/image-prompting/SKILL.md) | skill | Use when writing prompts for image-generation models: photographic direction (lens, light, composition), style control, and representation that avoids stereotyped or culturally inaccurate de |
| [`creative-media:poster-design`](../domains/creative-media/skills/poster-design/SKILL.md) | skill | Use when creating a static visual piece as a PNG or PDF: a poster, cover, print piece or art board composed from a written design philosophy, with bundled typefaces. |
| [`creative-media:presentation-slides`](../domains/creative-media/skills/presentation-slides/SKILL.md) | skill | Use when creating an HTML slide deck or presentation from scratch or from an outline: narrative structure, slide layouts, animation, charts with Chart.js and design tokens, or converting an |

## data

[Plugin e instalação](../domains/data/README.md) · [Manifesto editorial](../catalog/curation/domains/data.yaml)

Databases, migrations, data modelling and data engineering.

| Artefato | Tipo | Capacidade |
|---|---|---|
| [`data:data-pipelines`](../domains/data/skills/data-pipelines/SKILL.md) | skill | Use when building or fixing data pipelines and bulk data movement: ingestion, ETL/ELT, backfills, exports, warehouse or lakehouse loading, streaming, data quality checks and throughput probl |
| [`data:database-design`](../domains/data/skills/database-design/SKILL.md) | skill | Use when designing a schema, writing or optimising queries, choosing indexes, transactions or isolation levels, or reviewing database code for PostgreSQL, MySQL/MariaDB, Redis, ClickHouse or |
| [`data:database-migrations`](../domains/data/skills/database-migrations/SKILL.md) | skill | Use when changing a production database schema or data: writing migrations, renaming or dropping columns, backfills, adding indexes or constraints without downtime, and planning rollback. Ap |

## debugging

[Plugin e instalação](../domains/debugging/README.md) · [Manifesto editorial](../catalog/curation/domains/debugging.yaml)

Finding the cause of failures - diagnosis, build errors, silent failures.

| Artefato | Tipo | Capacidade |
|---|---|---|
| [`debugging:build-failure-resolution`](../domains/debugging/skills/build-failure-resolution/SKILL.md) | skill | Use when a build, compile, type-check, bundling or dependency step fails, or when errors are being swallowed silently: read the first real error, fix the smallest cause, rebuild, repeat; the |
| [`debugging:systematic-debugging`](../domains/debugging/skills/systematic-debugging/SKILL.md) | skill | Build a tight feedback loop on the exact symptom, find the root cause from evidence, then fix with a regression test. |

## documents

[Plugin e instalação](../domains/documents/README.md) · [Manifesto editorial](../catalog/curation/domains/documents.yaml)

Office documents and technical or corporate writing.

| Artefato | Tipo | Capacidade |
|---|---|---|
| [`documents:doc-coauthoring`](../domains/documents/skills/doc-coauthoring/SKILL.md) | skill | Use when the user wants to write a document together with you - a proposal, technical spec, decision doc, RFC or similar - through a structured workflow: gather context, refine section by se |
| [`documents:internal-comms`](../domains/documents/skills/internal-comms/SKILL.md) | skill | Use when writing internal communications: status reports, leadership updates, incident notices, company newsletters, FAQs and project updates, in the formats and tone a company expects. |
| [`documents:office-documents`](../domains/documents/skills/office-documents/SKILL.md) | skill | Use when a task reads or produces Word, Excel, PowerPoint or PDF files (.docx, .xlsx, .pptx, .pdf): creating, editing, converting, extracting tables or text, filling forms or merging. Routes |
| [`documents:technical-writing`](../domains/documents/skills/technical-writing/SKILL.md) | skill | Use when writing or updating developer documentation: READMEs, API references, guides, tutorials, runbooks, architecture overviews or code maps, and keeping docs in sync after code changes. |

## finance

[Plugin e instalação](../domains/finance/README.md) · [Manifesto editorial](../catalog/curation/domains/finance.yaml)

Bookkeeping, FP&A, pricing, tax.

| Artefato | Tipo | Capacidade |
|---|---|---|
| [`finance:accounting`](../domains/finance/skills/accounting/SKILL.md) | skill | Use for day-to-day accounting: bookkeeping, reconciliations, month-end close, accounts payable, expense tracking, financial statements, and tax planning questions to prepare for an accountan |
| [`finance:billing-operations`](../domains/finance/skills/billing-operations/SKILL.md) | skill | Use when building or operating billing: subscriptions, invoicing, payment providers, refunds and disputes, dunning, revenue reporting and customer billing issues. |
| [`finance:financial-analysis`](../domains/finance/skills/financial-analysis/SKILL.md) | skill | Use for financial modelling and planning: three-statement and unit-economics models, forecasts and budgets, scenario analysis, variance analysis, pricing models and investment memos. |

## languages

[Plugin e instalação](../domains/languages/README.md) · [Manifesto editorial](../catalog/curation/domains/languages.yaml)

Idiomatic knowledge per programming language and framework, one pack per language.

| Artefato | Tipo | Capacidade |
|---|---|---|
| [`languages:cpp`](../domains/languages/skills/cpp/SKILL.md) | skill | C++ patterns, testing, security, review and build knowledge, plus framework references. |
| [`languages:dart`](../domains/languages/skills/dart/SKILL.md) | skill | Dart and Flutter patterns, testing, security, review and build knowledge, plus framework references. |
| [`languages:dotnet`](../domains/languages/skills/dotnet/SKILL.md) | skill | C# and F# on .NET patterns, testing, security, review and build knowledge, plus framework references. |
| [`languages:external-tools`](../domains/languages/knowledge/external-tools.md) | knowledge | External language tools referenced, not vendored: react-doctor (restricted licence), godoctor, Vercel interface guidelines. |
| [`languages:go`](../domains/languages/skills/go/SKILL.md) | skill | Go patterns, testing, security, review and build knowledge, plus framework references. |
| [`languages:jvm`](../domains/languages/skills/jvm/SKILL.md) | skill | Java and Kotlin patterns, testing, security, review and build knowledge, plus framework references. |
| [`languages:php`](../domains/languages/skills/php/SKILL.md) | skill | PHP patterns, testing, security, review and build knowledge, plus framework references. |
| [`languages:python`](../domains/languages/skills/python/SKILL.md) | skill | Python patterns, testing, security, review and build knowledge, plus framework references. |
| [`languages:react-diagnostics`](../domains/languages/skills/react-diagnostics/SKILL.md) | skill | Use when finishing a feature, fixing a bug or before committing React code, or when the user types /doctor or asks to scan, triage or clean up React diagnostics. Runs React Doctor across lin |
| [`languages:ruby`](../domains/languages/skills/ruby/SKILL.md) | skill | Ruby patterns, testing, security, review and build knowledge, plus framework references. |
| [`languages:rust`](../domains/languages/skills/rust/SKILL.md) | skill | Rust patterns, testing, security, review and build knowledge, plus framework references. |
| [`languages:swift`](../domains/languages/skills/swift/SKILL.md) | skill | Swift patterns, testing, security, review and build knowledge, plus framework references. |
| [`languages:typescript`](../domains/languages/skills/typescript/SKILL.md) | skill | TypeScript and JavaScript patterns, testing, security, review and build knowledge, plus framework references. |

## legal-compliance

[Plugin e instalação](../domains/legal-compliance/README.md) · [Manifesto editorial](../catalog/curation/domains/legal-compliance.yaml)

Contracts, regulatory compliance, legal privacy.

| Artefato | Tipo | Capacidade |
|---|---|---|
| [`legal-compliance:compliance-programs`](../domains/legal-compliance/skills/compliance-programs/SKILL.md) | skill | Use when preparing for or checking compliance: SOC 2, ISO 27001, GDPR, CCPA, HIPAA or PCI-DSS readiness, privacy programmes and data processing, control mapping, evidence collection and poli |
| [`legal-compliance:contracts`](../domains/legal-compliance/skills/contracts/SKILL.md) | skill | Use when drafting, reviewing or organising contracts: master service agreements and order forms, clause review against a playbook, redlines, client intake and matter organisation. Drafts are |

## marketing

[Plugin e instalação](../domains/marketing/README.md) · [Manifesto editorial](../catalog/curation/domains/marketing.yaml)

SEO and answer-engine optimisation, content, social, email, paid media.

| Artefato | Tipo | Capacidade |
|---|---|---|
| [`marketing:campaign-planning`](../domains/marketing/skills/campaign-planning/SKILL.md) | skill | Use when planning a marketing campaign or launch end to end: goals, audience, positioning and messaging, channel mix, calendar, growth experiments, press and communications, and success metr |
| [`marketing:content-marketing`](../domains/marketing/skills/content-marketing/SKILL.md) | skill | Use when planning or producing marketing content: content strategy and calendars, articles and newsletters, LinkedIn and social posts, cross-posting across platforms, developer relations con |
| [`marketing:email-marketing`](../domains/marketing/skills/email-marketing/SKILL.md) | skill | Use when planning or writing marketing email: lifecycle and nurture sequences, newsletters, segmentation, deliverability, subject lines and A/B tests, and operating email tools. |
| [`marketing:paid-media`](../domains/marketing/skills/paid-media/SKILL.md) | skill | Use for paid acquisition: search (PPC) and paid social campaigns, programmatic and display buying, search-query mining, ad creative, conversion tracking and attribution, and auditing ad acco |
| [`marketing:seo`](../domains/marketing/skills/seo/SKILL.md) | skill | Use for search visibility: technical SEO audits, keyword and intent research, on-page optimisation, structured data, Core Web Vitals, answer-engine and AI-citation optimisation, and app stor |

## operations

[Plugin e instalação](../domains/operations/README.md) · [Manifesto editorial](../catalog/curation/domains/operations.yaml)

Project management, people operations, customer support, processes.

| Artefato | Tipo | Capacidade |
|---|---|---|
| [`operations:customer-support`](../domains/operations/skills/customer-support/SKILL.md) | skill | Use for customer support and success work: answering tickets, writing help-center replies and macros, escalations, onboarding and health checks for accounts, and turning support trends into |
| [`operations:people-operations`](../domains/operations/skills/people-operations/SKILL.md) | skill | Use for people operations: hiring plans and job descriptions, interview loops, onboarding new staff, training programmes, and managing organisational change. |
| [`operations:project-management`](../domains/operations/skills/project-management/SKILL.md) | skill | Use when running a project or programme: plans and milestones, status tracking, risks and dependencies, stakeholder updates, meeting notes and action items, and keeping a Jira or tracker wor |

## platform

[Plugin e instalação](../domains/platform/README.md) · [Manifesto editorial](../catalog/curation/domains/platform.yaml)

Git and GitHub, CI/CD, containers, deployment, observability, SRE, incidents.

| Artefato | Tipo | Capacidade |
|---|---|---|
| [`platform:deployment`](../domains/platform/skills/deployment/SKILL.md) | skill | Use when containerising, deploying or releasing software: Dockerfiles and Compose, Kubernetes workloads, CI/CD pipelines, health checks, blue-green and canary rollouts, rollback, post-deploy |
| [`platform:git-workflow`](../domains/platform/skills/git-workflow/SKILL.md) | skill | Use when choosing a branching strategy, writing commit messages, tidying history before a merge, resolving conflicts, rebasing versus merging, or setting up pre-commit hooks with formatting, |
| [`platform:github-operations`](../domains/platform/skills/github-operations/SKILL.md) | skill | Use when operating a GitHub repository with the gh CLI: managing pull requests and issues, checking and re-running CI, configuring Actions, branch protection and releases, or monitoring Depe |
| [`platform:incident-response`](../domains/platform/skills/incident-response/SKILL.md) | skill | Use when production is down or degraded, an alert fires, a breach is suspected, or a postmortem is due: assess severity, coordinate responders, communicate status, contain, recover, preserve |
| [`platform:reliability`](../domains/platform/skills/reliability/SKILL.md) | skill | Use when defining SLOs and error budgets, adding logs, metrics and traces, building operator dashboards (Grafana, SigNoz), planning capacity, running chaos experiments, or maintaining infras |

## principles

[Plugin e instalação](../domains/principles/README.md) · [Manifesto editorial](../catalog/curation/domains/principles.yaml)

Always-on coding behaviour for agents - simplicity, surgical changes, explicit assumptions, verifiable success criteria.

| Artefato | Tipo | Capacidade |
|---|---|---|
| [`principles:coding-discipline`](../domains/principles/skills/coding-discipline/SKILL.md) | skill | Make the smallest complete change, surface assumptions, keep diffs surgical and define a verifiable check. |

## product

[Plugin e instalação](../domains/product/README.md) · [Manifesto editorial](../catalog/curation/domains/product.yaml)

Product management - PRDs, prioritisation, feedback synthesis, experiments.

| Artefato | Tipo | Capacidade |
|---|---|---|
| [`product:product-management`](../domains/product/skills/product-management/SKILL.md) | skill | Use when doing product management work: writing a PRD or product brief, defining outcomes and success metrics, prioritising a backlog or sprint, synthesising user feedback into themes, plann |

## research

[Plugin e instalação](../domains/research/README.md) · [Manifesto editorial](../catalog/curation/domains/research.yaml)

Source-backed research with citations, literature reviews.

| Artefato | Tipo | Capacidade |
|---|---|---|
| [`research:docs-lookup`](../domains/research/skills/docs-lookup/SKILL.md) | skill | Use when the user asks how to use a library, framework, SDK or API, or before writing code against one whose current behaviour matters. Fetches up-to-date documentation (for example through |
| [`research:literature-review`](../domains/research/skills/literature-review/SKILL.md) | skill | Use for a systematic literature review or for evaluating scholarly work: search planning across academic databases, screening criteria, extraction, synthesis, citation checks, and structured |
| [`research:source-research`](../domains/research/skills/source-research/SKILL.md) | skill | Use when a question needs current or verifiable facts from outside the codebase: research a topic, compare options, check what a library or service does today, or produce a cited report. Pla |

## sales

[Plugin e instalação](../domains/sales/README.md) · [Manifesto editorial](../catalog/curation/domains/sales.yaml)

Prospecting, qualification, proposals, pipeline.

| Artefato | Tipo | Capacidade |
|---|---|---|
| [`sales:deal-strategy`](../domains/sales/skills/deal-strategy/SKILL.md) | skill | Use when working an active sales opportunity: discovery calls, qualification, mapping stakeholders, technical sales and demos, proposals, handling objections, pipeline reviews and forecastin |
| [`sales:investor-relations`](../domains/sales/skills/investor-relations/SKILL.md) | skill | Use when raising money: pitch decks, one-pagers, financial narratives, data rooms, and investor outreach and follow-up. |
| [`sales:prospecting`](../domains/sales/skills/prospecting/SKILL.md) | skill | Use when finding and reaching new customers: defining the ideal customer profile, building and scoring lead lists, finding warm paths, and writing personalised outbound sequences. |

## security

[Plugin e instalação](../domains/security/README.md) · [Manifesto editorial](../catalog/curation/domains/security.yaml)

Application and agent security - audits, threat modelling, secrets, supply chain, hardening.

| Artefato | Tipo | Capacidade |
|---|---|---|
| [`security:agent-security`](../domains/security/skills/agent-security/SKILL.md) | skill | Harden agents and harnesses against injection and over-permission; statically review MCP and hook configs. |
| [`security:external-references`](../domains/security/knowledge/external-references.md) | knowledge | Links and licence notes for security material referenced but not copied (Shannon, checklists, OWASP). |
| [`security:secrets-hygiene`](../domains/security/skills/secrets-hygiene/SKILL.md) | skill | Respond to exposed secrets rotation-first and set up scanning, brokering and rotation. |
| [`security:security-audit`](../domains/security/skills/security-audit/SKILL.md) | skill | Source-first security guidance or full audit with sandboxed validation and schema-checked findings. |
| [`security:threat-modeling`](../domains/security/skills/threat-modeling/SKILL.md) | skill | Map data flows and trust boundaries, run STRIDE, rank threats, and turn them into mitigations and tests. |

## testing

[Plugin e instalação](../domains/testing/README.md) · [Manifesto editorial](../catalog/curation/domains/testing.yaml)

Proving behaviour - TDD, test strategy, end-to-end and browser testing, verification before completion.

| Artefato | Tipo | Capacidade |
|---|---|---|
| [`testing:browser-testing`](../domains/testing/skills/browser-testing/SKILL.md) | skill | Use when testing a web application in a real browser: driving a local app with Playwright, writing or stabilising end-to-end tests, Page Objects, capturing screenshots and console logs, post |
| [`testing:test-driven-development`](../domains/testing/skills/test-driven-development/SKILL.md) | skill | Agree seams, then red-green-refactor one vertical slice at a time with honest, behaviour-level tests. |
| [`testing:test-strategy`](../domains/testing/skills/test-strategy/SKILL.md) | skill | Use when deciding how a project should be tested rather than writing one test: the test portfolio and coverage targets, linking requirements and risks to tests, API and contract tests, perfo |
| [`testing:verification-before-completion`](../domains/testing/skills/verification-before-completion/SKILL.md) | skill | Run verification fresh and read the output before claiming work is complete, fixed or passing. |

## ui

[Plugin e instalação](../domains/ui/README.md) · [Manifesto editorial](../catalog/curation/domains/ui.yaml)

Visual interface - aesthetic direction, typography, colour, layout, tokens, design systems, components, finish.

| Artefato | Tipo | Capacidade |
|---|---|---|
| [`ui:component-styling`](../domains/ui/skills/component-styling/SKILL.md) | skill | Use when implementing interface components and styles in code: shadcn/ui and Radix components, Tailwind utility styling, theming and dark mode, responsive layouts, CSS architecture, and appl |
| [`ui:design-system`](../domains/ui/skills/design-system/SKILL.md) | skill | Choose or generate a design system (style, palette, type, charts, icons, tokens) from a curated database. |
| [`ui:motion-and-polish`](../domains/ui/skills/motion-and-polish/SKILL.md) | skill | Use when an interface works but feels flat or rough: adding purposeful motion and transitions, micro-interactions, easing and timing, reduced-motion support, and the small craft details that |
| [`ui:visual-design`](../domains/ui/skills/visual-design/SKILL.md) | skill | Design and build new pages that look designed, with themes, job-first layout and browser-linted quality gates. |

## ux

[Plugin e instalação](../domains/ux/README.md) · [Manifesto editorial](../catalog/curation/domains/ux.yaml)

User experience - user research, flows, information architecture, usability heuristics, microcopy.

| Artefato | Tipo | Capacidade |
|---|---|---|
| [`ux:usability-review`](../domains/ux/skills/usability-review/SKILL.md) | skill | Expert walkthrough and heuristic evaluation of an interface or flow, with ranked fixes. |
| [`ux:user-research`](../domains/ux/skills/user-research/SKILL.md) | skill | Plan, run and synthesise user research that informs a concrete product decision. |

## workflow

[Plugin e instalação](../domains/workflow/README.md) · [Manifesto editorial](../catalog/curation/domains/workflow.yaml)

Delivery lifecycle - ideation, specs, plans, execution, worktrees, branch completion, handoff, retrospectives, tickets.

| Artefato | Tipo | Capacidade |
|---|---|---|
| [`workflow:brainstorming`](../domains/workflow/skills/brainstorming/SKILL.md) | skill | Find out what the user wants and why, compare approaches, and get a written spec approved before building. |
| [`workflow:executing-plans`](../domains/workflow/skills/executing-plans/SKILL.md) | skill | Build an approved plan task by task, via subagents or inline, with TDD, a ledger and a final branch review. |
| [`workflow:feature-delivery`](../domains/workflow/workflows/feature-delivery/SKILL.md) | workflow | Orchestrate the stages from idea to merge-ready branch with an approval gate between each stage. |
| [`workflow:finishing-a-branch`](../domains/workflow/skills/finishing-a-branch/SKILL.md) | skill | Decide how finished work is integrated: merge, pull request, keep or discard, and clean up. |
| [`workflow:git-worktrees`](../domains/workflow/skills/git-worktrees/SKILL.md) | skill | Create an isolated worktree or branch from the right base with a passing baseline before building. |
| [`workflow:grilling`](../domains/workflow/skills/grilling/SKILL.md) | skill | Stress-test an existing plan or decision through rounds of questions over a design tree. |
| [`workflow:handoff`](../domains/workflow/skills/handoff/SKILL.md) | skill | Write or resume a handoff document so another session or person continues without re-deriving context. |
| [`workflow:initiative-mapping`](../domains/workflow/skills/initiative-mapping/SKILL.md) | skill | Chart an initiative too big for one session as a map of decision tickets resolved one at a time. |
| [`workflow:issue-breakdown`](../domains/workflow/skills/issue-breakdown/SKILL.md) | skill | Break approved work into tracer-bullet tickets with blocking edges and publish them to the tracker. |
| [`workflow:issue-tracking`](../domains/workflow/knowledge/issue-tracking) | knowledge | How to create, link, label and query issues on GitHub, GitLab or local markdown trackers. |
| [`workflow:issue-triage`](../domains/workflow/skills/issue-triage/SKILL.md) | skill | Move issues and external pull requests through triage roles and write agent-ready briefs. |
| [`workflow:writing-plans`](../domains/workflow/skills/writing-plans/SKILL.md) | skill | Turn an approved spec into plan.md and tasks.md with exact files, interfaces, tests and commands. |
