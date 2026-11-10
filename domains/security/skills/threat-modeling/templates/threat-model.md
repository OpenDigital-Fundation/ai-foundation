# Threat model — <system or feature>

- **Date:** YYYY-MM-DD · **Spec:** <path> · **Owner:** <team>

## System overview

- **Architecture:** <monolith / services / serverless / agent + tools>
- **Stack:** <languages, frameworks, data stores, cloud>
- **Data classification:** <credentials, personal, financial, health, public>
- **External integrations:** <payments, identity providers, third-party APIs, MCP servers>

## Trust boundaries

| Boundary | From | To | Existing controls |
|---|---|---|---|
| Internet → App | End user | API gateway | TLS, rate limiting |

## Threats (STRIDE)

| # | Threat | Component | Likelihood × impact | Attack scenario | Mitigation | Test |
|---|---|---|---|---|---|---|
| 1 | Elevation of privilege | Admin API | High × Critical | IDOR on `/admin/users/:id` | Server-side RBAC check | `test_admin_requires_role` |

## Attack surface

- **External:**
- **Internal:**
- **Data:**
- **Infrastructure:**
- **Supply chain:**

## Accepted risks

<Threats consciously not mitigated now, with the reason and the review date.>
