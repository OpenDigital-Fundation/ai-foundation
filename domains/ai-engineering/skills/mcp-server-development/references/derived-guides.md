# MCP server development — derived guides

Part of `ai-engineering:mcp-server-development`.

## FastMCP 3.0 Server Development

<!-- source: davila7/claude-code-templates cli-tool/components/skills/development/fastmcp-server/SKILL.md#key-concepts -->

### Key concepts

#### Tools
Functions exposed as executable capabilities for LLMs. Decorated with `@mcp.tool`. Support Pydantic validation, async, custom return types, and annotations (readOnlyHint, destructiveHint).

#### Resources & Templates
Static or dynamic data sources identified by URIs. Resources use fixed URIs (`data://config`), templates use parameterized URIs (`users://{id}/profile`). Support MIME types, annotations, and wildcard parameters.

#### Context
The `Context` object provides access to MCP features within tools/resources: logging, progress reporting, resource access, LLM sampling, user elicitation, and session state.

#### Dependency Injection
Inject values into tool/resource functions using `Depends()`. Supports HTTP requests, access tokens, custom dependencies, and generator-based cleanup patterns.

#### Providers
Control where components come from. `LocalProvider` (default, decorator-based), `FileSystemProvider` (load from Python files on disk), `SkillsProvider` (packaged bundles), or custom providers.

#### Authentication & Authorization
Multiple auth patterns: token verification (JWT, JWKS), OAuth proxy, OIDC proxy, remote OAuth, and full OAuth server. Authorization via scopes on components and middleware.

#### Middleware
Intercept and modify requests/responses. Built-in middleware for rate limiting, error handling, logging, and response size limits. Custom middleware via `@mcp.middleware`.
