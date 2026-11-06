# Java and Kotlin — Tooling

Part of `languages:jvm`. Load when formatters, linters, type checkers and editor hooks.

## Java Hooks

<!-- source: affaan-m/ECC rules/java/hooks.md -->

> This file extends common/hooks.md with Java-specific content.

### PostToolUse Hooks

Configure in `~/.claude/settings.json`:

- **google-java-format**: Auto-format `.java` files after edit
- **checkstyle**: Run style checks after editing Java files
- **./mvnw compile** or **./gradlew compileJava**: Verify compilation after changes

## Kotlin Hooks

<!-- source: affaan-m/ECC rules/kotlin/hooks.md -->

> This file extends common/hooks.md with Kotlin-specific content.

### PostToolUse Hooks

Configure in `~/.claude/settings.json`:

- **ktfmt/ktlint**: Auto-format `.kt` and `.kts` files after edit
- **detekt**: Run static analysis after editing Kotlin files
- **./gradlew build**: Verify compilation after changes
