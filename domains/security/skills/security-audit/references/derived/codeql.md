# Security audit — codeql

Part of `security:security-audit`. Adapted reference material; the owner procedure, project conventions, scope and authorization rules take precedence. Examples are not automatically executed.

## CodeQL Code Scanning

<!-- source: github/awesome-copilot skills/codeql/SKILL.md#core-workflow-github-actions -->

### Core Workflow — GitHub Actions

#### Step 1: Choose Setup Type

- **Default setup** — Enable from repository Settings → Advanced Security → CodeQL analysis. Best for getting started quickly. Uses `none` build mode for most languages.
- **Advanced setup** — Create a `.github/workflows/codeql.yml` file for full control over triggers, build modes, query suites, and matrix strategies.

To switch from default to advanced: disable default setup first, then commit the workflow file.

#### Step 2: Configure Workflow Triggers

Define when scanning runs:

```yaml
on:
  push:
    branches: [main, protected]
  pull_request:
    branches: [main]
  schedule:
    - cron: '30 6 * * 1'  # Weekly Monday 6:30 UTC
```

- `push` — scans on every push to specified branches; results appear in Security tab
- `pull_request` — scans PR merge commits; results appear as PR check annotations
- `schedule` — periodic scans of the default branch (cron must exist on default branch)
- `merge_group` — add if repository uses merge queues

To skip scans for documentation-only PRs:

```yaml
on:
  pull_request:
    paths-ignore:
      - '**/*.md'
      - '**/*.txt'
```

> `paths-ignore` controls whether the workflow runs, not which files are analyzed.

#### Step 3: Configure Permissions

Set least-privilege permissions:

```yaml
permissions:
  security-events: write   # Required to upload SARIF results
  contents: read            # Required to checkout code
  actions: read             # Required for private repos using codeql-action
```

#### Step 4: Configure Language Matrix

Use a matrix strategy to analyze each language in parallel:

```yaml
jobs:
  analyze:
    name: Analyze (${{ matrix.language }})
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        include:
          - language: javascript-typescript
            build-mode: none
          - language: python
            build-mode: none
```

For compiled languages, set the appropriate `build-mode`:
- `none` — no build required (supported for C/C++, C#, Java, Rust)
- `autobuild` — automatic build detection
- `manual` — custom build commands (advanced setup only)

> For detailed per-language autobuild behavior and runner requirements, search `references/compiled-languages.md`.

#### Step 5: Configure CodeQL Init and Analysis

```yaml
steps:
  - name: Checkout repository
    uses: actions/checkout@v4

  - name: Initialize CodeQL
    uses: github/codeql-action/init@v4
    with:
      languages: ${{ matrix.language }}
      build-mode: ${{ matrix.build-mode }}
      queries: security-extended
      dependency-caching: true

  - name: Perform CodeQL Analysis
    uses: github/codeql-action/analyze@v4
    with:
      category: "/language:${{ matrix.language }}"
```

**Query suite options:**
- `security-extended` — default security queries plus additional coverage
- `security-and-quality` — security plus code quality queries
- Custom query packs via `packs:` input (e.g., `codeql/javascript-queries:AlertSuppression.ql`)

**Dependency caching:** Set `dependency-caching: true` on the `init` action to cache restored dependencies across runs.

**Analysis category:** Use `category` to distinguish SARIF results in monorepos (e.g., per-language, per-component).

#### Step 6: Monorepo Configuration

For monorepos with multiple components, use the `category` parameter to separate SARIF results:

```yaml
category: "/language:${{ matrix.language }}/component:frontend"
```

To restrict analysis to specific directories, use a CodeQL configuration file (`.github/codeql/codeql-config.yml`):

```yaml
paths:
  - apps/
  - services/
paths-ignore:
  - node_modules/
  - '**/test/**'
```

Reference it in the workflow:

```yaml
- uses: github/codeql-action/init@v4
  with:
    config-file: .github/codeql/codeql-config.yml
```

#### Step 7: Manual Build Steps (Compiled Languages)

If `autobuild` fails or custom build commands are needed:

```yaml
- language: c-cpp
  build-mode: manual
```

Then add explicit build steps between `init` and `analyze`:

```yaml
- if: matrix.build-mode == 'manual'
  name: Build
  run: |
    make bootstrap
    make release
```
