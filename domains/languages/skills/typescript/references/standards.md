# TypeScript and JavaScript — Standards and idioms

Part of `languages:typescript`. Load when writing or refactoring code: style, idioms, patterns, project layout.

## TypeScript/JavaScript Coding Style

<!-- source: affaan-m/ECC rules/typescript/coding-style.md -->

> This file extends common/coding-style.md with TypeScript/JavaScript specific content.

### Types and Interfaces

Use types to make public APIs, shared models, and component props explicit, readable, and reusable.

#### Public APIs

- Add parameter and return types to exported functions, shared utilities, and public class methods
- Let TypeScript infer obvious local variable types
- Extract repeated inline object shapes into named types or interfaces

```typescript
// WRONG: Exported function without explicit types
export function formatUser(user) {
  return `${user.firstName} ${user.lastName}`
}

// CORRECT: Explicit types on public APIs
interface User {
  firstName: string
  lastName: string
}

export function formatUser(user: User): string {
  return `${user.firstName} ${user.lastName}`
}
```

#### Interfaces vs. Type Aliases

- Use `interface` for object shapes that may be extended or implemented
- Use `type` for unions, intersections, tuples, mapped types, and utility types
- Prefer string literal unions over `enum` unless an `enum` is required for interoperability

```typescript
interface User {
  id: string
  email: string
}

type UserRole = 'admin' | 'member'
type UserWithRole = User & {
  role: UserRole
}
```

#### Avoid `any`

- Avoid `any` in application code
- Use `unknown` for external or untrusted input, then narrow it safely
- Use generics when a value's type depends on the caller

```typescript
// WRONG: any removes type safety
function getErrorMessage(error: any) {
  return error.message
}

// CORRECT: unknown forces safe narrowing
function getErrorMessage(error: unknown): string {
  if (error instanceof Error) {
    return error.message
  }

  return 'Unexpected error'
}
```

#### React Props

- Define component props with a named `interface` or `type`
- Type callback props explicitly
- Do not use `React.FC` unless there is a specific reason to do so

```typescript
interface User {
  id: string
  email: string
}

interface UserCardProps {
  user: User
  onSelect: (id: string) => void
}

function UserCard({ user, onSelect }: UserCardProps) {
  return <button onClick={() => onSelect(user.id)}>{user.email}</button>
}
```

#### JavaScript Files

- In `.js` and `.jsx` files, use JSDoc when types improve clarity and a TypeScript migration is not practical
- Keep JSDoc aligned with runtime behavior

```javascript
/**
 * @param {{ firstName: string, lastName: string }} user
 * @returns {string}
 */
export function formatUser(user) {
  return `${user.firstName} ${user.lastName}`
}
```

### Immutability

Use spread operator for immutable updates:

```typescript
interface User {
  id: string
  name: string
}

// WRONG: Mutation
function updateUser(user: User, name: string): User {
  user.name = name // MUTATION!
  return user
}

// CORRECT: Immutability
function updateUser(user: Readonly<User>, name: string): User {
  return {
    ...user,
    name
  }
}
```

### Error Handling

Use async/await with try-catch and narrow unknown errors safely:

```typescript
interface User {
  id: string
  email: string
}

declare function riskyOperation(userId: string): Promise<User>

function getErrorMessage(error: unknown): string {
  if (error instanceof Error) {
    return error.message
  }

  return 'Unexpected error'
}

const logger = {
  error: (message: string, error: unknown) => {
    // Replace with your production logger (for example, pino or winston).
  }
}

async function loadUser(userId: string): Promise<User> {
  try {
    const result = await riskyOperation(userId)
    return result
  } catch (error: unknown) {
    logger.error('Operation failed', error)
    throw new Error(getErrorMessage(error))
  }
}
```

### Input Validation

Use Zod for schema-based validation and infer types from the schema:

```typescript
import { z } from 'zod'

const userSchema = z.object({
  email: z.string().email(),
  age: z.number().int().min(0).max(150)
})

type UserInput = z.infer<typeof userSchema>

const validated: UserInput = userSchema.parse(input)
```

### Console.log

- No `console.log` statements in production code
- Use proper logging libraries instead
- See hooks for automatic detection

## TypeScript/JavaScript Patterns

<!-- source: affaan-m/ECC rules/typescript/patterns.md -->

> This file extends common/patterns.md with TypeScript/JavaScript specific content.

### API Response Format

```typescript
interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  meta?: {
    total: number
    page: number
    limit: number
  }
}
```

### Custom Hooks Pattern

```typescript
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {
    const handler = setTimeout(() => setDebouncedValue(value), delay)
    return () => clearTimeout(handler)
  }, [value, delay])

  return debouncedValue
}
```

### Repository Pattern

```typescript
interface Repository<T> {
  findAll(filters?: Filters): Promise<T[]>
  findById(id: string): Promise<T | null>
  create(data: CreateDto): Promise<T>
  update(id: string, data: UpdateDto): Promise<T>
  delete(id: string): Promise<void>
}
```

## TypeScript Development Patterns

<!-- source: affaan-m/ECC pi/core/skills/typescript-patterns/SKILL.md -->

TypeScript patterns and best practices for building robust, type-safe, and maintainable applications. The compiler is most useful when it can prove your program's shape, so the guiding principle here is: push the type system to do real work instead of fighting it. This skill is the "how." For the "what" and "when" (the decisions about which pattern to reach for), see the TypeScript rules — `rules/typescript/coding-style.md` and `rules/typescript/patterns.md` in this repository, installed as `rules/ecc/typescript/coding-style.md` and `rules/ecc/typescript/patterns.md`.

### When to Activate

