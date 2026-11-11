# GitHub operations — derived guides

Part of `platform:github-operations`.

## GitHub Automation via Rube MCP

<!-- source: davila7/claude-code-templates cli-tool/components/skills/workflow-automation/github-automation/SKILL.md#core-workflows -->

### Core Workflows

#### 1. Create and Manage Issues

**When to use**: User wants to create, list, or manage GitHub issues

**Tool sequence**:
1. `GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER` - Find target repo if unknown [Prerequisite]
2. `GITHUB_LIST_REPOSITORY_ISSUES` - List existing issues (includes PRs) [Required]
3. `GITHUB_CREATE_AN_ISSUE` - Create a new issue [Required]
4. `GITHUB_CREATE_AN_ISSUE_COMMENT` - Add comments to an issue [Optional]
5. `GITHUB_SEARCH_ISSUES_AND_PULL_REQUESTS` - Search across repos by keyword [Optional]

**Key parameters**:
- `owner`: Repository owner (username or org), case-insensitive
- `repo`: Repository name without .git extension
- `title`: Issue title (required for creation)
- `body`: Issue description (supports Markdown)
- `labels`: Array of label names
- `assignees`: Array of GitHub usernames
- `state`: 'open', 'closed', or 'all' for filtering

**Pitfalls**:
- `GITHUB_LIST_REPOSITORY_ISSUES` returns both issues AND pull requests; check `pull_request` field to distinguish
- Only users with push access can set assignees, labels, and milestones; they are silently dropped otherwise
- Pagination: `per_page` max 100; iterate pages until empty

#### 2. Manage Pull Requests

**When to use**: User wants to create, review, or merge pull requests

**Tool sequence**:
1. `GITHUB_FIND_PULL_REQUESTS` - Search and filter PRs [Required]
2. `GITHUB_GET_A_PULL_REQUEST` - Get detailed PR info including mergeable status [Required]
3. `GITHUB_LIST_PULL_REQUESTS_FILES` - Review changed files [Optional]
4. `GITHUB_CREATE_A_PULL_REQUEST` - Create a new PR [Required]
5. `GITHUB_CREATE_AN_ISSUE_COMMENT` - Post review comments [Optional]
6. `GITHUB_LIST_CHECK_RUNS_FOR_A_REF` - Verify CI status before merge [Optional]
7. `GITHUB_MERGE_A_PULL_REQUEST` - Merge after explicit user approval [Required]

**Key parameters**:
- `head`: Source branch with changes (must exist; for cross-repo: 'username:branch')
- `base`: Target branch to merge into (e.g., 'main')
- `title`: PR title (required unless `issue` number provided)
- `merge_method`: 'merge', 'squash', or 'rebase'
- `state`: 'open', 'closed', or 'all'

**Pitfalls**:
- `GITHUB_CREATE_A_PULL_REQUEST` fails with 422 if base/head are invalid, identical, or already merged
- `GITHUB_MERGE_A_PULL_REQUEST` can be rejected if PR is draft, closed, or branch protection applies
- Always verify mergeable status with `GITHUB_GET_A_PULL_REQUEST` immediately before merging
- Require explicit user confirmation before calling MERGE

#### 3. Manage Repositories and Branches

**When to use**: User wants to create repos, manage branches, or update repo settings

**Tool sequence**:
1. `GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER` - List user's repos [Required]
2. `GITHUB_GET_A_REPOSITORY` - Get detailed repo info [Optional]
3. `GITHUB_CREATE_A_REPOSITORY_FOR_THE_AUTHENTICATED_USER` - Create personal repo [Required]
4. `GITHUB_CREATE_AN_ORGANIZATION_REPOSITORY` - Create org repo [Alternative]
5. `GITHUB_LIST_BRANCHES` - List branches [Required]
6. `GITHUB_CREATE_A_REFERENCE` - Create new branch from SHA [Required]
7. `GITHUB_UPDATE_A_REPOSITORY` - Update repo settings [Optional]

**Key parameters**:
- `name`: Repository name
- `private`: Boolean for visibility
- `ref`: Full reference path (e.g., 'refs/heads/new-branch')
- `sha`: Commit SHA to point the new reference to
- `default_branch`: Default branch name

**Pitfalls**:
- `GITHUB_CREATE_A_REFERENCE` only creates NEW references; use `GITHUB_UPDATE_A_REFERENCE` for existing ones
- `ref` must start with 'refs/' and contain at least two slashes
- `GITHUB_LIST_BRANCHES` paginates via `page`/`per_page`; iterate until empty page
- `GITHUB_DELETE_A_REPOSITORY` is permanent and irreversible; requires admin privileges

