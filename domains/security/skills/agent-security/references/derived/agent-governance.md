# Agent security — agent governance

Part of `security:agent-security`. Adapted reference material; the owner procedure, project conventions, scope and authorization rules take precedence. Examples are not automatically executed.

## Agent Governance Patterns

<!-- source: github/awesome-copilot skills/agent-governance/SKILL.md#pattern-1-governance-policy -->

### Pattern 1: Governance Policy

Define what an agent is allowed to do as a composable, serializable policy object.

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import re

class PolicyAction(Enum):
    ALLOW = "allow"
    DENY = "deny"
    REVIEW = "review"  # flag for human review

@dataclass
class GovernancePolicy:
    """Declarative policy controlling agent behavior."""
    name: str
    allowed_tools: list[str] = field(default_factory=list)       # allowlist
    blocked_tools: list[str] = field(default_factory=list)       # blocklist
    blocked_patterns: list[str] = field(default_factory=list)    # content filters
    max_calls_per_request: int = 100                             # rate limit
    require_human_approval: list[str] = field(default_factory=list)  # tools needing approval

    def check_tool(self, tool_name: str) -> PolicyAction:
        """Check if a tool is allowed by this policy."""
        if tool_name in self.blocked_tools:
            return PolicyAction.DENY
        if tool_name in self.require_human_approval:
            return PolicyAction.REVIEW
        if self.allowed_tools and tool_name not in self.allowed_tools:
            return PolicyAction.DENY
        return PolicyAction.ALLOW

    def check_content(self, content: str) -> Optional[str]:
        """Check content against blocked patterns. Returns matched pattern or None."""
        for pattern in self.blocked_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return pattern
        return None
```

#### Policy Composition

Combine multiple policies (e.g., org-wide + team + agent-specific):

```python
def compose_policies(*policies: GovernancePolicy) -> GovernancePolicy:
    """Merge policies with most-restrictive-wins semantics."""
    combined = GovernancePolicy(name="composed")

    for policy in policies:
        combined.blocked_tools.extend(policy.blocked_tools)
        combined.blocked_patterns.extend(policy.blocked_patterns)
        combined.require_human_approval.extend(policy.require_human_approval)
        combined.max_calls_per_request = min(
            combined.max_calls_per_request,
            policy.max_calls_per_request
        )
        if policy.allowed_tools:
            if combined.allowed_tools:
                combined.allowed_tools = [
                    t for t in combined.allowed_tools if t in policy.allowed_tools
                ]
            else:
                combined.allowed_tools = list(policy.allowed_tools)

    return combined


# Usage: layer policies from broad to specific
org_policy = GovernancePolicy(
    name="org-wide",
    blocked_tools=["shell_exec", "delete_database"],
    blocked_patterns=[r"(?i)(api[_-]?key|secret|password)\s*[:=]"],
    max_calls_per_request=50
)
team_policy = GovernancePolicy(
    name="data-team",
    allowed_tools=["query_db", "read_file", "write_report"],
    require_human_approval=["write_report"]
)
agent_policy = compose_policies(org_policy, team_policy)
```

#### Policy as YAML

Store policies as configuration, not code:

```yaml
# governance-policy.yaml
name: production-agent
allowed_tools:
  - search_documents
  - query_database
  - send_email
blocked_tools:
  - shell_exec
  - delete_record
blocked_patterns:
  - "(?i)(api[_-]?key|secret|password)\\s*[:=]"
  - "(?i)(drop|truncate|delete from)\\s+\\w+"
max_calls_per_request: 25
require_human_approval:
  - send_email
```

```python
import yaml

def load_policy(path: str) -> GovernancePolicy:
    with open(path) as f:
        data = yaml.safe_load(f)
    return GovernancePolicy(**data)
```

---