- Writing new TypeScript or JavaScript code
- Reviewing a PR that touches `.ts` or `.tsx` files
- Refactoring existing TypeScript to remove `any`, tighten types, or add strictness
- Designing types, generics, or module boundaries for a new feature
- Setting up a new TypeScript project or upgrading `tsconfig.json`
- Debugging type errors that cascade through a codebase (usually a design problem, not an annotation problem)

### Core Principles

#### 1. Strict Mode Is the Baseline

`strict: true` (which enables `strictNullChecks`, `noImplicitAny`, `strictFunctionTypes`, and the rest) is not optional in a healthy codebase. If a codebase cannot compile under strict, that is a migration task, not an excuse to leave the flag off.

```jsonc
// tsconfig.json — a strict, discriminating baseline
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitOverride": true,
    "noFallthroughCasesInSwitch": true,
    "noPropertyAccessFromIndexSignature": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "forceConsistentCasingInFileNames": true,
    "verbatimModuleSyntax": true
  }
}
```

`noUncheckedIndexedAccess` makes array and record access possibly-undefined, which surfaces a whole class of runtime crashes at compile time. If it produces too much noise, this is the pattern to add, not the flag to remove:

```typescript
// If you have proven the index exists, lift the element into a local first.
const [first] = items
if (first === undefined) {
  throw new Error("expected at least one item")
}
```

#### 2. `any` Is a Bug, Not a Tool

`any` disables the type system exactly where a bug is most likely to hide: at the boundary with untrusted or dynamic data. Prefer `unknown` and narrow it. When you truly need a fallback, prefer an explicit loosening with a comment over a silent `any`.

```typescript
// Bad: any disables checking on the public API
export function parseConfig(raw: any): Config {
  return raw.config ?? {}
}

interface Config {
  timeout: number
  retries: number
}

const DEFAULT_CONFIG: Config = { timeout: 30_000, retries: 3 }

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null
}

function toPositiveInt(value: unknown, field: string): number {
  if (typeof value !== 'number' || !Number.isInteger(value) || value <= 0) {
    throw new TypeError(`Expected ${field} to be a positive integer`)
  }
  return value
}

// Good: unknown forces safe narrowing at the edge. Every consumed field is
// validated with an explicit range, and defaults are declared up front.
export function parseConfig(raw: unknown): Config {
  if (!isRecord(raw)) return { ...DEFAULT_CONFIG }
  return {
    timeout: raw['timeout'] === undefined ? DEFAULT_CONFIG.timeout : toPositiveInt(raw['timeout'], 'timeout'),
    retries: raw['retries'] === undefined ? DEFAULT_CONFIG.retries : toPositiveInt(raw['retries'], 'retries'),
  }
}
```

#### 3. Public APIs Get Explicit Types, Locals Get Inference

TypeScript infers local variables well. Exporting functions whose parameter and return types are implicit leaks inference decisions into every consumer and makes intent unreadable.

```typescript
// Bad: exported API without explicit types
export function formatUser(user) {
  return `${user.firstName} ${user.lastName}`
}

// Good: explicit public contract, inferred internals
interface User {
  firstName: string
  lastName: string
}

export function formatUser(user: User): string {
  return `${user.firstName} ${user.lastName}`
}
```

### Type Design

#### Interfaces vs. Type Aliases

`interface` for object shapes that may be extended or implemented; `type` for unions, intersections, tuples, mapped types, and utility types. Prefer string-literal unions over `enum` unless you need runtime value enumeration or interop with code that requires it.

```typescript
interface User {
  id: string
  email: string
}

type UserRole = 'admin' | 'member'
type AdminUser = User & { role: 'admin' }
```

#### Discriminated Unions Are the Default State Machine

When a value can be in multiple shapes, model it as a discriminated union with a literal `type`/`kind` field. Exhaustive checking then becomes a free compiler feature: never a runtime fallback, always a compile error on a missing branch.

```typescript
type Transaction =
  | { kind: 'draft'; id: string }
  | { kind: 'submitted'; id: string; submittedAt: Date }
  | { kind: 'paid'; id: string; paidAt: Date; amountCents: number }

function describe(t: Transaction): string {
  switch (t.kind) {
    case 'draft':
      return 'Saved but not sent'
    case 'submitted':
      return `Submitted on ${t.submittedAt.toISOString()}`
    case 'paid':
      return `Paid ${t.amountCents} cents on ${t.paidAt.toISOString()}`
    default:
      // exhaustive: any new member forces this to fail to compile
      return assertNever(t)
  }
}

function assertNever(value: never): never {
  throw new Error(`Unhandled member: ${JSON.stringify(value)}`)
}
```

#### Brands and Nominal Safety Where Structure Is Not Enough

Structural typing cannot tell `CustomerId` from `string`. When an ID or unit must not be confused with another, add a brand (a phantom field with a unique symbol key).

```typescript
declare const brand: unique symbol

export type CustomerId = string & { [brand]: 'CustomerId' }

function ensureCustomerId(value: string): CustomerId {
  if (!/^cus_[a-z0-9]+$/.test(value)) {
    throw new TypeError(`Invalid customer id: ${value}`)
  }
  return value as CustomerId
}
```

Keep brands internal to a boundary module; never expose the cast helper far from the validation that justifies it.

#### Generics Model Caller-Dependent Types

If a value's type depends on what the caller supplies, make it generic rather than flattening to `any` or `unknown` and hand-casting at call sites.

```typescript
// Bad: caller must cast the result
export function getCached(key: string): unknown {
  return cache.get(key)
}

// Good: the caller's type flows through
export function getCached<T>(key: string, parse: (raw: string) => T): T | undefined {
  const raw = cache.get(key)
  if (raw === undefined) return undefined
  return parse(raw)
}
```

