# Rust — Standards and idioms

Part of `languages:rust`. Load when writing or refactoring code: style, idioms, patterns, project layout.

## Rust Coding Style

<!-- source: affaan-m/ECC rules/rust/coding-style.md -->

> This file extends common/coding-style.md with Rust-specific content.

### Formatting

- **rustfmt** for enforcement — always run `cargo fmt` before committing
- **clippy** for lints — `cargo clippy -- -D warnings` (treat warnings as errors)
- 4-space indent (rustfmt default)
- Max line width: 100 characters (rustfmt default)

### Immutability

Rust variables are immutable by default — embrace this:

- Use `let` by default; only use `let mut` when mutation is required
- Prefer returning new values over mutating in place
- Use `Cow<'_, T>` when a function may or may not need to allocate

```rust
use std::borrow::Cow;

// GOOD — immutable by default, new value returned
fn normalize(input: &str) -> Cow<'_, str> {
    if input.contains(' ') {
        Cow::Owned(input.replace(' ', "_"))
    } else {
        Cow::Borrowed(input)
    }
}

// BAD — unnecessary mutation
fn normalize_bad(input: &mut String) {
    *input = input.replace(' ', "_");
}
```

### Naming

Follow standard Rust conventions:
- `snake_case` for functions, methods, variables, modules, crates
- `PascalCase` (UpperCamelCase) for types, traits, enums, type parameters
- `SCREAMING_SNAKE_CASE` for constants and statics
- Lifetimes: short lowercase (`'a`, `'de`) — descriptive names for complex cases (`'input`)

### Ownership and Borrowing

- Borrow (`&T`) by default; take ownership only when you need to store or consume
- Never clone to satisfy the borrow checker without understanding the root cause
- Accept `&str` over `String`, `&[T]` over `Vec<T>` in function parameters
- Use `impl Into<String>` for constructors that need to own a `String`

```rust
// GOOD — borrows when ownership isn't needed
fn word_count(text: &str) -> usize {
    text.split_whitespace().count()
}

// GOOD — takes ownership in constructor via Into
fn new(name: impl Into<String>) -> Self {
    Self { name: name.into() }
}

// BAD — takes String when &str suffices
fn word_count_bad(text: String) -> usize {
    text.split_whitespace().count()
}
```

### Error Handling

- Use `Result<T, E>` and `?` for propagation — never `unwrap()` in production code
- **Libraries**: define typed errors with `thiserror`
- **Applications**: use `anyhow` for flexible error context
- Add context with `.with_context(|| format!("failed to ..."))?`
- Reserve `unwrap()` / `expect()` for tests and truly unreachable states

```rust
// GOOD — library error with thiserror
#[derive(Debug, thiserror::Error)]
pub enum ConfigError {
    #[error("failed to read config: {0}")]
    Io(#[from] std::io::Error),
    #[error("invalid config format: {0}")]
    Parse(String),
}

// GOOD — application error with anyhow
use anyhow::Context;

fn load_config(path: &str) -> anyhow::Result<Config> {
    let content = std::fs::read_to_string(path)
        .with_context(|| format!("failed to read {path}"))?;
    toml::from_str(&content)
        .with_context(|| format!("failed to parse {path}"))
}
```

### Iterators Over Loops

Prefer iterator chains for transformations; use loops for complex control flow:

```rust
// GOOD — declarative and composable
let active_emails: Vec<&str> = users.iter()
    .filter(|u| u.is_active)
    .map(|u| u.email.as_str())
    .collect();

// GOOD — loop for complex logic with early returns
for user in &users {
    if let Some(verified) = verify_email(&user.email)? {
        send_welcome(&verified)?;
    }
}
```

### Module Organization

Organize by domain, not by type:

```text
src/
├── main.rs
├── lib.rs
├── auth/           # Domain module
│   ├── mod.rs
│   ├── token.rs
│   └── middleware.rs
├── orders/         # Domain module
│   ├── mod.rs
│   ├── model.rs
│   └── service.rs
└── db/             # Infrastructure
    ├── mod.rs
    └── pool.rs
```

### Visibility

- Default to private; use `pub(crate)` for internal sharing
- Only mark `pub` what is part of the crate's public API
- Re-export public API from `lib.rs`

### References

See skill: `languages:rust` (`references/standards.md`) for comprehensive Rust idioms and patterns.

## Rust Patterns

<!-- source: affaan-m/ECC rules/rust/patterns.md -->

> This file extends common/patterns.md with Rust-specific content.

### Repository Pattern with Traits

Encapsulate data access behind a trait:

```rust
pub trait OrderRepository: Send + Sync {
    fn find_by_id(&self, id: u64) -> Result<Option<Order>, StorageError>;
    fn find_all(&self) -> Result<Vec<Order>, StorageError>;
    fn save(&self, order: &Order) -> Result<Order, StorageError>;
    fn delete(&self, id: u64) -> Result<(), StorageError>;
}
```

Concrete implementations handle storage details (Postgres, SQLite, in-memory for tests).

### Service Layer

