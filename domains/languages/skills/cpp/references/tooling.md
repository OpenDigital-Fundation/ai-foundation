# C++ — Tooling

Part of `languages:cpp`. Load when formatters, linters, type checkers and editor hooks.

## C++ Hooks

<!-- source: affaan-m/ECC rules/cpp/hooks.md -->

> This file extends common/hooks.md with C++ specific content.

### Build Hooks

Run these checks before committing C++ changes:

```bash
# Format check
clang-format --dry-run --Werror src/*.cpp src/*.hpp

# Static analysis
clang-tidy src/*.cpp -- -std=c++17

# Build
cmake --build build

# Tests
ctest --test-dir build --output-on-failure
```

### Recommended CI Pipeline

1. **clang-format** — formatting check
2. **clang-tidy** — static analysis
3. **cppcheck** — additional analysis
4. **cmake build** — compilation
5. **ctest** — test execution with sanitizers

## vcpkg

<!-- source: github/awesome-copilot skills/vcpkg/SKILL.md#version-management -->

### Version Management

#### Setting Versions for Individual Dependencies

Prefer `"version>="` for minimum-version constraints:
```json
{
  "dependencies": [{ "name": "fmt", "version>=": "10.2.0" }],
  "builtin-baseline": "<commit-sha>"
}
```

Use `overrides` only when a hard pin is required:
```json
{
  "dependencies": ["fmt"],
  "overrides": [{ "name": "fmt", "version": "10.2.0" }],
  "builtin-baseline": "<commit-sha>"
}
```

Use a baseline for the registry that resolves the dependency. For the builtin registry, that means `builtin-baseline` in `vcpkg.json`. For a custom default registry, set the baseline in `vcpkg-configuration.json`.

**Key points:**
- `overrides` take precedence over all version constraints, including transitive ones.
- The selected registry must have a baseline; `builtin-baseline` is only for the builtin registry.
- Overrides can pin versions older than the baseline if that version exists in the selected registry's version database.
- Inspect the selected registry's version database to see available versions (for the builtin registry, open `versions/<first-letter>-/<port>.json` in the vcpkg repository).

---
