# TypeScript and JavaScript — nuxt

Part of `languages:typescript`. Load only when the project uses nuxt.

## Nuxt Coding Style

<!-- source: affaan-m/ECC rules/nuxt/coding-style.md -->

> This file extends common/coding-style.md with Nuxt specific content.

### Directory layout

- Default `srcDir` is `app/`. Framework files live at `app/pages/`, `app/layouts/`, `app/middleware/`, `app/plugins/`, `app/app.config.ts`. `nuxt.config.ts` and `server/` stay at project root.
- Some projects override `srcDir` to `src/` for a Feature-Sliced Design layout, remapping `dir.pages` (for example to `src/app/routes`), `dir.layouts`, and the `@`/`~` aliases. Always check `nuxt.config.ts` before assuming a path.

### Auto-imports discipline

- Composables in `app/composables/` and `server/utils/` auto-import. Do NOT manually import Nuxt composables (`useFetch`, `useState`, `navigateTo`) or `defineStore` / `storeToRefs`.
- Do NOT add a standalone `vue-router` dep (Nuxt bundles v5) or hand-mount `createApp` / `createPinia` / `createRouter`. The framework wires these.

### Compiler macros

- `definePageMeta` is a compile-time macro. Static values only, no reactive data and no side-effect calls inside it.
- Augment typed `PageMeta` via `declare module '#app'` rather than casting.

### Config file separation

Three distinct files, do not conflate.

- `nuxt.config.ts` = build-time only (`routeRules`, `modules`, `nitro`, `ssr` flag). Not reactive.
- `runtimeConfig` (inside nuxt.config) = per-env runtime values, env-overridable via `NUXT_*`. Root keys are server-only, `public` keys are client-visible.
- `app/app.config.ts` = public build-fixed reactive settings (theme tokens, feature flags). No env override. NEVER secrets.

### Head and meta

- `app.head` in `nuxt.config.ts` takes static values only.
- Reactive meta goes through `useHead` / `useSeoMeta` in component setup, never via `app.head`.

### Reference

