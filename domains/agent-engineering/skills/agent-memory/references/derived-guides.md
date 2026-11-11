# Agent memory — derived guides

Part of `agent-engineering:agent-memory`.

## Context Architecture: bind a repository's claims to mechanisms

<!-- source: davila7/claude-code-templates cli-tool/components/skills/development/context-architecture/SKILL.md#the-nine-principles,the-kinds-of-mechanism-not-tools -->

### The kinds of mechanism (not tools)

Binding a claim is connecting it to something that fails when it stops being true. Context
Architecture names the kinds of mechanism; the repository picks the product (`oxlint` or `eslint`,
it makes no difference), and the infrastructure runs it on each change.

- **The compiler** catches what can be expressed in types: reintroducing a forbidden import breaks
  the build.
- **The linter** catches problems of structure and convention: a file in the wrong folder fails the
  lint and cites the rule it breaks.
- **Automated tests** catch documentation that lies and behavior that strays: an `AGENTS.md` that
  mentions a deleted file turns the tests red.
- **Review**, by a person or an agent, catches the meaning the others do not see: on each change it
  asks whether any document now says something false, and requires the fix in the same change. Review
  by an agent counts only when its verdict can stop the change (a required check, a request for
  changes), not a comment nobody must resolve, and its approval never authorizes a change to the
  verification surface.

Where a mechanism fires is the infrastructure's choice: a hook the repository commits runs it in the
agent's loop, the repository's rules run it at push, or CI runs it. Firing early does not replace the
gate, because a hook can be switched off locally. The split is clean: Context Architecture decides
**what** gets verified and guarantees the mechanism exists and fails. The infrastructure runs it.

### The nine principles

Each principle is a property you can check, not an aspiration. Either it is true of the repository
and bound to a mechanism, or it is not. If it cannot be bound to something that fails, it is not a
principle.

#### Let the repository say what it is

**01 · Structure Screams Intent.** The file tree says what the system does, not what framework built
it. A `billing/` folder names a business responsibility; a `controllers/` folder names a technical
detail that could belong to any system. The framework lives one level down, inside the domain it
serves.
_Mechanism: a linter rule that errors when a file lands in a folder that does not match its domain._

**02 · Context Lives With Code.** Context lives next to the code it describes, at every important
boundary, not in a separate wiki that goes stale. It holds only what the code cannot say on its own:
where the source of truth is, what invariants must be respected, what tech debt was accepted on
purpose, what behavioral limits apply.
_Mechanism: a test that fails if an `AGENTS.md` mentions a file that no longer exists._

**03 · Boundaries Are Explicit and Named.** Each module and package is named for the responsibility
it owns. Folders like `utils/`, `common/`, or `helpers/` collect anything, because the name rules
nothing out. Genuinely shared, domain-free code goes in a small `shared/` with no dependencies
toward any domain. If you cannot name a boundary precisely, the boundary is usually drawn wrong.
_Mechanism: a rule that forbids a module from importing across another boundary through paths that
are not allowed, and breaks the build when it happens._

**04 · The Repo Is Legible at Every Zoom Level.** Legibility works at every level. A clean tree with
functions named `doStuff` or `data2` is legible at one level and illegible at the next. The same
discipline that names folders names functions, types, and variables.
_Mechanism: linter rules on names and complexity limits._

**05 · Capabilities Are Discoverable.** The project's tools, scripts, and commands live in
predictable places with names that say what they do (`package.json` scripts, a `scripts/` folder, a
skills folder). A capability an agent cannot find does not exist for that agent: it reimplements it.
The list of capabilities is generated from those predictable places, not written by hand.
_Mechanism: the list generated from the conventional paths, and a test that fails if a real
capability does not appear in it._

#### Bind every claim to a mechanism

**06 · Intent Becomes Mechanism.** Intent is written as a spec before the code, then turned into the
code and into the tests and rules that enforce it, and the spec is removed once its content already
lives there. What stays is the intent and its verification, not the code that satisfies it: as long
as the tests pin down the behavior, that code can be regenerated.
_Mechanism: the tests, the types, and the rules the spec was turned into._

**07 · Conventions Are Codified, Not Implicit.** A convention that lives only in people's heads is
invisible to an agent, and the agent will break it. Take it out of the culture and put it in the
tools that review the code: linter rules, type constraints, automated validations in CI that state
the rule and enforce it in the same place.
_Mechanism: the linter rules and the type constraints._

**08 · Behavior Is Verifiable, Not Asserted.** Every claim about how the system behaves (how long an
operation may take, what data must not cross a boundary, what format must not break for the people
already using it) is bound to an automated test that lives in the repository and goes red when the
behavior strays. A time limit in a document goes stale; the same limit bound to a test that fails
when it is exceeded is architecture.
_Mechanism: an automated behavior test (performance, data contract, security) that lives in the
repository and fails when the behavior deviates._

**09 · The Verification Surface Is Itself Bound.** The set of tests and rules that verify the
repository is, in turn, a set of claims, so it too is bound. An agent can rewrite the code freely,
but it cannot weaken or delete a test, a rule, or a validation to get a change through. Without a
person reviewing, this is the principle that matters most: the cheapest way to make a validation
pass is to remove it.
_Mechanism: a validation that goes red if the set of tests and rules changes without the
authorization the repository defined._