#### 4. Search Code and Commits

**When to use**: User wants to find code, files, or commits across repositories

**Tool sequence**:
1. `GITHUB_SEARCH_CODE` - Search file contents and paths [Required]
2. `GITHUB_SEARCH_CODE_ALL_PAGES` - Multi-page code search [Alternative]
3. `GITHUB_SEARCH_COMMITS_BY_AUTHOR` - Search commits by author/date/org [Required]
4. `GITHUB_LIST_COMMITS` - List commits for a specific repo [Alternative]
5. `GITHUB_GET_A_COMMIT` - Get detailed commit info [Optional]
6. `GITHUB_GET_REPOSITORY_CONTENT` - Get file content [Optional]

**Key parameters**:
- `q`: Search query with qualifiers (`language:python`, `repo:owner/repo`, `extension:js`)
- `owner`/`repo`: For repo-specific commit listing
- `author`: Filter by commit author
- `since`/`until`: ISO 8601 date range for commits

**Pitfalls**:
- Code search only indexes files under 384KB on default branch
- Maximum 1000 results returned from code search
- `GITHUB_SEARCH_COMMITS_BY_AUTHOR` requires keywords in addition to qualifiers; qualifier-only queries are not allowed
- `GITHUB_LIST_COMMITS` returns 409 on empty repos

#### 5. Manage CI/CD and Deployments

**When to use**: User wants to view workflows, check CI status, or manage deployments

**Tool sequence**:
1. `GITHUB_LIST_REPOSITORY_WORKFLOWS` - List GitHub Actions workflows [Required]
2. `GITHUB_GET_A_WORKFLOW` - Get workflow details by ID or filename [Optional]
3. `GITHUB_CREATE_A_WORKFLOW_DISPATCH_EVENT` - Manually trigger a workflow [Required]
4. `GITHUB_LIST_CHECK_RUNS_FOR_A_REF` - Check CI status for a commit/branch [Required]
5. `GITHUB_LIST_DEPLOYMENTS` - List deployments [Optional]
6. `GITHUB_GET_A_DEPLOYMENT_STATUS` - Get deployment status [Optional]

**Key parameters**:
- `workflow_id`: Numeric ID or filename (e.g., 'ci.yml')
- `ref`: Git reference (branch/tag) for workflow dispatch
- `inputs`: JSON string of workflow inputs matching `on.workflow_dispatch.inputs`
- `environment`: Filter deployments by environment name

**Pitfalls**:
- `GITHUB_CREATE_A_WORKFLOW_DISPATCH_EVENT` requires the workflow to have `workflow_dispatch` trigger configured
- Full path `.github/workflows/main.yml` is auto-stripped to just `main.yml`
- Inputs max 10 key-value pairs; must match workflow's `on.workflow_dispatch.inputs` definitions

#### 6. Manage Users and Permissions

**When to use**: User wants to check collaborators, permissions, or branch protection

**Tool sequence**:
1. `GITHUB_LIST_REPOSITORY_COLLABORATORS` - List repo collaborators [Required]
2. `GITHUB_GET_REPOSITORY_PERMISSIONS_FOR_A_USER` - Check specific user's access [Optional]
3. `GITHUB_GET_BRANCH_PROTECTION` - Inspect branch protection rules [Required]
4. `GITHUB_UPDATE_BRANCH_PROTECTION` - Update protection settings [Optional]
5. `GITHUB_ADD_A_REPOSITORY_COLLABORATOR` - Add/update collaborator [Optional]

**Key parameters**:
- `affiliation`: 'outside', 'direct', or 'all' for collaborator filtering
- `permission`: Filter by 'pull', 'triage', 'push', 'maintain', 'admin'
- `branch`: Branch name for protection rules
- `enforce_admins`: Whether protection applies to admins

**Pitfalls**:
- `GITHUB_GET_BRANCH_PROTECTION` returns 404 for unprotected branches; treat as no protection rules
- Determine push ability from `permissions.push` or `role_name`, not display labels
- `GITHUB_LIST_REPOSITORY_COLLABORATORS` paginates; iterate all pages
- `GITHUB_GET_REPOSITORY_PERMISSIONS_FOR_A_USER` may be inconclusive for non-collaborators

## GitHub Repo Standardizer

<!-- source: github/awesome-copilot skills/repo-standardizer/SKILL.md#preflight-mandatory-in-order -->

### Preflight (mandatory, in order)

> **Requires**: `gh` CLI (authenticated), `git`, `jq`, `python3` — verify
> they exist before starting (`which gh git jq python3`).

