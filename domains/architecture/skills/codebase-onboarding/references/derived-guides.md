# Codebase onboarding — derived guides

Part of `architecture:codebase-onboarding`.

## Create high‑quality AGENTS.md file

<!-- source: github/awesome-copilot skills/create-agentsmd/SKILL.md#file-structure-and-content-guidelines -->

### File Structure and Content Guidelines

#### 1. Required Setup

- Create the file as `AGENTS.md` in the repository root
- Use standard Markdown formatting
- No required fields - flexible structure based on project needs

#### 2. Essential Sections to Include

##### Project Overview

- Brief description of what the project does
- Architecture overview if complex
- Key technologies and frameworks used

##### Setup Commands

- Installation instructions
- Environment setup steps
- Dependency management commands
- Database setup if applicable

##### Development Workflow

- How to start development server
- Build commands
- Watch/hot-reload setup
- Package manager specifics (npm, pnpm, yarn, etc.)

##### Testing Instructions

- How to run tests (unit, integration, e2e)
- Test file locations and naming conventions
- Coverage requirements
- Specific test patterns or frameworks used
- How to run subset of tests or focus on specific areas

##### Code Style Guidelines

- Language-specific conventions
- Linting and formatting rules
- File organization patterns
- Naming conventions
- Import/export patterns

##### Build and Deployment

- Build commands and outputs
- Environment configurations
- Deployment steps and requirements
- CI/CD pipeline information

#### 3. Optional but Recommended Sections

##### Security Considerations

- Security testing requirements
- Secrets management
- Authentication patterns
- Permission models

##### Monorepo Instructions (if applicable)

- How to work with multiple packages
- Cross-package dependencies
- Selective building/testing
- Package-specific commands

##### Pull Request Guidelines

- Title format requirements
- Required checks before submission
- Review process
- Commit message conventions

##### Debugging and Troubleshooting

- Common issues and solutions
- Logging patterns
- Debug configuration
- Performance considerations

## Acquire Codebase Knowledge

<!-- source: github/awesome-copilot skills/acquire-codebase-knowledge/SKILL.md#gotchas -->

### Gotchas

**Monorepos:** Root `package.json` may have no source — check for `workspaces`, `packages/`, or `apps/` directories. Each workspace may have independent dependencies and conventions. Map each sub-package separately.

**Outdated README:** README often describes intended architecture, not the current one. Cross-reference with actual file structure before treating any README claim as fact.

**TypeScript path aliases:** `tsconfig.json` `paths` config means imports like `@/foo` don't map directly to the filesystem. Map aliases to real paths before documenting structure.

**Generated/compiled output:** Never document patterns from `dist/`, `build/`, `generated/`, `.next/`, `out/`, or `__pycache__/`. These are artefacts — document source conventions only.

**`.env.example` reveals required config:** Secrets are never committed. Read `.env.example`, `.env.template`, or `.env.sample` to discover required environment variables.

**`devDependencies` ≠ production stack:** Only `dependencies` (or equivalent, e.g. `[tool.poetry.dependencies]`) runs in production. Document linters, formatters, and test frameworks separately as dev tooling.

**Test TODOs ≠ production debt:** TODOs inside `test/`, `tests/`, `__tests__/`, or `spec/` are coverage gaps, not production technical debt. Separate them in `CONCERNS.md`.

**High-churn files = fragile areas:** Files appearing most in recent git history have the highest modification rate and likely hidden complexity. Always note them in `CONCERNS.md`.

---