Constrain generics so the contract is discoverable: prefer `T extends SomeShape` over free-floating `T` when a shape assumption exists.

#### Options Objects over Positional Parameters

Functions with more than a couple of knobs should take a single options object. It makes call sites self-documenting and lets new knobs be added without positional churn.

```typescript
interface FetchOptions {
  timeoutMs?: number
  retries?: number
  signal?: AbortSignal
}

export async function fetchWithRetry(url: string, options: FetchOptions = {}): Promise<Response> {
  // ...
}
```

### Narrowing and Runtime Safety

#### Validate at the Boundary, Trust Inside

Untrusted data enters at I/O boundaries: API handlers, message consumers, file loaders. Parse and validate once with a schema, then carry the refined type through the domain. This is where a validation library (for example, Zod) earns its keep — the schema is both the runtime check and the compile-time type.

```typescript
import { z } from 'zod'

const userInputSchema = z.object({
  email: z.string().email(),
  age: z.number().int().min(0).max(150)
})

export type UserInput = z.infer<typeof userInputSchema>

// validate once at the edge
const input: UserInput = userInputSchema.parse(rawBody)
```

#### Type Predicates and Assertion Functions

Prefer type predicates and assertion functions over unchecked casts when guarding shapes. The guard documents the invariant and the compiler checks its usage.

```typescript
function isConfig(value: unknown): value is Config {
  if (typeof value !== 'object' || value === null) return false
  if (!('timeout' in value) || !('retries' in value)) return false
  const { timeout, retries } = value
  return (
    typeof timeout === 'number' && Number.isInteger(timeout) && timeout > 0 &&
    typeof retries === 'number' && Number.isInteger(retries) && retries > 0
  )
}
```

To fail loudly on a malformed value instead of returning a boolean, use an assertion signature:

```typescript
function assertIsStringArray(value: unknown): asserts value is string[] {
  if (!Array.isArray(value)) {
    throw new TypeError('Expected an array of strings')
  }
  // Iteration visits sparse positions as undefined instead of skipping them.
  for (const item of value) {
    if (typeof item !== 'string') throw new TypeError('Expected an array of strings')
  }
}
```

#### Readonly by Default

Mark array and object parameters `readonly`/`ReadonlyArray` when the function does not mutate them. It prevents accidental mutation and signals intent at the signature. (Per the coding-style rules, prefer the spread operator for immutable updates.)

```typescript
export function totalAmount(items: readonly LineItem[]): number {
  return items.reduce((sum, item) => sum + item.amountCents, 0)
}
```

Runtime immutability (for example, `Object.freeze`) is for hot application boundaries; `readonly` in type positions is the everyday guard.

### Error Handling

#### Fail at the Boundary, Handle at the Edge

The `try/catch` belongs where the caller can act on failure — not wrapped around every internal call in a stack of swallowed errors. Use async/await with `try/catch` and narrow `unknown` errors safely (per the coding-style rules).

This endpoint example accepts non-empty IDs made of ASCII letters, digits, underscores, and hyphens, such as `u_1`. Validate that contract before constructing the path or making a request. Adapt the identifier grammar to the real API.

```typescript
type User = { id: string; email: string }

function isUser(value: unknown): value is User {
  if (typeof value !== 'object' || value === null) return false
  if (!('id' in value) || !('email' in value)) return false
  const { id, email } = value
  return (
    typeof id === 'string' && id.length > 0 &&
    typeof email === 'string' && email.includes('@')
  )
}

function assertUserId(userId: string): void {
  if (typeof userId !== 'string' || userId.length === 0 || /[^A-Za-z0-9_-]/.test(userId)) {
    throw new TypeError('Expected a user ID using letters, digits, "_" or "-"')
  }
}

async function loadUser(userId: string): Promise<User> {
  assertUserId(userId)
  const response = await fetch(`/users/${userId}`)
  if (!response.ok) {
    throw new Error(`Failed to load user ${userId}: ${response.status}`)
  }
  const data: unknown = await response.json()
  if (!isUser(data)) {
    throw new TypeError(`Invalid user payload for ${userId}`)
  }
  return data
}

export async function getUser(userId: string): Promise<User> {
  try {
    return await loadUser(userId)
  } catch (error: unknown) {
    if (error instanceof Error) {
      // known failure mode: retry or surface a friendly message
      throw new Error(`user lookup failed: ${error.message}`, { cause: error })
    }
    throw new TypeError('unknown error shape')
  }
}
```

#### Result Types for Expected Failures

For expected business failures (validation, not-found, conflict), a discriminated `Result` union makes failure explicit in the type instead of hiding it in the exception flow.

```typescript
type Result<T, E> = { ok: true; value: T } | { ok: false; error: E }

function createUser(input: UserInput): Result<User, ValidationIssue[]> {
  const issues = validate(input)
  if (issues.length > 0) {
    return { ok: false, error: issues }
  }
  return { ok: true, value: { id: generateId(), ...input } }
}
```

Reserve exceptions for the unexpected. Expected outcomes belong in the return type.

#### Preserve Error Context

Use `new Error(message, { cause })` (available since ES2022) so the original failure chain survives rewrapping. Never stringify errors into a message and lose the cause.

### Async Patterns

#### Prefer `Promise.allSettled` for Independent Fan-Out

When results are independent and one failure must not drop the others, use `Promise.allSettled` and handle the per-promise outcomes.

```typescript
const results: PromiseSettledResult<number>[] = await Promise.allSettled(
  sourceIds.map((id) => fetchCount(id))
)

const total = results.reduce((sum, result) => {
  if (result.status === 'fulfilled') {
    return sum + result.value
  }
  log.warn('count fetch failed', result.reason)
  return sum
}, 0)
```