Business logic in service structs; inject dependencies via constructor:

```rust
pub struct OrderService {
    repo: Box<dyn OrderRepository>,
    payment: Box<dyn PaymentGateway>,
}

impl OrderService {
    pub fn new(repo: Box<dyn OrderRepository>, payment: Box<dyn PaymentGateway>) -> Self {
        Self { repo, payment }
    }

    pub fn place_order(&self, request: CreateOrderRequest) -> anyhow::Result<OrderSummary> {
        let order = Order::from(request);
        self.payment.charge(order.total())?;
        let saved = self.repo.save(&order)?;
        Ok(OrderSummary::from(saved))
    }
}
```

### Newtype Pattern for Type Safety

Prevent argument mix-ups with distinct wrapper types:

```rust
struct UserId(u64);
struct OrderId(u64);

fn get_order(user: UserId, order: OrderId) -> anyhow::Result<Order> {
    // Can't accidentally swap user and order IDs at call sites
    todo!()
}
```

### Enum State Machines

Model states as enums — make illegal states unrepresentable:

```rust
enum ConnectionState {
    Disconnected,
    Connecting { attempt: u32 },
    Connected { session_id: String },
    Failed { reason: String, retries: u32 },
}

fn handle(state: &ConnectionState) {
    match state {
        ConnectionState::Disconnected => connect(),
        ConnectionState::Connecting { attempt } if *attempt > 3 => abort(),
        ConnectionState::Connecting { .. } => wait(),
        ConnectionState::Connected { session_id } => use_session(session_id),
        ConnectionState::Failed { retries, .. } if *retries < 5 => retry(),
        ConnectionState::Failed { reason, .. } => log_failure(reason),
    }
}
```

Always match exhaustively — no wildcard `_` for business-critical enums.

### Builder Pattern

Use for structs with many optional parameters:

```rust
pub struct ServerConfig {
    host: String,
    port: u16,
    max_connections: usize,
}

impl ServerConfig {
    pub fn builder(host: impl Into<String>, port: u16) -> ServerConfigBuilder {
        ServerConfigBuilder {
            host: host.into(),
            port,
            max_connections: 100,
        }
    }
}

pub struct ServerConfigBuilder {
    host: String,
    port: u16,
    max_connections: usize,
}

impl ServerConfigBuilder {
    pub fn max_connections(mut self, n: usize) -> Self {
        self.max_connections = n;
        self
    }

    pub fn build(self) -> ServerConfig {
        ServerConfig {
            host: self.host,
            port: self.port,
            max_connections: self.max_connections,
        }
    }
}
```

### Sealed Traits for Extensibility Control

Use a private module to seal a trait, preventing external implementations:

```rust
mod private {
    pub trait Sealed {}
}

pub trait Format: private::Sealed {
    fn encode(&self, data: &[u8]) -> Vec<u8>;
}

pub struct Json;
impl private::Sealed for Json {}
impl Format for Json {
    fn encode(&self, data: &[u8]) -> Vec<u8> { todo!() }
}
```

### API Response Envelope

Consistent API responses using a generic enum:

```rust
#[derive(Debug, serde::Serialize)]
#[serde(tag = "status")]
pub enum ApiResponse<T: serde::Serialize> {
    #[serde(rename = "ok")]
    Ok { data: T },
    #[serde(rename = "error")]
    Error { message: String },
}
```

### References

See skill: `languages:rust` (`references/standards.md`) for comprehensive patterns including ownership, traits, generics, concurrency, and async.

## Rust Development Patterns

<!-- source: affaan-m/ECC pi/core/skills/rust-patterns/SKILL.md -->

Idiomatic Rust patterns and best practices for building safe, performant, and maintainable applications.

### When to Use

- Writing new Rust code
- Reviewing Rust code
- Refactoring existing Rust code
- Designing crate structure and module layout

### How It Works

This skill enforces idiomatic Rust conventions across six key areas: ownership and borrowing to prevent data races at compile time, `Result`/`?` error propagation with `thiserror` for libraries and `anyhow` for applications, enums and exhaustive pattern matching to make illegal states unrepresentable, traits and generics for zero-cost abstraction, safe concurrency via `Arc<Mutex<T>>`, channels, and async/await, and minimal `pub` surfaces organized by domain.

### Core Principles

#### 1. Ownership and Borrowing

Rust's ownership system prevents data races and memory bugs at compile time.

```rust
// Good: Pass references when you don't need ownership
fn process(data: &[u8]) -> usize {
    data.len()
}

// Good: Take ownership only when you need to store or consume
fn store(data: Vec<u8>) -> Record {
    Record { payload: data }
}

// Bad: Cloning unnecessarily to avoid borrow checker
fn process_bad(data: &Vec<u8>) -> usize {
    let cloned = data.clone(); // Wasteful — just borrow
    cloned.len()
}
```

#### Use `Cow` for Flexible Ownership

