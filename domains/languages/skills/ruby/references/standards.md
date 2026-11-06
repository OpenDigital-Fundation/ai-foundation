# Ruby — Standards and idioms

Part of `languages:ruby`. Load when writing or refactoring code: style, idioms, patterns, project layout.

## Ruby Coding Style

<!-- source: affaan-m/ECC rules/ruby/coding-style.md -->

> This file extends common/coding-style.md with Ruby and Rails specific content.

### Standards

- Target **Ruby 3.3+** for new Rails work unless the project already pins an older supported runtime.
- Enable **YJIT** in production only after measuring boot time, memory, and request/job throughput.
- Add `# frozen_string_literal: true` to new Ruby files when the project uses that convention.
- Prefer clear Ruby over clever metaprogramming; isolate DSL-heavy code behind narrow, tested boundaries.

### Formatting And Linting

- Use the project's checked-in RuboCop config. For Rails 8+ apps, start from `rubocop-rails-omakase` and customize only where the codebase has a real convention.
- Keep formatter/linter commands behind binstubs or scripts so CI and local runs match:

```bash
bundle exec rubocop
bundle exec rubocop -A
```

- Do not silence cops inline unless the exception is narrow, documented, and harder to express cleanly in code.

### Rails Style

- Follow Rails naming and directory conventions before adding custom structure.
- Keep controllers transport-focused: authentication, authorization, parameter handling, response shape.
- Put reusable domain behavior in models, concerns, service objects, query objects, or form objects based on actual complexity, not as default ceremony.
- Prefer `bin/rails`, `bin/rake`, and checked-in binstubs over globally installed commands.

### Error Handling

- Rescue specific exceptions. Avoid broad `rescue StandardError` blocks unless they re-raise or preserve enough context for operators.
- Use `ActiveSupport::Notifications` or the app's logger for operational events; do not leave `puts`, `pp`, or `debugger` in committed application code.

### Reference

See skill: `backend-patterns` for broader service/repository layering guidance.

## Ruby Patterns

<!-- source: affaan-m/ECC rules/ruby/patterns.md -->

> This file extends common/patterns.md with Ruby and Rails specific content.

### Rails Way First

- Start with plain Rails MVC and Active Record conventions for small and medium features.
- Introduce service objects, query objects, form objects, decorators, or presenters when the model/controller boundary is carrying multiple responsibilities.
- Name extracted objects after the business operation they perform, not after generic layers like `Manager` or `Processor`.

### Persistence

- Prefer PostgreSQL for multi-host production Rails apps unless the existing platform has a clear reason for MySQL or SQLite.
- Treat Rails 8 SQLite-backed defaults as viable for single-host or modest deployments, not as an automatic fit for shared multi-service systems.
- Keep raw SQL behind query objects or model scopes and parameterize every dynamic value.

### Background Jobs And Runtime Services

- Use **Solid Queue** for greenfield Rails 8 apps with modest throughput and simple deployment needs.
- Use **Sidekiq** when the app needs mature observability, high throughput, existing Redis infrastructure, or Pro/Enterprise features.
- Use **Solid Cache** and **Solid Cable** when their deployment model matches the app; use Redis when shared cross-service behavior, high fanout, or advanced data structures matter.

### Frontend

- Prefer **Hotwire** with Turbo, Stimulus, Importmap, and Propshaft for server-rendered Rails apps.
- Use React, Vue, Inertia.js, or a separate SPA when interaction complexity, existing product architecture, or team ownership justifies the extra client surface.
- Keep view components, partials, and presenters focused on rendering decisions; keep persistence and authorization out of templates.

### Authentication

- Use the Rails 8 authentication generator for straightforward session auth and password reset needs.
- Use Devise or another established auth system when requirements include OAuth, MFA, confirmable/lockable flows, multi-model auth, or a large existing Devise footprint.

### Reference

See skill: `backend-patterns` for service boundaries and adapter patterns.
