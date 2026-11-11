# Api design — protobuf grpc api review

Part of `architecture:api-design`. Adapted reference material; the owner procedure, project conventions, scope and authorization rules take precedence. Examples are not automatically executed.

## Protobuf and gRPC API Review

<!-- source: github/awesome-copilot skills/protobuf-grpc-api-review/SKILL.md#review-workflow -->

### Review Workflow

#### 1. Inventory Contract Changes

Compare the old and new definitions by fully qualified symbol. Record:

- message fields: number, name, type, cardinality, presence, `oneof`, defaults, and relevant options
- enums: value name, number, aliases, reservations, and zero value
- services: package, service, method, request and response types, and streaming mode
- generated API inputs: package options, outer class names, namespaces, and custom options

Ignore formatting-only changes after confirming they do not alter descriptors or generated APIs.

#### 2. Evaluate Four Compatibility Dimensions

Assess each affected symbol independently:

1. **Binary wire** — can old and new readers parse both old and new bytes without corruption or loss?
2. **Named formats** — do ProtoJSON, text-format, REST-transcoded, or name-based consumers still work?
3. **Source and generated API** — will regenerated clients compile and preserve presence, enum, and accessor behavior?
4. **Behavior and operations** — do status codes, retry safety, deadlines, authorization, streaming, and resource bounds preserve the RPC contract?

Read protobuf compatibility rules for field, enum, presence, `oneof`, and serialization changes. Read gRPC contract review when services, methods, or runtime behavior change.

#### 3. Trace Mixed-Version Scenarios

For every non-trivial change, reason through these paths:

- old writer -> new reader
- new writer -> old reader
- old reader modifies and reserializes a new message
- rollback after new writers have emitted new values
- persisted old data read after the migration

For conditionally compatible changes, identify the exact writer constraint and the point at which it may be relaxed. A safe rollout commonly requires deploying readers before writers and retaining the old field or method until rollback is no longer needed.

#### 4. Review Repository Evidence

Use the repository's own tooling when available:

- compile descriptors with the project's `protoc`, Buf, Gradle, Maven, Bazel, or language-specific task
- run configured breaking-change or lint checks
- inspect generated-code diffs only when they are committed by repository convention
- search call sites for exhaustive enum switches, presence assumptions, JSON field names, method paths, status handling, and retry configuration
- look for compatibility fixtures or descriptor baselines before proposing a new mechanism

Do not claim a check passed unless you ran it. If a required tool or baseline is unavailable, name the unverified risk.

#### 5. Produce an Actionable Review

Lead with one verdict:

- **Compatible** — safe within the stated compatibility envelope
- **Rollout-dependent** — parseable, but safe only with explicit sequencing or value constraints
- **Breaking** — causes wire, named-format, source, or behavioral incompatibility
- **Insufficient context** — the old schema, encoding, consumers, or deployment model is unknown

Then provide only evidence-backed findings. For each finding include:

```text
[severity] Short title
Location: file and symbol or changed lines
Dimension: binary | JSON/text | source | behavior/operations
Change: old contract -> new contract
Impact: concrete failing mixed-version scenario
Remediation: smallest safe schema change or staged migration
```

Use **blocker** for corruption, unparsable data, tag reuse, or an unavoidable production break; **high** for likely cross-version data loss or unsafe RPC behavior; **medium** for bounded compatibility or operability risks; and **low** for maintainability issues that do not break the contract. Do not inflate style preferences into compatibility findings.

Conclude with:

- a compact compatibility matrix for changed symbols
- the rollout/rollback sequence if migration is required
- targeted tests that would prove the remaining assumptions
