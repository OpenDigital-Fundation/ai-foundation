# Debt ledger — dependency updater

Part of `code-quality:debt-ledger`. Adapted reference material; the owner procedure, project conventions, scope and authorization rules take precedence. Examples are not automatically executed.

<!-- source: davila7/claude-code-templates cli-tool/components/skills/development/dependency-updater/SKILL.md#commands-by-language -->

## Dependency inventory by ecosystem

This owner reports debt; it does not upgrade dependencies. Use the repository's existing tools to collect outdated/vulnerable dependency evidence, including resolved versions and manifests. Example read-only inventory commands, only when those toolchains are already installed:

```text
npm outdated
pip list --outdated
go list -m -u all
bundle outdated
dotnet list package --outdated
dotnet list package --vulnerable
```

Registry/network queries may reveal package names: confirm the allowed destination for private projects. Do not install a missing helper, globally install tooling, run automatic audit fixes or update all packages as part of this inventory. Report tool failure as incomplete evidence, not a clean dependency set.

For each finding record package, installed/available versions, affected capability, source of advisory or breaking change, and a verification plan for a separately authorized upgrade.