- Related: `languages:typescript` (`references/frameworks/nuxt.md`), `languages:typescript` (`references/frameworks/vite.md`), `languages:typescript` (`references/standards.md`).
- [Nuxt directory structure](https://nuxt.com/docs/guide/directory-structure/app)
- [Nuxt configuration](https://nuxt.com/docs/api/nuxt-config)

## Nuxt Patterns

<!-- source: affaan-m/ECC rules/nuxt/patterns.md -->

> This file extends common/patterns.md with Nuxt specific content.

### Data-fetch selection

Load-bearing. Pick by render timing, not habit.

- `useFetch(url)` = SSR-safe, URL-first initial/first-paint data. The default. Forwards the server result through the payload so there is no hydration double-fetch.
- `useAsyncData(key, fn)` = SSR-safe, custom async logic (SDK / GraphQL / combined calls). The explicit key shares the result across components.
- `$fetch` = client interactions only (form submit, button click, POST/PUT/DELETE). NOT SSR-safe, double-fetches if used for first paint.
- Rule: `useFetch` / `useAsyncData` for anything rendered on first paint, `$fetch` only for event-driven mutations.

### Shared state

- `useState('key', () => init)` for SSR-safe shared state. Values must be JSON-serializable.
- NEVER `export const x = ref()` at module scope. One shared instance leaks across concurrent SSR requests and causes a memory leak.
- With `@pinia/nuxt`: Pinia for domain state, `useState` for small cross-component primitives.
- Async server-side init goes in `callOnce(async () => {...})`, not as a side effect inside `useAsyncData`.

### Nitro server routes

- `server/api/*.{get,post}.ts` auto-register by path + method. Handler is `defineEventHandler((event) => ...)`.
- Errors via `throw createError({ status, statusText })`. Prefer the Web-API `status` / `statusText` over deprecated `statusCode` / `statusMessage`.
- `server/middleware/` must NOT return a response. Only mutate `event.context` or set headers.

### Route middleware

- `app/middleware/*.ts` with `defineNuxtRouteMiddleware((to, from) => ...)`.
- Use the `to` / `from` args. Do NOT call `useRoute()` inside middleware.
- `.global` suffix runs on every route. Return `navigateTo()` to redirect, `abortNavigation()` to stop.

### Hydration-safe rendering

- Route off `status` (`idle | pending | success | error`) for lazy fetches.
- `useAsyncData` payload uses `devalue` (Date/Map/Set/refs survive). A `server/api` response is `JSON.stringify`-only, so define `toJSON()` for non-JSON types.
- Shrink payload with `pick` / `transform`. This reduces serialized size, it does not skip the fetch.

### Reference

- Related: `languages:typescript` (`references/frameworks/nuxt.md`), `languages:typescript` (`references/frameworks/vite.md`), `languages:typescript` (`references/standards.md`).
- [Nuxt data fetching](https://nuxt.com/docs/getting-started/data-fetching)
- [Nuxt state management](https://nuxt.com/docs/getting-started/state-management)
- [Nuxt server engine (Nitro)](https://nuxt.com/docs/guide/directory-structure/server)

## Nuxt 4 Patterns

<!-- source: affaan-m/ECC pi/core/skills/nuxt4-patterns/SKILL.md -->

Use when building or debugging Nuxt 4 apps with SSR, hybrid rendering, route rules, or page-level data fetching.

### When to Activate

- Hydration mismatches between server HTML and client state
- Route-level rendering decisions such as prerender, SWR, ISR, or client-only sections
- Performance work around lazy loading, lazy hydration, or payload size
- Page or component data fetching with `useFetch`, `useAsyncData`, or `$fetch`
- Nuxt routing issues tied to route params, middleware, or SSR/client differences

### Hydration Safety

- Keep the first render deterministic. Do not put `Date.now()`, `Math.random()`, browser-only APIs, or storage reads directly into SSR-rendered template state.
- Move browser-only logic behind `onMounted()`, `import.meta.client`, `ClientOnly`, or a `.client.vue` component when the server cannot produce the same markup.
- Use Nuxt's `useRoute()` composable, not the one from `vue-router`.
- Do not use `route.fullPath` to drive SSR-rendered markup. URL fragments are client-only, which can create hydration mismatches.
- Treat `ssr: false` as an escape hatch for truly browser-only areas, not a default fix for mismatches.

### Data Fetching

- Prefer `await useFetch()` for SSR-safe API reads in pages and components. It forwards server-fetched data into the Nuxt payload and avoids a second fetch on hydration.
- Use `useAsyncData()` when the fetcher is not a simple `$fetch()` call, when you need a custom key, or when you are composing multiple async sources.
- Give `useAsyncData()` a stable key for cache reuse and predictable refresh behavior.
- Keep `useAsyncData()` handlers side-effect free. They can run during SSR and hydration.
- Use `$fetch()` for user-triggered writes or client-only actions, not top-level page data that should be hydrated from SSR.
- Use `lazy: true`, `useLazyFetch()`, or `useLazyAsyncData()` for non-critical data that should not block navigation. Handle `status === 'pending'` in the UI.
- Use `server: false` only for data that is not needed for SEO or the first paint.
- Trim payload size with `pick` and prefer shallower payloads when deep reactivity is unnecessary.

```ts
const route = useRoute()

const { data: article, status, error, refresh } = await useAsyncData(
  () => `article:${route.params.slug}`,
  () => $fetch(`/api/articles/${route.params.slug}`),
)

const { data: comments } = await useFetch(`/api/articles/${route.params.slug}/comments`, {
  lazy: true,
  server: false,
})
```

### Route Rules

Prefer `routeRules` in `nuxt.config.ts` for rendering and caching strategy:

```ts
export default defineNuxtConfig({
  routeRules: {
    '/': { prerender: true },
    '/products/**': { swr: 3600 },
    '/blog/**': { isr: true },
    '/admin/**': { ssr: false },
    '/api/**': { cache: { maxAge: 60 * 60 } },
  },
})
```

- `prerender`: static HTML at build time
- `swr`: serve cached content and revalidate in the background
- `isr`: incremental static regeneration on supported platforms
- `ssr: false`: client-rendered route
- `cache` or `redirect`: Nitro-level response behavior

Pick route rules per route group, not globally. Marketing pages, catalogs, dashboards, and APIs usually need different strategies.

### Lazy Loading and Performance

- Nuxt already code-splits pages by route. Keep route boundaries meaningful before micro-optimizing component splits.
- Use the `Lazy` prefix to dynamically import non-critical components.
- Conditionally render lazy components with `v-if` so the chunk is not loaded until the UI actually needs it.
- Use lazy hydration for below-the-fold or non-critical interactive UI.

```vue
<template>
  <LazyRecommendations v-if="showRecommendations" />
  <LazyProductGallery hydrate-on-visible />
</template>
```

- For custom strategies, use `defineLazyHydrationComponent()` with a visibility or idle strategy.
- Nuxt lazy hydration works on single-file components. Passing new props to a lazily hydrated component will trigger hydration immediately.
- Use `NuxtLink` for internal navigation so Nuxt can prefetch route components and generated payloads.

### Review Checklist

- First SSR render and hydrated client render produce the same markup
- Page data uses `useFetch` or `useAsyncData`, not top-level `$fetch`
- Non-critical data is lazy and has explicit loading UI
- Route rules match the page's SEO and freshness requirements
- Heavy interactive islands are lazy-loaded or lazily hydrated

## Nuxt Testing

<!-- source: affaan-m/ECC rules/nuxt/testing.md -->

> This file extends common/testing.md with Nuxt specific content.

Package: `@nuxt/test-utils`. Vitest-first for unit and component tests, with built-in Playwright browser E2E support. nuxt-vitest and vitest-environment-nuxt are superseded and folded into it.

### Setup

- Install dev deps: `@nuxt/test-utils vitest @vue/test-utils happy-dom playwright-core`.
- Config: `defineVitestConfig({ test: { environment: 'nuxt' } })` from `@nuxt/test-utils/config`. Use `defineVitestProject` for multi-project (separate unit / nuxt / e2e environments).
- Add `@nuxt/test-utils/module` to `nuxt.config`. Per-file opt-in via `// @vitest-environment nuxt`.

### Runtime helpers

Import from `@nuxt/test-utils/runtime`.

- `mountSuspended(component, opts)` mounts in the Nuxt env with async setup + plugin injection (accepts `@vue/test-utils` mount options + `route`).
- `renderSuspended(component, opts)` is the Testing Library variant (needs `@testing-library/vue`).
- `mockNuxtImport(name, factory)` mocks auto-imports (e.g. `useState`). Once per import per file, use `vi.hoisted()`.
- `mockComponent(name, factory)` mocks by PascalCase name or path.
- `registerEndpoint(path, handler|opts)` mocks a Nitro endpoint to test server routes or stub the backend. Supports method + `once`.

### E2E helpers

Import from `@nuxt/test-utils/e2e`.

- `await setup({ rootDir, server, browser, ... })` inside the describe block (manages beforeAll/afterAll).
- Then `$fetch(url)` (rendered HTML), `fetch(url)` (response object), `url(path)` (full URL with port), `createPage(url)` (Playwright).
- Playwright integration: import `expect` / `test` from `@nuxt/test-utils/playwright`.

### What to test how

- Composables: mock auto-imports with `mockNuxtImport`, mount a host component via `mountSuspended` to exercise `useState` / `useFetch` in the Nuxt runtime.
- Server routes: `registerEndpoint` to stub, or e2e `$fetch` / `fetch` against the real Nitro server.

### Reference

- Related: `languages:typescript` (`references/frameworks/nuxt.md`), `testing:browser-testing`, `languages:typescript` (`references/frameworks/vite.md`).
- [Nuxt testing docs](https://nuxt.com/docs/getting-started/testing)
- [@nuxt/test-utils npm](https://www.npmjs.com/package/@nuxt/test-utils)

## Nuxt Security

<!-- source: affaan-m/ECC rules/nuxt/security.md -->

> This file extends common/security.md with Nuxt specific content.

### runtimeConfig public vs private

- Root `runtimeConfig` keys are server-only. `runtimeConfig.public` serializes into EVERY page payload (client-visible).
- Secrets go at root only. Never put secrets in `app.config.ts` or `runtimeConfig.public`, both ship to the client bundle.
- Official warning: "Be careful not to expose runtime config keys to the client-side by either rendering them or passing them to `useState`."

### Server-route input validation

- Use h3 validating readers. Do NOT trust raw `readBody` / `getQuery` / `getRouterParam`.
  - `readValidatedBody(event, schema)` validates the body.
  - `getValidatedQuery(event, schema)` validates the query.
  - `getValidatedRouterParams(event, schema)` validates route params.
- All accept a validation function or a Zod schema and throw on failure.

### SSR payload leakage

- Anything in `useState`, `useFetch` / `useAsyncData` results, or `runtimeConfig.public` is serialized into the client payload. Never write a secret into those.
- Use `useServerSeoMeta` for server-only meta with no client cost.

### Cookie and auth passthrough on SSR

- Nuxt does NOT auto-attach the incoming user's cookies to outbound server-side `$fetch`.
- Forward explicitly with `useRequestFetch()` (cleanest, pre-bound to request headers) or `useRequestHeaders(['cookie'])`.
- Relay a backend `Set-Cookie` to the browser via `$fetch.raw` + `appendResponseHeader(event, 'set-cookie', ...)`.
- socket.io is client-only (`.client.ts` plugin), never SSR.

### SSRF on server $fetch

- Server routes run with full network egress. Never pass user-controlled input directly into a server-side `$fetch` URL or host.
- Validate the param first (h3 utilities above), allowlist the target, pin to `runtimeConfig.public.apiBase`, reject user-supplied absolute URLs.
- Auto-trigger `code-quality:code-review` only for routes that make external network requests (server `$fetch`), handle auth tokens or credentials, or perform sensitive mutations or authorization checks. Examples: SSRF-prone proxy endpoints, token exchange or password reset, admin actions. Skip benign read-only routes that only accept validated query params.

### Reference

- Related: `security:security-audit`, `languages:typescript` (`references/frameworks/nuxt.md`).
- [Nuxt runtime config](https://nuxt.com/docs/guide/going-further/runtime-config)
- [h3 request utils](https://v1.h3.dev/utils/request)

## Expert Nuxt Developer

<!-- source: github/awesome-copilot agents/nuxt-expert.agent.md -->

You are a world-class Nuxt expert with deep experience building modern, production-grade applications using Nuxt 3, Vue 3, Nitro, and TypeScript.

### Your Expertise

- **Nuxt 3 Architecture**: App structure, pages/layouts, plugins, middleware, and composables
- **Nitro Runtime**: Server routes, API handlers, edge/serverless targets, and deployment patterns
- **Data Fetching**: Mastery of `useFetch`, `useAsyncData`, server/client execution, caching, and hydration behavior
- **Rendering Modes**: SSR, SSG, hybrid rendering, route rules, and ISR-like strategies
- **Vue 3 Foundations**: `<script setup>`, Composition API, reactivity, and component patterns
- **State Management**: Pinia patterns, store organization, and server/client state synchronization
- **Performance**: Route-level optimization, payload size reduction, lazy loading, and Web Vitals improvements
- **TypeScript**: Strong typing for composables, runtime config, API layers, and component props/emits
- **Testing**: Unit/integration/e2e strategies with Vitest, Vue Test Utils, and Playwright

### Your Approach

- **Nuxt 3 First**: Favor current Nuxt 3 patterns for all new work
- **Server-Aware by Default**: Make execution context explicit (server vs client) to avoid hydration/runtime bugs
- **Performance-Conscious**: Optimize data access and bundle size early
- **Type-Safe**: Use strict typing across app, API, and shared schemas
- **Progressive Enhancement**: Build experiences that remain robust under partial JS/network constraints
- **Maintainable Structure**: Keep composables, stores, and server logic cleanly separated
- **Legacy-Aware**: Provide migration-safe advice for Nuxt 2/Vue 2 codebases when needed

### Guidelines

- Prefer Nuxt 3 conventions (`pages/`, `server/`, `composables/`, `plugins/`) for new code
- Use `useFetch` and `useAsyncData` intentionally: choose based on caching, keying, and lifecycle needs
- Keep server logic inside `server/api` or Nitro handlers, not in client components
- Use runtime config (`useRuntimeConfig`) instead of hard-coded environment values
- Implement clear route rules for caching and rendering strategy
- Use auto-imported composables responsibly and avoid hidden coupling
- Use Pinia for shared client state; avoid over-centralized global stores
- Prefer composables for reusable logic over monolithic utilities
- Add explicit loading and error states for async data paths
- Handle hydration edge cases (browser-only APIs, non-deterministic values, time-based rendering)
- Use lazy hydration and dynamic imports for heavy UI areas
- Write testable code and include test guidance when proposing architecture
- For legacy projects, propose incremental migration from Nuxt 2 to Nuxt 3 with minimal disruption

### Common Scenarios You Excel At

- Building or refactoring Nuxt 3 applications with scalable folder architecture
- Designing SSR/SSG/hybrid rendering strategies for SEO and performance
- Implementing robust API layers with Nitro server routes and shared validation
- Debugging hydration mismatches and client/server data inconsistencies
- Migrating from Nuxt 2/Vue 2 to Nuxt 3/Vue 3 using phased, low-risk steps
- Optimizing Core Web Vitals in content-heavy or data-heavy Nuxt apps
- Structuring authentication flows with route middleware and secure token handling
- Integrating CMS/e-commerce backends with efficient cache and revalidation strategy

### Response Style

- Provide complete, production-ready Nuxt examples with clear file paths
- Explain whether code runs on server, client, or both
- Include TypeScript types for props, composables, and API responses
- Highlight trade-offs for rendering and data-fetching decisions
- Include migration notes when a legacy Nuxt/Vue pattern is involved
- Prefer pragmatic, minimal-complexity solutions over over-engineering

### Legacy Compatibility Guidance

- Support Nuxt 2/Vue 2 codebases with explicit migration recommendations
- Preserve behavior first, then modernize structure and APIs incrementally
- Recommend compatibility bridges only when they reduce risk
- Avoid big-bang rewrites unless explicitly requested
