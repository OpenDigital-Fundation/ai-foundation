# Git workflow — derived guides

Part of `platform:git-workflow`.

## git-flow-branch-creator

<!-- source: github/awesome-copilot skills/git-flow-branch-creator/SKILL.md#git-flow-branch-analysis-framework -->

#### Git Flow Branch Analysis Framework

```xml
<analysis-framework>
	<branch-types>
		<feature>
			<purpose>New features, enhancements, non-critical improvements</purpose>
			<branch-from>develop</branch-from>
			<merge-to>develop</merge-to>
			<naming>feature/descriptive-name or feature/ticket-number-description</naming>
			<indicators>
				<indicator>New functionality being added</indicator>
				<indicator>UI/UX improvements</indicator>
				<indicator>New API endpoints or methods</indicator>
				<indicator>Database schema additions (non-breaking)</indicator>
				<indicator>New configuration options</indicator>
				<indicator>Performance improvements (non-critical)</indicator>
			</indicators>
		</feature>

		<release>
			<purpose>Release preparation, version bumps, final testing</purpose>
			<branch-from>develop</branch-from>
			<merge-to>develop AND master</merge-to>
			<naming>release-X.Y.Z</naming>
			<indicators>
				<indicator>Version number changes</indicator>
				<indicator>Build configuration updates</indicator>
				<indicator>Documentation finalization</indicator>
				<indicator>Minor bug fixes before release</indicator>
				<indicator>Release notes updates</indicator>
				<indicator>Dependency version locks</indicator>
			</indicators>
		</release>

		<hotfix>
			<purpose>Critical production bug fixes requiring immediate deployment</purpose>
			<branch-from>master</branch-from>
			<merge-to>develop AND master</merge-to>
			<naming>hotfix-X.Y.Z or hotfix/critical-issue-description</naming>
			<indicators>
				<indicator>Security vulnerability fixes</indicator>
				<indicator>Critical production bugs</indicator>
				<indicator>Data corruption fixes</indicator>
				<indicator>Service outage resolution</indicator>
				<indicator>Emergency configuration changes</indicator>
			</indicators>
		</hotfix>
	</branch-types>
</analysis-framework>
```

## Commit work

<!-- source: davila7/claude-code-templates cli-tool/components/skills/productivity/commit-work/SKILL.md#workflow-checklist -->

### Workflow (checklist)
1) Inspect the working tree before staging
   - `git status`
   - `git diff` (unstaged)
   - If many changes: `git diff --stat`
2) Decide commit boundaries (split if needed)
   - Split by: feature vs refactor, backend vs frontend, formatting vs logic, tests vs prod code, dependency bumps vs behavior changes.
   - If changes are mixed in one file, plan to use patch staging.
3) Stage only what belongs in the next commit
   - Prefer patch staging for mixed changes: `git add -p`
   - To unstage a hunk/file: `git restore --staged -p` or `git restore --staged <path>`
4) Review what will actually be committed
   - `git diff --cached`
   - Sanity checks:
     - no secrets or tokens
     - no accidental debug logging
     - no unrelated formatting churn
5) Describe the staged change in 1-2 sentences (before writing the message)
   - "What changed?" + "Why?"
   - If you cannot describe it cleanly, the commit is probably too big or mixed; go back to step 2.
6) Write the commit message
   - Use Conventional Commits (required):
     - `type(scope): short summary`
     - blank line
     - body (what/why, not implementation diary)
     - footer (BREAKING CHANGE) if needed
   - Prefer an editor for multi-line messages: `git commit -v`
   - Use `references/commit-message-template.md` if helpful.
7) Run the smallest relevant verification
   - Run the repo's fastest meaningful check (unit tests, lint, or build) before moving on.
8) Repeat for the next commit until the working tree is clean

## Git Bisect Helper & Automation

<!-- source: davila7/claude-code-templates cli-tool/components/commands/git-workflow/git-bisect-helper.md#bisect-modes -->

### Bisect Modes

#### Automatic Bisect (`--auto [test-command]`)
```bash
# Automatically bisect using test command
/git-bisect-helper --auto "npm test"
/git-bisect-helper --auto "python -m pytest tests/test_regression.py"
/git-bisect-helper --auto "./scripts/check-performance.sh"
```

**Process:**
1. Run test command at each bisect point
2. Mark commit as good (exit code 0) or bad (non-zero)
3. Continue until regression commit is found
4. Provide detailed report of findings

#### Manual Guided Bisect
```bash
# Interactive bisect with guidance
/git-bisect-helper v1.2.0 HEAD
/git-bisect-helper abc123 def456
```

**Process:**
1. Show current commit details and changes
2. Provide testing suggestions
3. Wait for user input (good/bad)
4. Continue to next bisect point
5. Offer insights about current commit

#### Continue Existing Session (`--continue`)
```bash
# Resume interrupted bisect session
/git-bisect-helper --continue
```

**Process:**
1. Analyze current bisect state
2. Show progress and remaining steps
3. Continue with appropriate mode
4. Provide context from previous steps

#### Reset Session (`--reset`)
```bash
# Clean up and reset bisect session
/git-bisect-helper --reset
```

**Process:**
1. End current bisect session
2. Return to original branch
3. Clean up temporary files
4. Provide session summary

## Git Commit with Conventional Commits

<!-- source: github/awesome-copilot skills/git-commit/SKILL.md#types -->

### Types

Conventional Commits defines only `feat` and `fix`. The other types come from the Angular convention ([`@commitlint/config-conventional`](https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional)). If the repository has its own list, use that list.

| Type       | Use it for                                     |
| ---------- | ---------------------------------------------- |
| `feat`     | A new feature                                  |
| `fix`      | A bug fix                                      |
| `docs`     | Documentation only                             |
| `style`    | Formatting only, with no change to the logic   |
| `refactor` | A code change that is not a feature or a fix   |
| `perf`     | A performance improvement                      |
| `test`     | New or changed tests                           |
| `build`    | The build system or the dependencies           |
| `ci`       | The CI configuration                           |
| `chore`    | Other maintenance                              |
| `revert`   | A revert of an earlier commit                  |
