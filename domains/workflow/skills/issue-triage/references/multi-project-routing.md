# Heuristic triage and routing across GitHub Projects

Part of workflow:issue-triage: a classification engine and routing scheme for organisations that keep one portfolio board plus several domain boards (GitHub Projects v2). Replace every `<placeholder>` with the organisation's own values, kept in the repository's `AGENTS.md` or a routing file.

## Board layout

- **Portfolio board** (`<PORTFOLIO_PROJECT_ID>`): holds 100% of the organisation's items, for executive visibility, billing and global deadlines.
- **Domain boards** (`<DOMAIN_PROJECT_ID>` per product area): each item also lives on the board of its product area.
- A **routing matrix** maps each repository to its boards, product and default team:

| Repository | Boards | Product | Default team |
|---|---|---|---|
| `<org>/<repo>` | portfolio, `<domain board>` | `<product>` | `<team>` |

## Triage steps

1. **Read the item:** `gh issue view <N> --repo <org>/<repo> --json id,number,title,body,labels,assignees,state`.
2. **Extract signals:** title prefix (`feat:`, `fix:`, `chore:`, `docs:`, `[P0]`...), body length, checklists (`- [ ]`), explicit complexity, blockers and links (`closes #123`, "blocked by"), labels, assignees.
3. **Classify** with the rules below; run any automation in dry-run first and apply only after review.
4. **Route:** add the item to the portfolio board and to its domain board; set the fields.

## Classification rules

**Team (functional area)** — inferred from the content: product (discovery, rules, requirements, specs), infrastructure (CI/CD, containers, cloud, security, CVEs), data (databases, ETL, SQL, metrics), front end (UI frameworks, forms, screens, accessibility), back end (APIs, services, integrations).

**Product** — from the repository via the routing matrix, or an explicit label.

**Delivery type** — from the Conventional Commits prefix or a `type:*` label: feat, fix, bug, test, chore, docs, refactor, perf, ci, hotfix, style, ops.

**Priority**
- **P0 (critical):** blocking production failure, critical exploitable vulnerability, immediate legal deadline.
- **P1 (high):** serious bug without an easy workaround; priority deliveries of the active sprint.
- **P2 (medium):** regular evolution, incremental improvements.
- **P3 (low):** cosmetic adjustments, small refactors, non-urgent debt.
- **None:** not prioritised yet.

**Estimate**

| Size | Hours | Rule of thumb |
|:---:|:---:|---|
| XS | 2 | Docs, typo, small text or CSS change |
| S | 4 | Small bug fix, isolated test, one or two tasks |
| M | 8 | Standard feature with clear scope, three to five tasks |
| L | 16 | Cross-layer integration (front and back end), six to nine tasks |
| XL | 24 | Intermediate epic or module, ten to fourteen tasks |
| XXL | 40 | New module, cross-cutting architecture, legacy migration, fifteen or more tasks |

**Refinement status**
- **Initial idea:** description under ~80 characters.
- **Planning pending:** dense description (over ~400 characters) without tasks or acceptance criteria.
- **Review needed:** scope or technical dependencies need review.
- **Ready:** clear checklist and acceptance criteria or definition of done.

## Icebox versus sprint

Items that should not crowd immediate execution live in an **icebox** status. An item leaves the icebox for the sprint backlog only if it meets the **Definition of Ready**:

1. Refinement status is Ready.
2. At least one structured checklist in the body.
3. Priority P0 or P1, or included in the active sprint milestone.
4. At least one assignee and a team set.
5. Estimate and hours filled in.
6. No blocker and no external impediment.

## GitHub Projects v2 recipes

```bash
# Items and fields of a project
gh api graphql -f query='query { node(id: "<PROJECT_ID>") { ... on ProjectV2 { title
  items(first: 20) { nodes { id content { ... on Issue { number title repository { nameWithOwner } } } } } } } }'

# Add an issue to a project
gh api graphql -f query='mutation { addProjectV2ItemById(input: {projectId: "<PROJECT_ID>", contentId: "<ISSUE_NODE_ID>"}) { item { id } } }'

# Set a single-select field (status, priority, size)
gh api graphql -f query='mutation { updateProjectV2ItemFieldValue(input: {projectId: "<PROJECT_ID>", itemId: "<ITEM_ID>",
  fieldId: "<FIELD_ID>", value: {singleSelectOptionId: "<OPTION_ID>"}}) { projectV2Item { id } } }'
```

Field and option IDs come from the project schema (`gh project field-list <number> --owner <org> --format json`); keep them in a versioned schema file instead of hard-coding them in scripts. Writing to boards changes shared state: run in dry-run, show the planned changes, then apply.