```rust
use std::borrow::Cow;

fn normalize(input: &str) -> Cow<'_, str> {
    if input.contains(' ') {
        Cow::Owned(input.replace(' ', "_"))
    } else {
        Cow::Borrowed(input) // Zero-cost when no mutation needed
    }
}
```

### Error Handling

#### Use `Result` and `?` — Never `unwrap()` in Production

```rust
// Good: Propagate errors with context
use anyhow::{Context, Result};

fn load_config(path: &str) -> Result<Config> {
    let content = std::fs::read_to_string(path)
        .with_context(|| format!("failed to read config from {path}"))?;
    let config: Config = toml::from_str(&content)
        .with_context(|| format!("failed to parse config from {path}"))?;
    Ok(config)
}

// Bad: Panics on error
fn load_config_bad(path: &str) -> Config {
    let content = std::fs::read_to_string(path).unwrap(); // Panics!
    toml::from_str(&content).unwrap()
}
```

#### Library Errors with `thiserror`, Application Errors with `anyhow`

```rust
// Library code: structured, typed errors
use thiserror::Error;

#[derive(Debug, Error)]
pub enum StorageError {
    #[error("record not found: {id}")]
    NotFound { id: String },
    #[error("connection failed")]
    Connection(#[from] std::io::Error),
    #[error("invalid data: {0}")]
    InvalidData(String),
}

// Application code: flexible error handling
use anyhow::{bail, Result};

fn run() -> Result<()> {
    let config = load_config("app.toml")?;
    if config.workers == 0 {
        bail!("worker count must be > 0");
    }
    Ok(())
}
```

#### `Option` Combinators Over Nested Matching

```rust
// Good: Combinator chain
fn find_user_email(users: &[User], id: u64) -> Option<String> {
    users.iter()
        .find(|u| u.id == id)
        .map(|u| u.email.clone())
}

// Bad: Deeply nested matching
fn find_user_email_bad(users: &[User], id: u64) -> Option<String> {
    match users.iter().find(|u| u.id == id) {
        Some(user) => match &user.email {
            email => Some(email.clone()),
        },
        None => None,
    }
}
```

### Enums and Pattern Matching

#### Model States as Enums

```rust
// Good: Impossible states are unrepresentable
enum ConnectionState {
    Disconnected,
    Connecting { attempt: u32 },
    Connected { session_id: String },
    Failed { reason: String, retries: u32 },
}

fn handle(state: &ConnectionState) {
    match state {
        ConnectionState::Disconnected => connect(),
        ConnectionState::Connecting { attempt } if *attempt > 3 => abort(),
        ConnectionState::Connecting { .. } => wait(),
        ConnectionState::Connected { session_id } => use_session(session_id),
        ConnectionState::Failed { retries, .. } if *retries < 5 => retry(),
        ConnectionState::Failed { reason, .. } => log_failure(reason),
    }
}
```

#### Exhaustive Matching — No Catch-All for Business Logic

```rust
// Good: Handle every variant explicitly
match command {
    Command::Start => start_service(),
    Command::Stop => stop_service(),
    Command::Restart => restart_service(),
    // Adding a new variant forces handling here
}

// Bad: Wildcard hides new variants
match command {
    Command::Start => start_service(),
    _ => {} // Silently ignores Stop, Restart, and future variants
}
```

### Traits and Generics

#### Accept Generics, Return Concrete Types

```rust
// Good: Generic input, concrete output
fn read_all(reader: &mut impl Read) -> std::io::Result<Vec<u8>> {
    let mut buf = Vec::new();
    reader.read_to_end(&mut buf)?;
    Ok(buf)
}

// Good: Trait bounds for multiple constraints
fn process<T: Display + Send + 'static>(item: T) -> String {
    format!("processed: {item}")
}
```

#### Trait Objects for Dynamic Dispatch

```rust
// Use when you need heterogeneous collections or plugin systems
trait Handler: Send + Sync {
    fn handle(&self, request: &Request) -> Response;
}

struct Router {
    handlers: Vec<Box<dyn Handler>>,
}

// Use generics when you need performance (monomorphization)
fn fast_process<H: Handler>(handler: &H, request: &Request) -> Response {
    handler.handle(request)
}
```

#### Newtype Pattern for Type Safety

```rust
// Good: Distinct types prevent mixing up arguments
struct UserId(u64);
struct OrderId(u64);

fn get_order(user: UserId, order: OrderId) -> Result<Order> {
    // Can't accidentally swap user and order IDs
    todo!()
}

// Bad: Easy to swap arguments
fn get_order_bad(user_id: u64, order_id: u64) -> Result<Order> {
    todo!()
}
```

### Structs and Data Modeling

#### Builder Pattern for Complex Construction

```rust
struct ServerConfig {
    host: String,
    port: u16,
    max_connections: usize,
}

impl ServerConfig {
    fn builder(host: impl Into<String>, port: u16) -> ServerConfigBuilder {
        ServerConfigBuilder { host: host.into(), port, max_connections: 100 }
    }
}

struct ServerConfigBuilder { host: String, port: u16, max_connections: usize }

impl ServerConfigBuilder {
    fn max_connections(mut self, n: usize) -> Self { self.max_connections = n; self }
    fn build(self) -> ServerConfig {
        ServerConfig { host: self.host, port: self.port, max_connections: self.max_connections }
    }
}

// Usage: ServerConfig::builder("localhost", 8080).max_connections(200).build()
```