#### 1. Authenticate — check gh login first

```bash
gh auth status 2>/dev/null || echo "NOT_LOGGED_IN"
```

- **Logged in** → continue; print `gh api user -q .login` so the user knows which account will act.
- **Not logged in** → STOP. Tell the user (do not guess):
  1. Run `gh auth login` (web/device flow), **or**
  2. Export a token: `export GH_TOKEN=ghp_xxx` — needs `repo`, `workflow` (for CI files) and, for org repos, `admin:org` (or `admin:repo_hook` / org membership admin) scopes.
  - Never paste tokens into chat, logs, or files. If the user pastes a token in chat, advise them to revoke it and re-issue.
  - If `gh auth login` is impossible in this environment (headless), suggest `gh auth login --with-token` reading from a file the user created.

Verify the acting account can write to the target:

```bash
# user repos: no extra check needed beyond token scopes
# org repos: must be a member/admin of the org
gh api "orgs/ORG/memberships/$(gh api user -q .login)" -q .role 2>/dev/null || echo "NO_ORG_ACCESS"
```

- `admin`/`member` → OK. `404` → stop and ask the user to add the account to the org first.

#### 2. Detect repository type

```bash
gh repo view OWNER/REPO --json name,owner,visibility,defaultBranchRef,isArchived,isFork \
  -q '{name:.name, ownerType:.owner.type, visibility:.visibility, defaultBranch:.defaultBranchRef.name, archived:.isArchived, fork:.isFork}'
```

| Field | Meaning | Consequence |
|---|---|---|
| `ownerType` | `User` = personal, `Organization` = org | Org repos can also use org-level rulesets; both support repo-level rulesets |
| `visibility` | `PUBLIC` / `PRIVATE` / `INTERNAL` | Private: skip public-facing docs pressure, keep CI secrets minimal; public: README badges + CONTRIBUTING/SECURITY matter |
| `archived` / `fork` | Read-only / fork | **Skip write modules**; report why |

If the repo was not explicitly named by the user, confirm before touching an
org or private repository.

#### 3. Audit current state

```bash
gh label list --repo OWNER/REPO --limit 200
gh api repos/OWNER/REPO/contents/.github -q '.[].path' 2>/dev/null || echo "no .github dir"
gh api repos/OWNER/REPO/contents/.github/workflows -q '.[].name' 2>/dev/null || echo "no workflows"
gh api repos/OWNER/REPO/rulesets -q '.[] | {name:.name, enforcement:.enforcement}' 2>/dev/null || echo "no rulesets"
gh api repos/OWNER/REPO/branches -q '.[].name' 2>/dev/null
for f in README.md CONTRIBUTING.md SECURITY.md LICENSE .gitignore; do
  gh api "repos/OWNER/REPO/contents/$f" -q .name 2>/dev/null || echo "missing: $f"
done
```

#### 4. Detect test framework (for CI module)

Check for these signals (first match wins):

```bash
gh api repos/OWNER/REPO/contents/package.json -q .name 2>/dev/null   # node → templates/ci-node.yml
gh api repos/OWNER/REPO/contents/pyproject.toml -q .name 2>/dev/null # python → templates/ci-python.yml
gh api repos/OWNER/REPO/contents/go.mod -q .name 2>/dev/null         # go → templates/ci-go.yml
gh api repos/OWNER/REPO/contents/Cargo.toml -q .name 2>/dev/null     # rust → templates/ci-rust.yml
```

No signal → propose the generic CI (or ask the user whether CI is wanted at all).

#### 5. Ask about language (before planning)

- Ask the user which language `CONTRIBUTING.md` and the PR template should be
  written in (default: English, or the project's primary language for local
  projects). Translate the templates accordingly when generating — never
  assume a language.
- (README languages are asked separately in Module F.)

#### 6. Ask about automation (decides the Governance labels)

Ask the user whether the repo has any **automation bots or AI writers**
running on it — e.g. dependabot, a Stale bot, ClawSweeper, or an AI coding
agent that auto-files PRs / auto-fixes issues.

- **Why ask**: `r:*` / `clawsweeper:*` / `triage:*` / `close:*` labels are
  **signal labels, not categories** — a bot reads them and acts (auto-close,
  auto-lock, auto-fix, auto-merge). Without running automation those labels
  are dead weight, so the answer decides whether the Governance dimension is
  added at all (Module A, Step 2).
- **Yes** → plan the `Governance / auto-close rules` dimension (add only the
  `r:*` rules matching the project's real reject criteria).
- **No** → skip that dimension entirely — never add `r:*` / bot labels to a
  repo with no automation.