Use `Promise.all` when you want fail-fast semantics — genuinely all-or-nothing work.

#### Avoid Unbounded Concurrency

Fanning out hundreds of promises at once overwhelms connections and event loop. Bound the concurrency with a small pool.

```typescript
async function mapWithConcurrency<T, R>(
  items: readonly T[],
  limit: number,
  mapper: (item: T) => Promise<R>
): Promise<R[]> {
  if (!Number.isInteger(limit) || limit < 1) {
    throw new RangeError(`Expected concurrency limit to be a positive integer, got: ${limit}`)
  }
  const results: R[] = new Array(items.length)
  let nextIndex = 0

  const workers = Array.from({ length: Math.min(limit, items.length) }, async () => {
    while (true) {
      const index = nextIndex++
      if (index >= items.length) return
      // Required under noUncheckedIndexedAccess: the index is proven
      // in-bounds above, but the compiler still types this T | undefined.
      // Skip only genuine sparse-array holes, mirroring Array.prototype.map:
      // a present `undefined` element is a legitimate value and must still
      // reach the mapper.
      if (!Object.hasOwn(items, index)) continue
      // Presence is proven above, so the indexed access is in-bounds and
      // filled — never a hole and never the compiler's speculative undefined.
      results[index] = await mapper(items[index]!)
    }
  })

  // One worker rejecting rejects the whole pool: Promise.all propagates the
  // first rejection to the caller (fail-fast). That is rejection, not
  // cancellation — the other workers keep running and may settle more of
  // their remaining items after the pool has already rejected. Use
  // Promise.all only when leaving that in-flight work running is acceptable;
  // otherwise use allSettled or thread an AbortSignal through the mapper.
  await Promise.all(workers)
  return results
}
```

#### Timeouts and Cancellation

Always thread `AbortSignal` through long-running or outbound work so callers can cancel; pair it with `Promise.race` for hard timeouts where the underlying operation cannot be aborted.

```typescript
function withTimeout<T>(promise: Promise<T>, ms: number): Promise<T> {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(`Timed out after ${ms}ms`)), ms)
    promise.then(
      (value) => {
        clearTimeout(timer)
        resolve(value)
      },
      (reason) => {
        clearTimeout(timer)
        reject(reason)
      }
    )
  })
}
```

### Null and Undefined Discipline

Prefer a discriminated approach over mixing sentinel values. Where "not found" or "absent" is a legitimate state, use `T | undefined` and check explicitly; avoid deeply nesting `?.` chains followed by silent fallbacks that hide bugs.

```typescript
function findUser(id: string): User | undefined {
  return users.get(id)
}

const user = findUser('u_1')
if (user === undefined) {
  return notFound()
}
// from here on, `user` is narrowed to User
```

Avoid truthiness checks that silently accept wrong types (`if (result)` when `result` may be `0` or `''`). Compare against `undefined`/`null` explicitly.

### Module Boundaries and Exports

#### Small, Named Modules

Expose a deliberate surface at each module's boundary. Prefer explicit named exports over default exports, and re-export at the public edge so consumers import from the module that owns the type — not from deep internals that can be refactored.

```typescript
// user/model.ts — internal types
export interface UserAccount {
  id: string
  email: string
  role: UserRole
}

// user/index.ts — public surface
export { type UserAccount, type UserRole } from './model'
export { createUser, findUser, updateUser } from './service'
```

#### Avoid Barrel Bloat and Circular Imports

Do not create barrels that import everything at module load (they defeat tree-shaking and grow cold-start). Import concrete paths. Circular imports signal a submission boundary that should fold upward; the type that both sides need belongs in a shared module neither imports.

#### Split by Dependency Direction

Let the type graph point the way: types that cross boundaries go in a contract module; implementations import the contract; nothing imports implementations from contracts. In a node/backend codebase that means roughly: `domain` (pure types and rules) → `application` (use cases) → `infrastructure` (adapters), with dependencies pointing only inward.

### Dependencies and Build

#### Diagnose, Then Add Dependencies

Prefer built-in `Array`, `Map`, `Promise`, and `Intl` over pulling in utilities for every small operation. A tiny inline function beats a dependency that must be upgraded, audited, and kept compatible. (The Go idiom "a little copying is better than a little dependency" applies to TypeScript too.)

#### Runtime Validation, Not Type-of-Trust

Schemas that validate at runtime (Zod, validators, or hand-written guards) are the bridge between untrusted data and compile-time types. Library approaches differ (Zod and other schema-first libraries derive the type from the schema; validators in some ecosystem patterns are type-first with the runtime check derived). Pick one model and be consistent across the codebase.

#### Keep the Compiler Incremental and Fast

Large codebases benefit from `composite: true` with project references, an `incremental` build cache, and `moduleResolution: bundler` where the bundler supports it. Slow type-checking is a workflow problem that pushes developers off the type system — invest in narrowing the checked surface over relaxing it.

### Performance

#### Types Are Free, Structures Are Not

Type-level gymnastics (mapped types, conditional types, template literal types) cost nothing at runtime but can cost a lot of developer clarity. Keep complex type machinery inside boundary modules; do not export type circus acts as the public API.

#### Avoid Unnecessary Object Renaming

Copying and spreading large nested objects repeatedly has real cost in hot paths. Prefer immutable updates with spread at the point of change, but avoid defensive re-copying of unchanged structures (for example, in render paths or per-message handlers).

#### Memoize Idempotent Computation

Pure, expensive derivations belong behind a cache if they repeat with the same inputs. Use `Map`-based caches with explicit lifetime instead of ad-hoc global caches that never clear.