### Iterators and Closures

#### Prefer Iterator Chains Over Manual Loops

```rust
// Good: Declarative, lazy, composable
let active_emails: Vec<String> = users.iter()
    .filter(|u| u.is_active)
    .map(|u| u.email.clone())
    .collect();

// Bad: Imperative accumulation
let mut active_emails = Vec::new();
for user in &users {
    if user.is_active {
        active_emails.push(user.email.clone());
    }
}
```

#### Use `collect()` with Type Annotation

```rust
// Collect into different types
let names: Vec<_> = items.iter().map(|i| &i.name).collect();
let lookup: HashMap<_, _> = items.iter().map(|i| (i.id, i)).collect();
let combined: String = parts.iter().copied().collect();

// Collect Results — short-circuits on first error
let parsed: Result<Vec<i32>, _> = strings.iter().map(|s| s.parse()).collect();
```

### Concurrency

#### `Arc<Mutex<T>>` for Shared Mutable State

```rust
use std::sync::{Arc, Mutex};

let counter = Arc::new(Mutex::new(0));
let handles: Vec<_> = (0..10).map(|_| {
    let counter = Arc::clone(&counter);
    std::thread::spawn(move || {
        let mut num = counter.lock().expect("mutex poisoned");
        *num += 1;
    })
}).collect();

for handle in handles {
    handle.join().expect("worker thread panicked");
}
```

#### Channels for Message Passing

```rust
use std::sync::mpsc;

let (tx, rx) = mpsc::sync_channel(16); // Bounded channel with backpressure

for i in 0..5 {
    let tx = tx.clone();
    std::thread::spawn(move || {
        tx.send(format!("message {i}")).expect("receiver disconnected");
    });
}
drop(tx); // Close sender so rx iterator terminates

for msg in rx {
    println!("{msg}");
}
```

#### Async with Tokio

```rust
use tokio::time::Duration;

async fn fetch_with_timeout(url: &str) -> Result<String> {
    let response = tokio::time::timeout(
        Duration::from_secs(5),
        reqwest::get(url),
    )
    .await
    .context("request timed out")?
    .context("request failed")?;

    response.text().await.context("failed to read body")
}

// Spawn concurrent tasks
async fn fetch_all(urls: Vec<String>) -> Vec<Result<String>> {
    let handles: Vec<_> = urls.into_iter()
        .map(|url| tokio::spawn(async move {
            fetch_with_timeout(&url).await
        }))
        .collect();

    let mut results = Vec::with_capacity(handles.len());
    for handle in handles {
        results.push(handle.await.unwrap_or_else(|e| panic!("spawned task panicked: {e}")));
    }
    results
}
```

### Unsafe Code

#### When Unsafe Is Acceptable

```rust
// Acceptable: FFI boundary with documented invariants (Rust 2024+)
/// # Safety
/// `ptr` must be a valid, aligned pointer to an initialized `Widget`.
unsafe fn widget_from_raw<'a>(ptr: *const Widget) -> &'a Widget {
    // SAFETY: caller guarantees ptr is valid and aligned
    unsafe { &*ptr }
}

// Acceptable: Performance-critical path with proof of correctness
// SAFETY: index is always < len due to the loop bound
unsafe { slice.get_unchecked(index) }
```

#### When Unsafe Is NOT Acceptable

```rust
// Bad: Using unsafe to bypass borrow checker
// Bad: Using unsafe for convenience
// Bad: Using unsafe without a Safety comment
// Bad: Transmuting between unrelated types
```

### Module System and Crate Structure

#### Organize by Domain, Not by Type

```text
my_app/
├── src/
│   ├── main.rs
│   ├── lib.rs
│   ├── auth/          # Domain module
│   │   ├── mod.rs
│   │   ├── token.rs
│   │   └── middleware.rs
│   ├── orders/        # Domain module
│   │   ├── mod.rs
│   │   ├── model.rs
│   │   └── service.rs
│   └── db/            # Infrastructure
│       ├── mod.rs
│       └── pool.rs
├── tests/             # Integration tests
├── benches/           # Benchmarks
└── Cargo.toml
```

#### Visibility — Expose Minimally

```rust
// Good: pub(crate) for internal sharing
pub(crate) fn validate_input(input: &str) -> bool {
    !input.is_empty()
}

// Good: Re-export public API from lib.rs
pub mod auth;
pub use auth::AuthMiddleware;

// Bad: Making everything pub
pub fn internal_helper() {} // Should be pub(crate) or private
```

### Tooling Integration

#### Essential Commands

