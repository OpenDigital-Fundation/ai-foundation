# Stacked pull requests

Part of platform:git-workflow. A stack decomposes a large change into a chain of small, reviewable pull requests where each branch is created from the previous one:

```text
main ──► PR 1: feat(db): schema and migrations ──► PR 2: feat(api): routes and services ──► PR 3: feat(ui): screens
```

## When to stack

Use a stack when a feature spans several layers (schema → API → state → UI), the total change exceeds ~300–400 lines or several modules, a refactor must land before a new rule, the front end must start while the back end is in review, or different specialists must approve different parts.

Do not stack a simple fix (one atomic PR is enough) or independent changes (open parallel PRs against `main` instead).

## Build the stack

```bash
git switch main && git pull --ff-only
git switch -c feat/booking-db
# ...change, commit (Conventional Commits)
git push -u origin feat/booking-db
gh pr create --base main --head feat/booking-db --title "feat(db): booking schema and migrations [1/3]" --body "Part 1 of 3 of the booking stack."

git switch -c feat/booking-api            # from feat/booking-db
# ...change, commit
git push -u origin feat/booking-api
gh pr create --base feat/booking-db --head feat/booking-api --title "feat(api): booking routes and services [2/3]" --body "Part 2 of 3. Depends on #<PR1>."

git switch -c feat/booking-ui             # from feat/booking-api
# ...change, commit
git push -u origin feat/booking-ui
gh pr create --base feat/booking-api --head feat/booking-ui --title "feat(ui): booking screens [3/3]" --body "Part 3 of 3. Depends on #<PR2>."
```

Name each PR with its position (`[n/total]`) and link the one it depends on.

## Review and merge

- Review from the bottom up: each PR shows only its own diff.
- Merge the base PR first. When the platform supports native stacks, the next PR is retargeted and rebased automatically; otherwise retarget it to `main` (`gh pr edit <N> --base main`) and rebase it onto the updated `main`.
- After a change in a lower PR, rebase the PRs above it (`git rebase --update-refs` keeps every branch of the stack in place); force-pushing a shared branch needs agreement from whoever else uses it.
- Keep every PR green and deployable on its own; if one cannot be, mark the stack's integration point clearly.