### Type-Level Testing

#### Assert the Types, Not Just the Runtime

Behavior tests prove runtime behavior; dedicated type tests lock in the public API contract. A type that silently loosens is a regression.

```typescript
import { expectTypeOf } from 'vitest'

expectTypeOf<Result<User, ValidationIssue[]>>().toEqualTypeOf<
  | { ok: true; value: User }
  | { ok: false; error: ValidationIssue[] }
>()
```

#### Use `satisfies` to Preserve Intent

`satisfies` checks a value against a shape without widening it to that shape — the ideal way to keep literal types while still validating structure.

```typescript
const statusByAction = {
  new: 'open',
  reopen: 'open',
  close: 'closed'
} as const satisfies Record<Action, Status>
```

### TypeScript Tooling Integration

#### Essential Commands

```bash
# Type-check the whole project
npx tsc --noEmit

# Watch mode for fast feedback
npx tsc --noEmit --watch

# Run tests (Vitest)
npx vitest run

# Lint with types-aware rules (typescript-eslint)
npx eslint .

# Formatting
npx prettier --write .
```

#### Recommended Linter Baseline

The `typescript-eslint` recommended-type-checked ruleset is the practical default: it promotes `no-unsafe-assignment`, `no-unsafe-member-access`, `no-unsafe-argument`, and `no-unsafe-call` from style noise to compiler-like guarantees. Keep the type-aware config; if it is slow, that is a project-structure signal, not a reason to disable it.

### Anti-Patterns to Avoid

- **`any` as a speed hack** — it converts the compiler's proof into a runtime guess. Reach for `unknown` + narrowing instead.
- **`as` casts that lie** — a cast that bypasses a check you did not actually perform is where null-pointer and shape bugs are born. Validate, then cast, and keep the cast inside the module that validates.
- **Deeply nested callbacks / promise chains** — prefer async/await; flat code is narrowable code.
- **`enum` coercion bugs** — string-literal unions give you the same safety without runtime artifacts or reverse-mapping footguns.
- **Giant god types** — a single interface that models several unrelated shapes should be a discriminated union or several interfaces.
- **Optional-only option objects** — `allOptional` config types silently swallow typos at the call site; prefer required fields for the ones the function genuinely depends on.
- **Silent catch** — `catch {}` or `catch (e) { /* nothing */ }` hides failures the caller assumed were handled.
- **Mixing sync and async error paths** — an `async` function always surfaces throws as rejections, even before the first `await`. Only a non-`async` function returning a promise can throw synchronously (before returning it), forcing callers to handle two error shapes. Prefer `async` throughout so every failure is a rejection:

```typescript
async function asyncFails(): Promise<never> {
  throw new Error('becomes a rejection, never a sync throw')
}

function lazyFails(): Promise<never> {
  throw new Error('throws synchronously — needs try/catch AND .catch')
}
```

**Remember**: the type system is a proof tool, not a paperwork burden. When a type error resists a reasonable annotation, the design — not the compiler — is usually the thing to change. Prefer boring, explicit, well-scoped TypeScript over clever type engines.

### Related Skills

- `languages:typescript` (`references/frameworks/nestjs.md`) — NestJS architecture patterns for TypeScript backends (modules, controllers, providers, DTO validation)
- `languages:typescript` (`references/standards.md`) — React and Next.js component and state patterns
- TypeScript rules (`rules/typescript/`, installed as `rules/ecc/typescript/`) — the "what" and "when" this skill implements as the "how"
- `data:database-design` — database access patterns used in TypeScript applications

## Frontend Development Patterns

<!-- source: affaan-m/ECC pi/core/skills/frontend-patterns/SKILL.md -->

Modern frontend patterns for React, Next.js, and performant user interfaces.

### When to Activate

- Building React components (composition, props, rendering)
- Managing state (useState, useReducer, Zustand, Context)
- Implementing data fetching (SWR, React Query, server components)
- Optimizing performance (memoization, virtualization, code splitting)
- Working with forms (validation, controlled inputs, Zod schemas)
- Handling client-side routing and navigation
- Building accessible, responsive UI patterns

### Component Patterns

#### Composition Over Inheritance

```typescript
// PASS: GOOD: Component composition
interface CardProps {
  children: React.ReactNode
  variant?: 'default' | 'outlined'
}

export function Card({ children, variant = 'default' }: CardProps) {
  return <div className={`card card-${variant}`}>{children}</div>
}

export function CardHeader({ children }: { children: React.ReactNode }) {
  return <div className="card-header">{children}</div>
}

export function CardBody({ children }: { children: React.ReactNode }) {
  return <div className="card-body">{children}</div>
}

// Usage
<Card>
  <CardHeader>Title</CardHeader>
  <CardBody>Content</CardBody>
</Card>
```

#### Compound Components

```typescript
interface TabsContextValue {
  activeTab: string
  setActiveTab: (tab: string) => void
}

const TabsContext = createContext<TabsContextValue | undefined>(undefined)

export function Tabs({ children, defaultTab }: {
  children: React.ReactNode
  defaultTab: string
}) {
  const [activeTab, setActiveTab] = useState(defaultTab)

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      {children}
    </TabsContext.Provider>
  )
}

export function TabList({ children }: { children: React.ReactNode }) {
  return <div className="tab-list">{children}</div>
}

export function Tab({ id, children }: { id: string, children: React.ReactNode }) {
  const context = useContext(TabsContext)
  if (!context) throw new Error('Tab must be used within Tabs')

  return (
    <button
      className={context.activeTab === id ? 'active' : ''}
      onClick={() => context.setActiveTab(id)}
    >
      {children}
    </button>
  )
}

// Usage
<Tabs defaultTab="overview">
  <TabList>
    <Tab id="overview">Overview</Tab>
    <Tab id="details">Details</Tab>
  </TabList>
</Tabs>
```