## Context Restoration: Advanced Semantic Memory Rehydration

<!-- source: wshobson/agents plugins/code-refactoring/commands/context-restore.md#advanced-context-retrieval-strategies -->

### Advanced Context Retrieval Strategies

#### 1. Semantic Vector Search

- Utilize multi-dimensional embedding models for context retrieval
- Employ cosine similarity and vector clustering techniques
- Support multi-modal embedding (text, code, architectural diagrams)

```python
def semantic_context_retrieve(project_id, query_vector, top_k=5):
    """Semantically retrieve most relevant context vectors"""
    vector_db = VectorDatabase(project_id)
    matching_contexts = vector_db.search(
        query_vector,
        similarity_threshold=0.75,
        max_results=top_k
    )
    return rank_and_filter_contexts(matching_contexts)
```

#### 2. Relevance Filtering and Ranking

- Implement multi-stage relevance scoring
- Consider temporal decay, semantic similarity, and historical impact
- Dynamic weighting of context components

```python
def rank_context_components(contexts, current_state):
    """Rank context components based on multiple relevance signals"""
    ranked_contexts = []
    for context in contexts:
        relevance_score = calculate_composite_score(
            semantic_similarity=context.semantic_score,
            temporal_relevance=context.age_factor,
            historical_impact=context.decision_weight
        )
        ranked_contexts.append((context, relevance_score))

    return sorted(ranked_contexts, key=lambda x: x[1], reverse=True)
```

#### 3. Context Rehydration Patterns

- Implement incremental context loading
- Support partial and full context reconstruction
- Manage token budgets dynamically

```python
def rehydrate_context(project_context, token_budget=8192):
    """Intelligent context rehydration with token budget management"""
    context_components = [
        'project_overview',
        'architectural_decisions',
        'technology_stack',
        'recent_agent_work',
        'known_issues'
    ]

    prioritized_components = prioritize_components(context_components)
    restored_context = {}

    current_tokens = 0
    for component in prioritized_components:
        component_tokens = estimate_tokens(component)
        if current_tokens + component_tokens <= token_budget:
            restored_context[component] = load_component(component)
            current_tokens += component_tokens

    return restored_context
```

#### 4. Session State Reconstruction

- Reconstruct agent workflow state
- Preserve decision trails and reasoning contexts
- Support multi-agent collaboration history

#### 5. Context Merging and Conflict Resolution

- Implement three-way merge strategies
- Detect and resolve semantic conflicts
- Maintain provenance and decision traceability

#### 6. Incremental Context Loading

- Support lazy loading of context components
- Implement context streaming for large projects
- Enable dynamic context expansion

#### 7. Context Validation and Integrity Checks

- Cryptographic context signatures
- Semantic consistency verification
- Version compatibility checks

#### 8. Performance Optimization

- Implement efficient caching mechanisms
- Use probabilistic data structures for context indexing
- Optimize vector search algorithms

## Context Save Tool: Intelligent Context Management Specialist

<!-- source: wshobson/agents plugins/context-management/commands/context-save.md#context-extraction-strategies -->

### Context Extraction Strategies

#### 1. Semantic Information Identification

- Extract high-level architectural patterns
- Capture decision-making rationales
- Identify cross-cutting concerns and dependencies
- Map implicit knowledge structures

#### 2. State Serialization Patterns

- Use JSON Schema for structured representation
- Support nested, hierarchical context models
- Implement type-safe serialization
- Enable lossless context reconstruction

#### 3. Multi-Session Context Management

- Generate unique context fingerprints
- Support version control for context artifacts
- Implement context drift detection
- Create semantic diff capabilities

#### 4. Context Compression Techniques

- Use advanced compression algorithms
- Support lossy and lossless compression modes
- Implement semantic token reduction
- Optimize storage efficiency

#### 5. Vector Database Integration

Supported Vector Databases:

- Pinecone
- Weaviate
- Qdrant

Integration Features:

- Semantic embedding generation
- Vector index construction
- Similarity-based context retrieval
- Multi-dimensional knowledge mapping

#### 6. Knowledge Graph Construction

- Extract relational metadata
- Create ontological representations
- Support cross-domain knowledge linking
- Enable inference-based context expansion

#### 7. Storage Format Selection

Supported Formats:

- Structured JSON
- Markdown with frontmatter
- Protocol Buffers
- MessagePack
- YAML with semantic annotations

## Mini Context Graph Skill

<!-- source: github/awesome-copilot skills/mini-context-graph/SKILL.md#design-philosophy -->

### Design Philosophy

> "The wiki is a persistent, compounding artifact. The cross-references are already there. The synthesis already reflects everything you've read." — Karpathy

| Layer | What Happens | Who Owns It |
|-------|-----------|-------------|
| **LLM Reasoning** | Extraction, synthesis, writing wiki pages | Agent (.md guidance files) |
| **Wiki Persistence** | Index, log, file I/O | `wiki_store.py` |
| **Graph Persistence** | Dedup, index, BFS traverse | `graph_store.py`, `retrieval_engine.py` |
| **Raw Source Storage** | Immutable docs + chunks + provenance | `documents_store.py` |

The human curates sources and asks questions. The LLM writes the wiki, extracts the graph, and answers with citations. Python handles all bookkeeping.