```bash
# Build and check
cargo build
cargo check              # Fast type checking without codegen
cargo clippy             # Lints and suggestions
cargo fmt                # Format code

# Testing
cargo test
cargo test -- --nocapture    # Show println output
cargo test --lib             # Unit tests only
cargo test --test integration # Integration tests only

# Dependencies
cargo audit              # Security audit
cargo tree               # Dependency tree
cargo update             # Update dependencies

# Performance
cargo bench              # Run benchmarks
```

### Quick Reference: Rust Idioms

| Idiom | Description |
|-------|-------------|
| Borrow, don't clone | Pass `&T` instead of cloning unless ownership is needed |
| Make illegal states unrepresentable | Use enums to model valid states only |
| `?` over `unwrap()` | Propagate errors, never panic in library/production code |
| Parse, don't validate | Convert unstructured data to typed structs at the boundary |
| Newtype for type safety | Wrap primitives in newtypes to prevent argument swaps |
| Prefer iterators over loops | Declarative chains are clearer and often faster |
| `#[must_use]` on Results | Ensure callers handle return values |
| `Cow` for flexible ownership | Avoid allocations when borrowing suffices |
| Exhaustive matching | No wildcard `_` for business-critical enums |
| Minimal `pub` surface | Use `pub(crate)` for internal APIs |

### Anti-Patterns to Avoid

```rust
// Bad: .unwrap() in production code
let value = map.get("key").unwrap();

// Bad: .clone() to satisfy borrow checker without understanding why
let data = expensive_data.clone();
process(&original, &data);

// Bad: Using String when &str suffices
fn greet(name: String) { /* should be &str */ }

// Bad: Box<dyn Error> in libraries (use thiserror instead)
fn parse(input: &str) -> Result<Data, Box<dyn std::error::Error>> { todo!() }

// Bad: Ignoring must_use warnings
let _ = validate(input); // Silently discarding a Result

// Bad: Blocking in async context
async fn bad_async() {
    std::thread::sleep(Duration::from_secs(1)); // Blocks the executor!
    // Use: tokio::time::sleep(Duration::from_secs(1)).await;
}
```

**Remember**: If it compiles, it's probably correct — but only if you avoid `unwrap()`, minimize `unsafe`, and let the type system work for you.

## Rust Refactoring Specialist Agent

<!-- source: msitarzewski/agency-agents engineering/engineering-rust-refactoring-specialist.md -->

You are **Rust Refactoring Specialist**, a senior Rust systems engineer who reforms codebases through behavior-aware, evidence-based refactoring. You work across functions, types, traits, modules, crates, tests, manifests, documentation, and file layouts whenever the requested objective requires it.

Your defining rule is:

> Execute the complete, coherent change set required by the requested refactoring objective. There is no fixed limit on opportunities, files, symbols, or diff size. Avoid unrelated churn, not necessary breadth.

Rust has no classes. When someone refers to classes, interpret that as the relevant structs, enums, traits, implementations, or modules.

### 🎯 Your Core Mission

#### Audit the complete requested scope

- Inspect the entire declared scope when asked to audit, inventory, review, or list opportunities
- Report every credible, evidence-backed opportunity rather than stopping at an arbitrary top-N list
- State the crates, modules, files, features, targets, tests, generated code, and non-code references inspected
- Report coverage gaps for target-specific, feature-gated, macro-generated, external, or inaccessible code
- Keep independently actionable findings separate while clustering changes that must be implemented together

#### Implement coherent repository-scale refactors

- Complete every definition, caller, import, re-export, implementation, test, example, benchmark, document, and configuration update required by the objective
- Rename private and crate-private symbols and change their signatures when the new design is clearer and outward behavior remains correct
- Create, move, consolidate, split, or delete files and modules when doing so improves real cohesion, layering, discoverability, reuse, or testability
- Introduce shared helpers, types, or traits only when multiple real use cases or a clear domain boundary justify them
- Fix proven defects discovered inside the authorized scope and add regression coverage
- Continue through formatting, verification, and final diff review; a plan or partial edit is not completion

#### Preserve contracts deliberately

- Treat public API shape, errors, ordering, side effects, panic conditions, serialization, I/O, drop timing, lock scope, `.await` boundaries, and cancellation as observable behavior
- Preserve external compatibility unless the user explicitly authorizes a breaking change
- Separate structural evidence from measured performance claims
- Surface optional out-of-scope improvements instead of smuggling them into the refactor

### 🚨 Critical Rules You Must Follow

1. **No arbitrary refactor limit.** Semantic coherence, not file count or diff size, defines the boundary.
2. **No unrelated churn.** Every changed line must belong to the requested transformation.
3. **No silent public breakage.** Obtain authorization before changing externally reachable APIs, ABI, CLI, configuration, features, wire formats, serialization, or persistence contracts.
4. **No half-migrations.** Update definitions, references, tests, docs, module declarations, macros, build scripts, and string-based paths together.
5. **No unsafe shortcuts.** Never introduce `unsafe` to bypass ownership, borrowing, lifetime, or performance constraints.
6. **No test manipulation.** Never weaken, skip, or rewrite tests merely to accept changed behavior.
7. **No silent data loss.** Never replace an error with an empty value, default, sentinel, or ignored result unless the contract explicitly requires it.
8. **No speculative abstractions.** Do not add traits, generics, macros, dependencies, or design patterns merely to look idiomatic.
9. **No unsupported claims.** Claim speedups only after comparable measurement and never claim a command passed unless it ran successfully.
10. **No destructive Git operations.** Never discard user work, force-checkout, reset, clean, publish, or deploy without explicit authorization.
11. **No secret exposure.** Never print, copy, commit, or alter credentials discovered during inspection.
12. **No forced refactor.** If the existing design is clearer and safer, explain that conclusion and leave it intact.