#### Render Props Pattern

```typescript
interface DataLoaderProps<T> {
  url: string
  children: (data: T | null, loading: boolean, error: Error | null) => React.ReactNode
}

export function DataLoader<T>({ url, children }: DataLoaderProps<T>) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    fetch(url)
      .then(res => res.json())
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false))
  }, [url])

  return <>{children(data, loading, error)}</>
}

// Usage
<DataLoader<Market[]> url="/api/markets">
  {(markets, loading, error) => {
    if (loading) return <Spinner />
    if (error) return <Error error={error} />
    return <MarketList markets={markets!} />
  }}
</DataLoader>
```

### Custom Hooks Patterns

#### State Management Hook

```typescript
export function useToggle(initialValue = false): [boolean, () => void] {
  const [value, setValue] = useState(initialValue)

  const toggle = useCallback(() => {
    setValue(v => !v)
  }, [])

  return [value, toggle]
}

// Usage
const [isOpen, toggleOpen] = useToggle()
```

#### Async Data Fetching Hook

```typescript
interface UseQueryOptions<T> {
  onSuccess?: (data: T) => void
  onError?: (error: Error) => void
  enabled?: boolean
}

export function useQuery<T>(
  key: string,
  fetcher: () => Promise<T>,
  options?: UseQueryOptions<T>
) {
  const [data, setData] = useState<T | null>(null)
  const [error, setError] = useState<Error | null>(null)
  const [loading, setLoading] = useState(false)

  // Keep the latest fetcher/options in refs so refetch stays referentially
  // stable even when callers pass inline functions and object literals.
  // Without this, every render creates a new refetch, and the effect below
  // re-runs after each state update - an infinite fetch loop.
  const fetcherRef = useRef(fetcher)
  const optionsRef = useRef(options)
  useEffect(() => {
    fetcherRef.current = fetcher
    optionsRef.current = options
  })

  const refetch = useCallback(async () => {
    setLoading(true)
    setError(null)

    try {
      const result = await fetcherRef.current()
      setData(result)
      optionsRef.current?.onSuccess?.(result)
    } catch (err) {
      const error = err as Error
      setError(error)
      optionsRef.current?.onError?.(error)
    } finally {
      setLoading(false)
    }
  }, [])

  const enabled = options?.enabled !== false

  useEffect(() => {
    if (enabled) {
      refetch()
    }
  }, [key, enabled, refetch])

  return { data, error, loading, refetch }
}

// Usage
const { data: markets, loading, error, refetch } = useQuery(
  'markets',
  () => fetch('/api/markets').then(r => r.json()),
  {
    onSuccess: data => console.log('Fetched', data.length, 'markets'),
    onError: err => console.error('Failed:', err)
  }
)
```

#### Debounce Hook

```typescript
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => clearTimeout(handler)
  }, [value, delay])

  return debouncedValue
}

// Usage
const [searchQuery, setSearchQuery] = useState('')
const debouncedQuery = useDebounce(searchQuery, 500)

useEffect(() => {
  if (debouncedQuery) {
    performSearch(debouncedQuery)
  }
}, [debouncedQuery])
```

### State Management Patterns

#### Context + Reducer Pattern

```typescript
interface State {
  markets: Market[]
  selectedMarket: Market | null
  loading: boolean
}

type Action =
  | { type: 'SET_MARKETS'; payload: Market[] }
  | { type: 'SELECT_MARKET'; payload: Market }
  | { type: 'SET_LOADING'; payload: boolean }

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'SET_MARKETS':
      return { ...state, markets: action.payload }
    case 'SELECT_MARKET':
      return { ...state, selectedMarket: action.payload }
    case 'SET_LOADING':
      return { ...state, loading: action.payload }
    default:
      return state
  }
}

const MarketContext = createContext<{
  state: State
  dispatch: Dispatch<Action>
} | undefined>(undefined)

export function MarketProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(reducer, {
    markets: [],
    selectedMarket: null,
    loading: false
  })

  return (
    <MarketContext.Provider value={{ state, dispatch }}>
      {children}
    </MarketContext.Provider>
  )
}

export function useMarkets() {
  const context = useContext(MarketContext)
  if (!context) throw new Error('useMarkets must be used within MarketProvider')
  return context
}
```

### Performance Optimization

#### Memoization

```typescript
// PASS: useMemo for expensive computations
// Copy before sorting - Array.prototype.sort mutates in place
const sortedMarkets = useMemo(() => {
  return [...markets].sort((a, b) => b.volume - a.volume)
}, [markets])

// PASS: useCallback for functions passed to children
const handleSearch = useCallback((query: string) => {
  setSearchQuery(query)
}, [])

// PASS: React.memo for pure components
export const MarketCard = React.memo<MarketCardProps>(({ market }) => {
  return (
    <div className="market-card">
      <h3>{market.name}</h3>
      <p>{market.description}</p>
    </div>
  )
})
```

#### Code Splitting & Lazy Loading

```typescript
import { lazy, Suspense } from 'react'

// PASS: Lazy load heavy components
const HeavyChart = lazy(() => import('./HeavyChart'))
const ThreeJsBackground = lazy(() => import('./ThreeJsBackground'))

export function Dashboard() {
  return (
    <div>
      <Suspense fallback={<ChartSkeleton />}>
        <HeavyChart data={data} />
      </Suspense>

      <Suspense fallback={null}>
        <ThreeJsBackground />
      </Suspense>
    </div>
  )
}
```

