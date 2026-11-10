# Database migrations — derived guides

Part of `data:database-migrations`.

## Creating Integration Tests for Oracle-to-PostgreSQL Migration

<!-- source: github/awesome-copilot skills/creating-oracle-to-postgres-migration-integration-tests/SKILL.md#key-constraints -->

### Key Constraints

- **Phase 3 only** — these tests target Oracle. Do not invoke this skill during Phase 6 or against a PostgreSQL-targeting project.
- **Oracle is the golden source** — tests capture Oracle's expected behavior.
- **Assertion portability** — avoid platform-specific error messages or syntax in assertions so that when the test project is migrated to PostgreSQL in Phase 6, assertions require no changes.
- **Seed only against Oracle** — the test project will be migrated to PostgreSQL in Phase 6; seed data and infrastructure stay Oracle-targeted until then.
- **Scoped to one project** — do not create tests for artifacts outside the target project.
- **Preserve existing data** — never rewrite or wipe pre-existing business or lookup rows.