Explicit authorization is also required for production dependency changes, toolchain or MSRV changes, lint-policy changes, existing `unsafe`, FFI, inline assembly, cryptography, authentication, and authorization code.

### 📋 Your Technical Deliverables

#### Refactoring opportunity inventory

Every audit finding includes:

```markdown
### RUST-007 — Ownership — Avoid repeated path allocation

- **Location**: `crates/config/src/loader.rs`, `load_workspace`
- **Evidence**: All four callers already retain a borrowed `&Path`, but the function
  accepts `PathBuf` and each caller clones before invocation.
- **End state**: Accept `&Path`; update all callers and tests.
- **Coupled changes**: `loader.rs`, `workspace.rs`, integration fixtures.
- **API/behavior impact**: Internal signature only; filesystem and error behavior unchanged.
- **Risk/value**: Low risk, medium value.
- **Verification**: Targeted loader tests, workspace check, Clippy, diff review.
```

Do not inflate inventories with style preferences or hypothetical optimizations.

#### Example 1: Safe internal rename plus ownership improvement

Before:

```rust
fn do_load(path: PathBuf) -> Result<Config, ConfigError> {
    let source = std::fs::read_to_string(path)?;
    parse_config(&source)
}

let config = do_load(options.config.clone())?;
```

After:

```rust
fn load_config(path: &Path) -> Result<Config, ConfigError> {
    let source = std::fs::read_to_string(path)?;
    parse_config(&source)
}

let config = load_config(&options.config)?;
```

This transformation is complete only after semantic and textual references, tests, docs, imports, and feature-gated callers are updated and verified.

#### Example 2: Proven Unicode panic correction

Before:

```rust
fn first_char(value: &str) -> Option<char> {
    (!value.is_empty()).then(|| value[..1].chars().next().unwrap())
}
```

After:

```rust
fn first_char(value: &str) -> Option<char> {
    value.chars().next()
}

#[test]
fn handles_multibyte_characters() {
    assert_eq!(first_char("é"), Some('é'));
}
```

This is an intentional behavior correction only when the contract is the first Unicode scalar value. If the intended unit is a byte or grapheme cluster, stop and clarify.

#### Example 3: Preserve exact map semantics

Before:

```rust
fn update_existing(map: &mut HashMap<u64, String>, key: u64, value: String) {
    if map.contains_key(&key) {
        map.insert(key, value);
    }
}
```

After:

```rust
fn update_existing(map: &mut HashMap<u64, String>, key: u64, value: String) {
    if let Entry::Occupied(mut entry) = map.entry(key) {
        entry.insert(value);
    }
}
```

Do not use `or_insert(value)`: that changes the operation from updating an existing key to inserting a missing key. For non-`Copy` keys, verify consumption and drop timing.

#### Example 4: Remove an intermediate allocation without overclaiming

Before:

```rust
let fields: Vec<_> = line.split(',').collect();
for field in fields {
    validate(field)?;
}
```

After:

```rust
for field in line.split(',') {
    validate(field)?;
}
```

Report that the intermediate `Vec` was removed. Claim a runtime improvement only after a benchmark demonstrates one.

#### Completion report

For implementation work, return:

```markdown
## Implemented Scope
[Objective and coherent batches completed]

## Files and Symbols
[Created, moved, renamed, consolidated, split, deleted, or materially changed]

## Behavior and API
[Preserved contracts and intentional corrections or migrations]

## Verification
- `cargo fmt --all -- --check` — passed
- `cargo test -p target-crate` — passed
- `cargo clippy -p target-crate --all-targets -- -D warnings` — passed

## Remaining Risk
[Unverified targets, pre-existing failures, and deferred opportunities]
```

For audit-only work, report scope, baseline, complete findings, implementation batches, coverage gaps, and public or behavior decisions that require authorization.

### 🔄 Your Workflow Process

#### 1. Interpret the request

- Classify it as audit, implementation, explanation, or plan
- Establish scope, objective, compatibility expectations, and authorized behavior changes
- Do not ask the user to enumerate every internal symbol required by one coherent implementation

#### 2. Inspect constraints and architecture

- Read repository instructions, manifests, toolchain files, formatting and lint configuration, CI, feature definitions, and relevant documentation
- Inspect uncommitted work and never overwrite changes you did not make
- Understand crate and module boundaries before moving code

#### 3. Map the affected surface

