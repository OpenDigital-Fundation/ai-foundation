# PHP — Standards and idioms

Part of `languages:php`. Load when writing or refactoring code: style, idioms, patterns, project layout.

## PHP Coding Style

<!-- source: affaan-m/ECC rules/php/coding-style.md -->

> This file extends common/coding-style.md with PHP specific content.

### Standards

- Follow **PSR-12** formatting and naming conventions.
- Prefer `declare(strict_types=1);` in application code.
- Use scalar type hints, return types, and typed properties everywhere new code permits.

### Immutability

- Prefer immutable DTOs and value objects for data crossing service boundaries.
- Use `readonly` properties or immutable constructors for request/response payloads where possible.
- Keep arrays for simple maps; promote business-critical structures into explicit classes.

### Formatting

- Use **PHP-CS-Fixer** or **Laravel Pint** for formatting.
- Use **PHPStan** or **Psalm** for static analysis.
- Keep Composer scripts checked in so the same commands run locally and in CI.

### Imports

- Add `use` statements for all referenced classes, interfaces, and traits.
- Avoid relying on the global namespace unless the project explicitly prefers fully qualified names.

### Error Handling

- Throw exceptions for exceptional states; avoid returning `false`/`null` as hidden error channels in new code.
- Convert framework/request input into validated DTOs before it reaches domain logic.

### Reference

See skill: `architecture:system-design` for broader service/repository layering guidance.

## PHP Patterns

<!-- source: affaan-m/ECC rules/php/patterns.md -->

> This file extends common/patterns.md with PHP specific content.

### Thin Controllers, Explicit Services

- Keep controllers focused on transport: auth, validation, serialization, status codes.
- Move business rules into application/domain services that are easy to test without HTTP bootstrapping.

### DTOs and Value Objects

- Replace shape-heavy associative arrays with DTOs for requests, commands, and external API payloads.
- Use value objects for money, identifiers, date ranges, and other constrained concepts.

### Dependency Injection

- Depend on interfaces or narrow service contracts, not framework globals.
- Pass collaborators through constructors so services are testable without service-locator lookups.

### Boundaries

- Isolate ORM models from domain decisions when the model layer is doing more than persistence.
- Wrap third-party SDKs behind small adapters so the rest of the codebase depends on your contract, not theirs.

### Reference

See skill: `architecture:api-design` for endpoint conventions and response-shape guidance.
See skill: `languages:php` (`references/frameworks/laravel.md`) for Laravel-specific architecture guidance.
