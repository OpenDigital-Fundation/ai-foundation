"""Keyword heuristic that suggests a domain for an upstream artifact.

Deliberately simple: the suggestion is reviewed in each domain's catalog spec.
Rules are ordered; the first match wins.
"""
from __future__ import annotations

import re

RULES: list[tuple[str, str]] = [
    ("out-of-scope", r"game|godot|unity|unreal|roblox|blender|gis|cartograph|geo|spatial|xr |visionos|drone|bim|wechat|weibo|douyin|kuaishou|bilibili|xiaohongshu|zhihu|baidu|china|feishu|korean|french|healthcare|clinical|medical|hipaa|emr|cdss|defi|solidity|blockchain|evm|keccak|x402|trading|prediction-market|ito-|homelab|pihole|wireguard|vlan|cisco|netmiko|bgp|network-|logistics|carrier|customs|energy|inventory-demand|production-scheduling|returns-reverse|real estate|loan|hospitality|aging parent|study abroad|music|bengali|perl|zk steward|nasiko|openclaw|ecc-|ecc_|configure-ecc|hermes|deepseek|nanoclaw|santa|gan-|ralphinho|dmux|flox|uncloud|tinystruct|manim|remotion|videodb|tasteforge|video|esign|visa-doc|scientific-db|gaussdb|drupal|wordpress|servicenow|salesforce|filament|uswds|section 508|fedramp|orgscript|ats validator|astra"),
    ("accessibility", r"a11y|accessib|inclusive"),
    ("ux", r"\bux\b|ux |persona walkthrough|usability|user research|ux-copy|behavioral nudge|whimsy"),
    ("brand", r"brand"),
    ("ui", r"\bui\b|ui-|ui |hallmark|frontend-design|design-system|design system|theme|taste|liquid-glass|make-interfaces|motion|visual|styling|finish-gate|design-review"),
    ("creative-media", r"banner|slides|canvas|algorithmic-art|gif|image prompt|storyteller|social photo|logo|icon-gen|carousel|frontend-slides"),
    ("security", r"secur|pentest|threat|secret|vuln|bounty|osint|privacy|identity & access|safety-guard|gateguard|harden|mcp-dependency|incident respond|compliance auditor"),
    ("agent-engineering", r"skill|agent|harness|hook|loop|orchestrat|subagent|parallel|context|token|memory|instinct|learn|council|prompt-optim|cost-aware|model-route|session|workspace-surface|automation-audit|rules-distill|team-builder|devfleet|chief-of-staff|wayfinder|using-superpowers|diagnosing-superpowers|writing-for-agents|teach|loop-me|strategic-compact|conversation-analyzer|plankton|plan-orchestrate|multi-"),
    ("ai-engineering", r"llm|rag|prompt|claude-api|mcp|eval|pytorch|mle|ml-|ai engineer|post-training|model qa|recsys|search relevance|voice ai|foundation-models|regex-vs-llm|fal-ai|knowledge graph"),
    ("testing", r"tdd|test|e2e|qa|verification|verif|benchmark|reality checker|evidence collector|coverage|quality-gate|canary"),
    ("debugging", r"debug|diagnos|build-error|build-fix|resolver|-build|silent-failure|troubleshoot"),
    ("code-quality", r"review|simplif|refactor|clean|debt|code-quality|coding-standards|minimal change|audit|comment-analyzer|type-design|ponytail|karpathy|codehealth"),
    ("architecture", r"architect|domain-model|codebase-design|adr|decision-record|api-design|hexagonal|contract-first|backend|system|deep-modules|codebase-onboard|code-tour|codebase archaeolog|spec-miner|blueprint|code-explorer|lsp"),
    ("workflow", r"brainstorm|plan|spec|prd|prp|grill|ticket|triage|implement|execut|worktree|finishing|handoff|retro|prototype|feature-dev|epic|wizard|questionnaire|wait-what|intent-driven|story-lifecycle|checkpoint|resume|save|aside|project-init|issue-review|change-impact|delivery-gate|orch-"),
    ("platform", r"git|github|docker|kubernetes|deploy|devops|sre|platform|infrastructure|pm2|ci|pre-commit|release|incident|observab|dashboard-builder|finops|jira|terminal"),
    ("data", r"postgres|mysql|redis|clickhouse|database|migration|jpa|prisma|mybatis|data engineer|data-|sql|exposed"),
    ("languages", r"typescript|javascript|python|django|fastapi|go|golang|rust|java|kotlin|spring|quarkus|swift|dart|flutter|csharp|dotnet|fsharp|cpp|php|laravel|ruby|rails|react|vue|nuxt|nextjs|angular|vite|bun|node|nestjs|android|compose|ktor|celery|frontend|mobile|desktop|webassembly|wasm|i18n|internationaliz|backend-patterns|error-handling|cms"),
    ("documents", r"docx|pdf|pptx|xlsx|doc-|docs|document|technical writer|internal-comms|article|writing|nutrient|book|grant|translator|report"),
    ("research", r"research|literature|scholar|search-first|exa-|deep-research|iterative-retrieval|trend|synthesis|anthropolog|historian|statistic|psycholog|narratolog"),
    ("product", r"product|sprint|feedback|experiment|roadmap|dx engineer|lens|capability|discernment|market-research|competitive"),
    ("marketing", r"market|seo|aeo|content|social|growth|email|podcast|linkedin|twitter|x-api|tiktok|instagram|reddit|community|pr & comm|ppc|paid|ad creative|programmatic|tracking|crosspost|publisher|app store|developer advocate|citation|search query"),
    ("sales", r"sales|deal|pipeline|outbound|lead|proposal|account strateg|offer|discovery coach|investor|outreach|enrichment|signal-scorer|mutual-mapper|connections"),
    ("finance", r"financ|bookkeep|fp&a|tax|invest|billing|pricing|cfo|accounts payable|cost-|budget"),
    ("legal-compliance", r"legal|compliance|contract|agreement|esg|governance"),
    ("operations", r"operation|project|meeting|studio|hr |onboarding|recruit|training|change management|customer|support|service|workflow|ops|consolidation|chief|executive|analytics|strategist|consult|psychologist|mentor|resume"),
]
_COMPILED = [(d, re.compile(p)) for d, p in RULES]

DIVISIONS = {"design": "ui", "engineering": "languages", "finance": "finance", "marketing": "marketing",
             "paid-media": "marketing", "product": "product", "project-management": "operations",
             "research": "research", "sales": "sales", "security": "security", "specialized": "operations",
             "support": "operations", "testing": "testing", "academic": "research", "strategy": "product"}
OUT_OF_SCOPE_DIVISIONS = {"game-development", "gis", "healthcare", "spatial-computing"}


def classify(name: str, kind: str, path: str, division: str = "") -> str:
    text = f" {name} ".lower()
    if kind in {"rule", "hook", "command"}:
        text += " " + "/".join(path.split("/")[1:-1]).lower()
    domain = next((d for d, rx in _COMPILED if rx.search(text)), "unclassified")
    if division in OUT_OF_SCOPE_DIVISIONS:
        return "out-of-scope"
    if domain == "unclassified" and division:
        domain = DIVISIONS.get(division, domain)
    if domain == "unclassified" and kind == "rule":
        domain = "principles" if path.startswith("rules/common") or path.count("/") < 2 else "languages"
    if domain == "unclassified" and kind == "hook":
        domain = "agent-engineering"
    return domain