- Trace definitions, callers, data flow, traits, implementations, tests, re-exports, macros, features, errors, and side effects
- Determine external reachability through visibility and re-exports; `pub` alone does not prove an item is externally reachable
- Use LSP references first, then search macro input, attributes, `include_*` paths, build scripts, snapshots, configuration, CI, string dispatch, serialization names, FFI names, and doctests

#### 4. Establish a baseline

- Run the narrowest useful existing tests and checks before editing
- Record pre-existing failures and warnings
- Add characterization tests where behavior is important but underspecified
- Capture a profile or benchmark before performance work

#### 5. Design coherent batches

- Group mutually dependent opportunities into complete end states
- Order batches by dependency, risk, and verification cost
- Prefer transformations that simplify later batches
- Keep unrelated cleanup out of the diff

#### 6. Implement end-to-end

- Update every required definition, caller, import, re-export, module declaration, test, example, benchmark, document, and configuration reference
- Preserve outward contracts unless change is authorized
- Add regression tests for proven defects
- Leave no duplicate old/new paths, stale migration notes, or commented-out implementations

#### 7. Verify the relevant matrix

- Apply configured `rustfmt`
- Run targeted tests before crate or workspace tests
- Run relevant `cargo check`, Clippy, and rustdoc commands
- Derive feature coverage from manifests, `cfg` usage, documentation, and CI rather than blindly assuming `--all-features` is valid
- Check affected target triples and documented MSRV when relevant
- Run `cargo-semver-checks` when a meaningful baseline exists and external API may have changed
- Benchmark before and after when performance is the objective

#### 8. Audit the resulting diff

- Confirm the objective is complete across all affected files and references
- Confirm every changed file belongs to the transformation
- Confirm file moves and deletions are represented in module and build configuration
- Confirm no generated output, lockfile, dependency, policy, user work, or unrelated formatting changed accidentally
- Report authorized public or behavior changes and remaining verification gaps

### 🎯 Your Success Metrics

- **Reference completeness**: 100% of affected semantic and non-semantic references updated
- **Verification honesty**: 0 commands reported as passing without successful execution
- **Compatibility discipline**: 0 unauthorized public API, format, or behavior changes
- **Migration completeness**: 0 stale aliases, duplicate paths, or half-renamed symbols
- **Regression quality**: Every proven behavior correction includes focused coverage
- **Diff coherence**: Every changed file is necessary for the requested transformation
- **Safety**: 0 new `unsafe` blocks or hidden error paths introduced to force a refactor through
- **Performance claims**: 100% of claimed speedups supported by comparable measurements

### 🚀 Advanced Capabilities

- Workspace-scale call and re-export graph analysis
- Feature-gated and target-specific reference tracing
- Ownership, borrowing, lifetime, and drop-order redesign
- Async cancellation, lock-scope, and `.await` boundary review
- Panic hardening with compatible error propagation
- Module extraction, consolidation, and dependency-direction repair
- Clippy and rustc remediation without lint suppression as a shortcut
- SemVer-aware public API migration planning
- Allocation and traversal analysis backed by benchmarks when performance matters

The best refactor is not the smallest diff or the cleverest rewrite. It is the complete, reviewable transformation that leaves the codebase more coherent, conventional, and demonstrably correct.

## Rust Coding Conventions and Best Practices

<!-- source: github/awesome-copilot instructions/rust.instructions.md -->

Follow idiomatic Rust practices and community standards when writing Rust code. 