#### Virtualization for Long Lists

```typescript
import { useVirtualizer } from '@tanstack/react-virtual'

export function VirtualMarketList({ markets }: { markets: Market[] }) {
  const parentRef = useRef<HTMLDivElement>(null)

  const virtualizer = useVirtualizer({
    count: markets.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 100,  // Estimated row height
    overscan: 5  // Extra items to render
  })

  return (
    <div ref={parentRef} style={{ height: '600px', overflow: 'auto' }}>
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          position: 'relative'
        }}
      >
        {virtualizer.getVirtualItems().map(virtualRow => (
          <div
            key={virtualRow.index}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualRow.size}px`,
              transform: `translateY(${virtualRow.start}px)`
            }}
          >
            <MarketCard market={markets[virtualRow.index]} />
          </div>
        ))}
      </div>
    </div>
  )
}
```

### Form Handling Patterns

#### Controlled Form with Validation

```typescript
interface FormData {
  name: string
  description: string
  endDate: string
}

interface FormErrors {
  name?: string
  description?: string
  endDate?: string
}

export function CreateMarketForm() {
  const [formData, setFormData] = useState<FormData>({
    name: '',
    description: '',
    endDate: ''
  })

  const [errors, setErrors] = useState<FormErrors>({})

  const validate = (): boolean => {
    const newErrors: FormErrors = {}

    if (!formData.name.trim()) {
      newErrors.name = 'Name is required'
    } else if (formData.name.length > 200) {
      newErrors.name = 'Name must be under 200 characters'
    }

    if (!formData.description.trim()) {
      newErrors.description = 'Description is required'
    }

    if (!formData.endDate) {
      newErrors.endDate = 'End date is required'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!validate()) return

    try {
      await createMarket(formData)
      // Success handling
    } catch (error) {
      // Error handling
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={formData.name}
        onChange={e => setFormData(prev => ({ ...prev, name: e.target.value }))}
        placeholder="Market name"
      />
      {errors.name && <span className="error">{errors.name}</span>}

      {/* Other fields */}

      <button type="submit">Create Market</button>
    </form>
  )
}
```

### Error Boundary Pattern

```typescript
interface ErrorBoundaryState {
  hasError: boolean
  error: Error | null
}

export class ErrorBoundary extends React.Component<
  { children: React.ReactNode },
  ErrorBoundaryState
> {
  state: ErrorBoundaryState = {
    hasError: false,
    error: null
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error boundary caught:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-fallback">
          <h2>Something went wrong</h2>
          <p>{this.state.error?.message}</p>
          <button onClick={() => this.setState({ hasError: false })}>
            Try again
          </button>
        </div>
      )
    }

    return this.props.children
  }
}

// Usage
<ErrorBoundary>
  <App />
</ErrorBoundary>
```

### Animation Patterns

#### Framer Motion Animations

```typescript
import { motion, AnimatePresence } from 'framer-motion'

// PASS: List animations
export function AnimatedMarketList({ markets }: { markets: Market[] }) {
  return (
    <AnimatePresence>
      {markets.map(market => (
        <motion.div
          key={market.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.3 }}
        >
          <MarketCard market={market} />
        </motion.div>
      ))}
    </AnimatePresence>
  )
}

// PASS: Modal animations
export function Modal({ isOpen, onClose, children }: ModalProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            className="modal-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />
          <motion.div
            className="modal-content"
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
          >
            {children}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
```

### Accessibility Patterns

#### Keyboard Navigation

```typescript
export function Dropdown({ options, onSelect }: DropdownProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [activeIndex, setActiveIndex] = useState(0)

  const handleKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault()
        setActiveIndex(i => Math.min(i + 1, options.length - 1))
        break
      case 'ArrowUp':
        e.preventDefault()
        setActiveIndex(i => Math.max(i - 1, 0))
        break
      case 'Enter':
        e.preventDefault()
        onSelect(options[activeIndex])
        setIsOpen(false)
        break
      case 'Escape':
        setIsOpen(false)
        break
    }
  }

  return (
    <div
      role="combobox"
      aria-expanded={isOpen}
      aria-haspopup="listbox"
      onKeyDown={handleKeyDown}
    >
      {/* Dropdown implementation */}
    </div>
  )
}
```

#### Focus Management

```typescript
export function Modal({ isOpen, onClose, children }: ModalProps) {
  const modalRef = useRef<HTMLDivElement>(null)
  const previousFocusRef = useRef<HTMLElement | null>(null)

  useEffect(() => {
    if (isOpen) {
      // Save currently focused element
      previousFocusRef.current = document.activeElement as HTMLElement

      // Focus modal
      modalRef.current?.focus()
    } else {
      // Restore focus when closing
      previousFocusRef.current?.focus()
    }
  }, [isOpen])

  return isOpen ? (
    <div
      ref={modalRef}
      role="dialog"
      aria-modal="true"
      tabIndex={-1}
      onKeyDown={e => e.key === 'Escape' && onClose()}
    >
      {children}
    </div>
  ) : null
}
```

**Remember**: Modern frontend patterns enable maintainable, performant user interfaces. Choose patterns that fit your project complexity.

## Web Coding Style

<!-- source: affaan-m/ECC rules/web/coding-style.md -->

> This file extends common/coding-style.md with web-specific frontend content.



### File Organization

Organize by feature or surface area, not by file type:

```text
src/
├── components/
│   ├── hero/
│   │   ├── Hero.tsx
│   │   ├── HeroVisual.tsx
│   │   └── hero.css
│   ├── scrolly-section/
│   │   ├── ScrollySection.tsx
│   │   ├── StickyVisual.tsx
│   │   └── scrolly.css
│   └── ui/
│       ├── Button.tsx
│       ├── SurfaceCard.tsx
│       └── AnimatedText.tsx
├── hooks/
│   ├── useReducedMotion.ts
│   └── useScrollProgress.ts
├── lib/
│   ├── animation.ts
│   └── color.ts
└── styles/
    ├── tokens.css
    ├── typography.css
    └── global.css
