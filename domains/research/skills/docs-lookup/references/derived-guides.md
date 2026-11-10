# Documentation lookup — derived guides

Part of `research:docs-lookup`.

## Context7 Documentation Expert

<!-- source: github/awesome-copilot agents/context7.agent.md#quality-standards,documentation-retrieval-strategy -->

### Documentation Retrieval Strategy

#### Topic Specification 🎨

Be specific with the `topic` parameter to get relevant documentation:

**Good Topics**:
- "middleware" (not "how to use middleware")
- "hooks" (not "react hooks")
- "routing" (not "how to set up routes")
- "authentication" (not "how to authenticate users")

**Topic Examples by Library**:
- **Next.js**: routing, middleware, api-routes, server-components, image-optimization
- **React**: hooks, context, suspense, error-boundaries, refs
- **Tailwind**: responsive-design, dark-mode, customization, utilities
- **Express**: middleware, routing, error-handling
- **TypeScript**: types, generics, modules, decorators

#### Token Management 💰

Adjust `tokens` parameter based on complexity:
- **Simple queries** (syntax check): 2000-3000 tokens
- **Standard features** (how to use): 5000 tokens (default)
- **Complex integration** (architecture): 7000-10000 tokens

More tokens = more context but higher cost. Balance appropriately.

---

### Quality Standards

#### ✅ Every Response Should:
- **Use verified APIs**: No hallucinated methods or properties
- **Include working examples**: Based on actual documentation
- **Reference versions**: "In Next.js 14..." not "In Next.js..."
- **Follow current patterns**: Not outdated or deprecated approaches
- **Cite sources**: "According to the [library] docs..."

#### ⚠️ Quality Gates:
- Did you fetch documentation before answering?
- Did you read package.json to check current version?
- Did you determine the latest available version?
- Did you inform user about upgrade availability (YES/NO)?
- Does your code use only APIs present in the docs?
- Are you recommending current best practices?
- Did you check for deprecations or warnings?
- Is the version specified or clearly latest?
- If upgrade exists, did you provide migration guidance?

#### 🚫 Never Do:
- ❌ **Guess API signatures** - Always verify with Context7
- ❌ **Use outdated patterns** - Check docs for current recommendations
- ❌ **Ignore versions** - Version matters for accuracy
- ❌ **Skip version checking** - ALWAYS check package.json and inform about upgrades
- ❌ **Hide upgrade info** - Always tell users if newer versions exist
- ❌ **Skip library resolution** - Always resolve before fetching docs
- ❌ **Hallucinate features** - If docs don't mention it, it may not exist
- ❌ **Provide generic answers** - Be specific to the library version

---