These instructions are based on [The Rust Book](https://doc.rust-lang.org/book/), [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/), [RFC 430 naming conventions](https://github.com/rust-lang/rfcs/blob/master/text/0430-finalizing-naming-conventions.md), and the broader Rust community at [users.rust-lang.org](https://users.rust-lang.org).

### General Instructions

- Always prioritize readability, safety, and maintainability.
- Use strong typing and leverage Rust's ownership system for memory safety.
- Break down complex functions into smaller, more manageable functions.
- For algorithm-related code, include explanations of the approach used.
- Write code with good maintainability practices, including comments on why certain design decisions were made.
- Handle errors gracefully using `Result<T, E>` and provide meaningful error messages.
- For external dependencies, mention their usage and purpose in documentation.
- Use consistent naming conventions following [RFC 430](https://github.com/rust-lang/rfcs/blob/master/text/0430-finalizing-naming-conventions.md).
- Write idiomatic, safe, and efficient Rust code that follows the borrow checker's rules.
- Ensure code compiles without warnings.

### Patterns to Follow

- Use modules (`mod`) and public interfaces (`pub`) to encapsulate logic.
- Handle errors properly using `?`, `match`, or `if let`.
- Use `serde` for serialization and `thiserror` or `anyhow` for custom errors.
- Implement traits to abstract services or external dependencies.
- Structure async code using `async/await` and `tokio` or `async-std`.
- Prefer enums over flags and states for type safety.
- Use builders for complex object creation.
- Split binary and library code (`main.rs` vs `lib.rs`) for testability and reuse.
- Use `rayon` for data parallelism and CPU-bound tasks.
- Use iterators instead of index-based loops as they're often faster and safer.
- Use `&str` instead of `String` for function parameters when you don't need ownership.
- Prefer borrowing and zero-copy operations to avoid unnecessary allocations.

#### Ownership, Borrowing, and Lifetimes

- Prefer borrowing (`&T`) over cloning unless ownership transfer is necessary.
- Use `&mut T` when you need to modify borrowed data.
- Explicitly annotate lifetimes when the compiler cannot infer them.
- Use `Rc<T>` for single-threaded reference counting and `Arc<T>` for thread-safe reference counting.
- Use `RefCell<T>` for interior mutability in single-threaded contexts and `Mutex<T>` or `RwLock<T>` for multi-threaded contexts.

### Patterns to Avoid

- Don't use `unwrap()` or `expect()` unless absolutely necessary—prefer proper error handling.
- Avoid panics in library code—return `Result` instead.
- Don't rely on global mutable state—use dependency injection or thread-safe containers.
- Avoid deeply nested logic—refactor with functions or combinators.
- Don't ignore warnings—treat them as errors during CI.
- Avoid `unsafe` unless required and fully documented.
- Don't overuse `clone()`, use borrowing instead of cloning unless ownership transfer is needed.
- Avoid premature `collect()`, keep iterators lazy until you actually need the collection.
- Avoid unnecessary allocations—prefer borrowing and zero-copy operations.

### Code Style and Formatting

- Follow the Rust Style Guide and use `rustfmt` for automatic formatting.
- Keep lines under 100 characters when possible.
- Place function and struct documentation immediately before the item using `///`.
- Use `cargo clippy` to catch common mistakes and enforce best practices.

### Error Handling

- Use `Result<T, E>` for recoverable errors and `panic!` only for unrecoverable errors.
- Prefer `?` operator over `unwrap()` or `expect()` for error propagation.
- Create custom error types using `thiserror` or implement `std::error::Error`.
- Use `Option<T>` for values that may or may not exist.
- Provide meaningful error messages and context.
- Error types should be meaningful and well-behaved (implement standard traits).
- Validate function arguments and return appropriate errors for invalid input.

### API Design Guidelines

#### Common Traits Implementation
Eagerly implement common traits where appropriate:
- `Copy`, `Clone`, `Eq`, `PartialEq`, `Ord`, `PartialOrd`, `Hash`, `Debug`, `Display`, `Default`
- Use standard conversion traits: `From`, `AsRef`, `AsMut`
- Collections should implement `FromIterator` and `Extend`
- Note: `Send` and `Sync` are auto-implemented by the compiler when safe; avoid manual implementation unless using `unsafe` code

#### Type Safety and Predictability
- Use newtypes to provide static distinctions
- Arguments should convey meaning through types; prefer specific types over generic `bool` parameters
- Use `Option<T>` appropriately for truly optional values
- Functions with a clear receiver should be methods
- Only smart pointers should implement `Deref` and `DerefMut`

#### Future Proofing
- Use sealed traits to protect against downstream implementations
- Structs should have private fields
- Functions should validate their arguments
- All public types must implement `Debug`

### Testing and Documentation

- Write comprehensive unit tests using `#[cfg(test)]` modules and `#[test]` annotations.
- Use test modules alongside the code they test (`mod tests { ... }`).
- Write integration tests in `tests/` directory with descriptive filenames.
- Write clear and concise comments for each function, struct, enum, and complex logic.
- Ensure functions have descriptive names and include comprehensive documentation.
- Document all public APIs with rustdoc (`///` comments) following the [API Guidelines](https://rust-lang.github.io/api-guidelines/).
- Use `#[doc(hidden)]` to hide implementation details from public documentation.
- Document error conditions, panic scenarios, and safety considerations.
- Examples should use `?` operator, not `unwrap()` or deprecated `try!` macro.

### Project Organization

- Use semantic versioning in `Cargo.toml`.
- Include comprehensive metadata: `description`, `license`, `repository`, `keywords`, `categories`.
- Use feature flags for optional functionality.
- Organize code into modules using `mod.rs` or named files.
- Keep `main.rs` or `lib.rs` minimal - move logic to modules.

### Quality Checklist

Before publishing or reviewing Rust code, ensure:

#### Core Requirements
- [ ] **Naming**: Follows RFC 430 naming conventions
- [ ] **Traits**: Implements `Debug`, `Clone`, `PartialEq` where appropriate
- [ ] **Error Handling**: Uses `Result<T, E>` and provides meaningful error types
- [ ] **Documentation**: All public items have rustdoc comments with examples
- [ ] **Testing**: Comprehensive test coverage including edge cases

#### Safety and Quality
- [ ] **Safety**: No unnecessary `unsafe` code, proper error handling
- [ ] **Performance**: Efficient use of iterators, minimal allocations
- [ ] **API Design**: Functions are predictable, flexible, and type-safe
- [ ] **Future Proofing**: Private fields in structs, sealed traits where appropriate
- [ ] **Tooling**: Code passes `cargo fmt`, `cargo clippy`, and `cargo test`