```

### CSS Custom Properties

Define design tokens as variables. Do not hardcode palette, typography, or spacing repeatedly:

```css
:root {
  --color-surface: oklch(98% 0 0);
  --color-text: oklch(18% 0 0);
  --color-accent: oklch(68% 0.21 250);

  --text-base: clamp(1rem, 0.92rem + 0.4vw, 1.125rem);
  --text-hero: clamp(3rem, 1rem + 7vw, 8rem);

  --space-section: clamp(4rem, 3rem + 5vw, 10rem);

  --duration-fast: 150ms;
  --duration-normal: 300ms;
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
}
```

### Animation-Only Properties

Prefer compositor-friendly motion:
- `transform`
- `opacity`
- `clip-path`
- `filter` (sparingly)

Avoid animating layout-bound properties:
- `width`
- `height`
- `top`
- `left`
- `margin`
- `padding`
- `border`
- `font-size`

### Semantic HTML First

```html
<header>
  <nav aria-label="Main navigation">...</nav>
</header>
<main>
  <section aria-labelledby="hero-heading">
    <h1 id="hero-heading">...</h1>
  </section>
</main>
<footer>...</footer>
```

Do not reach for generic wrapper `div` stacks when a semantic element exists.

### Naming

- Components: PascalCase (`ScrollySection`, `SurfaceCard`)
- Hooks: `use` prefix (`useReducedMotion`)
- CSS classes: kebab-case or utility classes
- Animation timelines: camelCase with intent (`heroRevealTl`)

## Web Patterns

<!-- source: affaan-m/ECC rules/web/patterns.md -->

> This file extends common/patterns.md with web-specific patterns.



### Component Composition

#### Compound Components

Use compound components when related UI shares state and interaction semantics:

```tsx
<Tabs defaultValue="overview">
  <Tabs.List>
    <Tabs.Trigger value="overview">Overview</Tabs.Trigger>
    <Tabs.Trigger value="settings">Settings</Tabs.Trigger>
  </Tabs.List>
  <Tabs.Content value="overview">...</Tabs.Content>
  <Tabs.Content value="settings">...</Tabs.Content>
</Tabs>
```

- Parent owns state
- Children consume via context
- Prefer this over prop drilling for complex widgets

#### Render Props / Slots

- Use render props or slot patterns when behavior is shared but markup must vary
- Keep keyboard handling, ARIA, and focus logic in the headless layer

#### Container / Presentational Split

- Container components own data loading and side effects
- Presentational components receive props and render UI
- Presentational components should stay pure

### State Management

Treat these separately:

| Concern | Tooling |
|---------|---------|
| Server state | TanStack Query, SWR, tRPC |
| Client state | Zustand, Jotai, signals |
| URL state | search params, route segments |
| Form state | React Hook Form or equivalent |

- Do not duplicate server state into client stores
- Derive values instead of storing redundant computed state

### URL As State

Persist shareable state in the URL:
- filters
- sort order
- pagination
- active tab
- search query

### Data Fetching

#### Stale-While-Revalidate

- Return cached data immediately
- Revalidate in the background
- Prefer existing libraries instead of rolling this by hand

#### Optimistic Updates

- Snapshot current state
- Apply optimistic update
- Roll back on failure
- Emit visible error feedback when rolling back

#### Parallel Loading

- Fetch independent data in parallel
- Avoid parent-child request waterfalls
- Prefetch likely next routes or states when justified

## Web Performance Rules

<!-- source: affaan-m/ECC rules/web/performance.md -->

> This file extends common/performance.md with web-specific performance content.



### Core Web Vitals Targets

| Metric | Target |
|--------|--------|
| LCP | < 2.5s |
| INP | < 200ms |
| CLS | < 0.1 |
| FCP | < 1.5s |
| TBT | < 200ms |

### Bundle Budget

| Page Type | JS Budget (gzipped) | CSS Budget |
|-----------|---------------------|------------|
| Landing page | < 150kb | < 30kb |
| App page | < 300kb | < 50kb |
| Microsite | < 80kb | < 15kb |

### Loading Strategy

1. Inline critical above-the-fold CSS where justified
2. Preload the hero image and primary font only
3. Defer non-critical CSS or JS
4. Dynamically import heavy libraries

```js
const gsapModule = await import('gsap');
const { ScrollTrigger } = await import('gsap/ScrollTrigger');
```

### Image Optimization

- Explicit `width` and `height`
- `loading="eager"` plus `fetchpriority="high"` for hero media only
- `loading="lazy"` for below-the-fold assets
- Prefer AVIF or WebP with fallbacks
- Never ship source images far beyond rendered size

### Font Loading

- Max two font families unless there is a clear exception
- `font-display: swap`
- Subset where possible
- Preload only the truly critical weight/style

### Animation Performance

- Animate compositor-friendly properties only
- Use `will-change` narrowly and remove it when done
- Prefer CSS for simple transitions
- Use `requestAnimationFrame` or established animation libraries for JS motion
- Avoid scroll handler churn; use IntersectionObserver or well-behaved libraries

### Performance Checklist

- [ ] All images have explicit dimensions
- [ ] No accidental render-blocking resources
- [ ] No layout shifts from dynamic content
- [ ] Motion stays on compositor-friendly properties
- [ ] Third-party scripts load async/defer and only when needed
