# Agent security — mcp implementation security review

Part of `security:agent-security`. Adapted reference material; the owner procedure, project conventions, scope and authorization rules take precedence. Examples are not automatically executed.

## MCP Implementation Security Review

<!-- source: github/awesome-copilot skills/mcp-implementation-security-review/SKILL.md#controls-reference,owasp-mcp-top-10,reference -->

### Reference

#### Decision rules
- **Network-exposed server:** Apply **all 5 controls**, document which checks apply within the approved scope. Do not execute probes without explicit authorization.
- **Local/STDIO server:** Give **best-practice guidance only** for the 5 controls; still run RCE because tool input can execute locally.
- **Client:** Review received-token handling and refusal to trust server-provided session IDs; do not force server controls unless asked.
- **Reverse proxy or container exposure:** If traffic can reach the server over a network, treat it as **network-exposed** even if inner binding is localhost.
- **Unclear evidence:** Do not guess. Mark **NEEDS INVESTIGATION** and say what must be verified manually.
- **Ambiguous auth coverage:** Auth middleware exists but it is unclear whether it covers MCP endpoints → mark **NEEDS INVESTIGATION**.
- **Undeterminable transport:** If transport cannot be established from code, flag for manual review and do **not** assume STDIO — defaulting to STDIO would wrongly skip the server controls.

#### Transport classification

**Network-exposed (enforce all controls):**

| Pattern | Transport |
|---|---|
| `transport="http"` or `transport="sse"` | HTTP/SSE |
| `StreamableHttpServerTransport` | HTTP (TS/JS) |
| `SSEServerTransport` | SSE (TS/JS) |
| `WithHttpTransport()` | HTTP (C#) |
| `host="0.0.0.0"` | All-interfaces binding |
| Express `.listen(port)` with MCP routes | HTTP (default `0.0.0.0`) |
| `EXPOSE` in Dockerfile + MCP server | Network-exposed |

**Local-only (best practices only):**

| Pattern | Transport |
|---|---|
| `StdioServerTransport` | STDIO (TS/JS) |
| `WithStdioServerTransport()` | STDIO (C#) |
| `transport="stdio"` | STDIO |
| `mcp.run()` with no args (Python FastMCP) | STDIO default |
| `.vscode/mcp.json` with `command` key and no URL | STDIO child process |

**Host binding gotchas:**

| Binding | Actual exposure |
|---|---|
| `host="0.0.0.0"` | 🔴 Network-exposed |
| `host="127.0.0.1"` or `localhost` | 🟢 Local-only |
| No explicit host (Express/Node) | 🔴 Defaults to `0.0.0.0` |
| No explicit host (Python FastMCP) | 🟡 Depends on transport — verify |
| Docker `ports: "8000:8000"` | 🔴 Network-exposed even if the process binds `127.0.0.1` inside the container |

#### False Positive Filters

| FP pattern | How to detect |
|---|---|
| `.github/skills/` templates | Path contains `.github/skills/` — skill template, not server code |
| Vendored SDK / OSS copies | File defines `class FastMCP`, `class McpServer`, or path is in `node_modules/`, `vendor/` |
| MCP client configs | `.vscode/mcp.json` with `inputs`/`servers` but no server code |
| Documentation / tutorials | `.md`, `.rst` with code fences unrelated to the repo's own server |
| Outbound-only auth libraries | `DefaultAzureCredential`, service account JSON, or similar used only for outbound auth |

Docs describing the repo's **own** server behavior, transport, auth posture, or deployment are **not** false positives.

### Controls Reference

#### MCP-01 — Identity isolation
**Scope:** Remote MCP servers

**Condition**
- Authenticate every inbound request with a trusted identity provider and enforce authorization at the server boundary; do not infer auth from session IDs, prior requests, or network location.
- Use a **unique server-specific application identity** and audience/resource identifier; outbound calls use independently scoped service credentials or on-behalf-of flow where required, never the inbound token.
- Unauthenticated discovery endpoints are allowed only for metadata-only OAuth/MCP bootstrapping: `/.well-known/oauth-protected-resource`, `/.well-known/oauth-authorization-server`, `/.well-known/openid-configuration`.

**What to check**
- Token validation and authorization middleware run on every MCP route; authorization distinguishes tool invoke, read-only, and admin operations if present.
- Identity config shows a dedicated application/client/resource ID and audience; outbound clients acquire their own tokens and never copy inbound `Authorization`.
- Discovery endpoints return metadata only and cannot execute tools or expose protected data.

**Key pitfall:** Shared application identities or forwarded caller tokens break identity isolation and create confused-deputy paths.

#### MCP-02 — Sessions
**Scope:** Remote MCP servers that support sessions

**Applicability**
- No session identifiers issued or used anywhere → mark **N/A** (per-request auth is still required; see MCP-01).
- Sessions managed by the transport/SDK (e.g., Streamable HTTP `Mcp-Session-Id`) but generation/binding not visible in source → mark **NEEDS INVESTIGATION**, not FAIL.
- Session identifiers present in code → score **PASS/FAIL** against the conditions below.

**Condition**
- Authenticate and authorize **every** request; session state never substitutes for token validation.
- Session IDs are opaque correlation/continuity tokens only; they do not grant privileges, encode authorization, or bypass auth.
- Session IDs are CSPRNG-generated, unpredictable, bound to an authenticated context, and never embedded in URLs.

**What to check**
- Middleware validates tokens per request, not only when a session starts.
- Authorization logic never trusts a session ID alone; loss or reuse of a session ID must not grant access.
- Session creation uses random IDs (GUID v4/CSPRNG acceptable; sequential or time-based IDs are not).

**Key pitfall:** Treating a session ID as a bearer credential turns a correlation token into authentication.

#### MCP-03 — Rate limits
**Scope:** MCP servers and tools

**Condition**
- Enforce rate limits and abuse protection on tool discovery and tool invocation.
- Enforce limits **at the MCP server runtime**, not only at a gateway; partition by authenticated identity and by session where sessions exist.
- Apply stricter limits to mutation-capable and high-cost tools; when limits are exceeded, fail closed with **HTTP 429** and **Retry-After** and do not execute the tool.

**What to check**
- Rate-limit middleware or equivalent is present on discovery and invocation endpoints in server code, not just in ingress or proxy config.
- Limits are keyed by identity and session, with tighter budgets for write/high-cost operations.
- Exceeded requests stop before backend action and return 429 with Retry-After.

**Starting thresholds** (tune to actual load, downstream limits, and cost):

| Tool type | Per-identity | Per-session | Notes |
|---|---|---|---|
| Read-only / listing | 100/min | 200/min | Lower if downstream APIs are sensitive |
| Mutation / write | 10/min | 20/min | Stricter for state-changing ops |
| High-cost compute | 5/min | 10/min | Cost-weighted; watch cloud spend |
| Tool discovery | 30/min | 60/min | Prevents enumeration abuse |

**Key pitfall:** Gateway-only throttling or one flat bucket leaves bypasses and under-protects expensive tools.

#### MCP-04 — Schema validation
**Scope:** MCP servers exposing tools with structured arguments

**Condition**
- Validate **all** tool arguments against explicit schemas **before execution**.
- Schemas define types, required fields, enums, and bounds, and reject unspecified properties by default (`additionalProperties: false` or equivalent).
- Validation runs server-side on every invocation; invalid input fails closed with a 400/MCP error and no backend action.

**What to check**
- Each tool descriptor has a schema covering types, required fields, enums, bounds, and property restrictions.
- Validation occurs at the server boundary on every call, not only in clients, gateways, or downstream services.
- Negative tests reject malformed input, extra properties, and bounds violations.

**Key pitfall:** Allowing extra properties or client-only validation creates hidden attack surface and scope creep.

#### MCP-05 — SDK-first
**Scope:** Remote MCP servers

**Condition**
- Build remote MCP servers on an **official MCP SDK** for your server's language:
  - **Tier 1 (fully supported):** TypeScript (modelcontextprotocol/typescript-sdk), Python (modelcontextprotocol/python-sdk), C#/.NET (modelcontextprotocol/csharp-sdk), Go (modelcontextprotocol/go-sdk)
  - **Tier 2/3 (developing):** Java (modelcontextprotocol/java-sdk), Kotlin (modelcontextprotocol/kotlin-sdk), Rust (modelcontextprotocol/rust-sdk), Swift (modelcontextprotocol/swift-sdk), PHP (modelcontextprotocol/php-sdk), Ruby (modelcontextprotocol/ruby-sdk)
- If not using an official SDK, mark MCP-05 as NEEDS INVESTIGATION.
- Keep the SDK current and patched, and verify which controls are automatic versus manual.

**What to check**
- Dependencies reference an official MCP SDK rather than a hand-rolled HTTP/SSE stack.
- If no SDK is used, the repo contains direct evidence for auth/authz, sessions, rate limits, and schema validation.
- Dependency pinning and update hygiene show the SDK is maintained.

**Key pitfall:** Hand-rolled servers often miss one "small" primitive—per-request auth, throttling, or validation—and the gaps compound.

### OWASP MCP Top 10

**MCP01:2025 — Token Mismanagement & Secret Exposure**
Test: Search for hardcoded secrets and token logging; verify secrets come from env vars or a secrets manager; verify short-lived/rotated tokens.
Pass: No hardcoded secrets, sensitive fields redacted, short-lived/rotated tokens. Fail: Hardcoded secrets, token logging, or long-lived tokens without rotation.

**MCP02:2025 — Privilege Escalation via Scope Creep**
Test: Review scopes/roles; confirm least privilege and per-request authorization; reject wildcard admin scopes unless justified; check for runtime capability expansion.
Pass: Least-privilege scopes, per-request authorization, no runtime capability expansion. Fail: Broad scopes, one-time auth only, or self-escalating tools.

**MCP03:2025 — Tool Poisoning**
Test: Check whether tool definitions are static and server-controlled, whether tools can alter metadata, and whether outputs contain LLM-parseable instructions.
Pass: Static server-controlled definitions and data-only outputs. Fail: External metadata sources or outputs with embedded instructions.

**MCP04:2025 — Supply Chain Attacks & Dependency Tampering**
Test: Check for lock files, exact pinning, suspicious `postinstall` scripts, dependency audit results, and trusted registries.
Pass: Pinned deps, committed lock file, no known vulnerabilities, no suspicious post-install scripts. Fail: Unpinned deps, no lock file, unpatched CVEs, or untrusted registries.

**MCP05:2025 — Command Injection & Execution**
Test: Search for shell execution APIs and string-built commands; trace whether tool input reaches shell execution; test `; ls`, `$(whoami)`, `| cat /etc/passwd`.
Pass: No shell execution from untrusted input, or only parameterized allowlisted execution. Fail: User input reaches shell commands, `shell=True` with formatted strings, or unsafe concatenation.

**MCP06:2025 — Prompt Injection via Contextual Payloads**
Test: Check whether tool output goes back to the LLM, whether external content is sanitized/truncated/sandboxed, and whether chained tool calls are guarded; test adversarial instruction-bearing output.
Pass: Tool outputs are data, untrusted content is sanitized/truncated/sandboxed, and chaining has guardrails. Fail: Raw external content returns to the model and there are no chaining limits.

**MCP07:2025 — Insufficient Authentication & Authorization**
Test: Send requests without auth and with expired/invalid tokens; verify per-tool authorization; confirm auth is enforced in the server, not only at the gateway.
Pass: All endpoints require valid auth, per-tool authorization exists, and enforcement happens server-side. Fail: Any unauthenticated access, missing per-tool auth, or gateway-only enforcement.

**MCP08:2025 — Lack of Audit and Telemetry**
Test: Invoke a tool and confirm logs capture caller identity, tool name, and timestamp; trigger an error and confirm useful context; verify centralized logging and alerting.
Pass: Tool invocations are logged with identity, logs are centralized, and alerts exist. Fail: Missing logs, no caller identity, local-only logging, or no alerting.

**MCP09:2025 — Shadow MCP Servers**
Test: Verify the server exists in service inventory; inspect for undocumented MCP endpoints or exposed non-standard ports; check dev/staging isolation; verify an owner and review trail.
Pass: All servers are inventoried, isolated appropriately, and owned. Fail: Undocumented servers, dev/test exposure into production networks, or no ownership.

**MCP10:2025 — Context Injection & Over-Sharing**
Test: Inspect tool responses for data minimization; check for PII or full objects when only subsets are needed; verify context isolation.
Pass: Minimal data is returned, sensitive fields are masked/excluded, and context is isolated. Fail: Full objects are returned unnecessarily, PII is exposed, or context is shared across users.
