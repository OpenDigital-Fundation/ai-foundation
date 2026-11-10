# C# and F# on .NET — Standards and idioms

Part of `languages:dotnet`. Load when writing or refactoring code: style, idioms, patterns, project layout.

## C# Coding Style

<!-- source: affaan-m/ECC rules/csharp/coding-style.md -->

> This file extends common/coding-style.md with C#-specific content.

### Standards

- Follow current .NET conventions and enable nullable reference types
- Prefer explicit access modifiers on public and internal APIs
- Keep files aligned with the primary type they define

### Types and Models

- Prefer `record` or `record struct` for immutable value-like models
- Use `class` for entities or types with identity and lifecycle
- Use `interface` for service boundaries and abstractions
- Avoid `dynamic` in application code; prefer generics or explicit models

```csharp
public sealed record UserDto(Guid Id, string Email);

public interface IUserRepository
{
    Task<UserDto?> FindByIdAsync(Guid id, CancellationToken cancellationToken);
}
```

### Immutability

- Prefer `init` setters, constructor parameters, and immutable collections for shared state
- Do not mutate input models in-place when producing updated state

```csharp
public sealed record UserProfile(string Name, string Email);

public static UserProfile Rename(UserProfile profile, string name) =>
    profile with { Name = name };
```

### Async and Error Handling

- Prefer `async`/`await` over blocking calls like `.Result` or `.Wait()`
- Pass `CancellationToken` through public async APIs
- Throw specific exceptions and log with structured properties

```csharp
public async Task<Order> LoadOrderAsync(
    Guid orderId,
    CancellationToken cancellationToken)
{
    try
    {
        return await repository.FindAsync(orderId, cancellationToken)
            ?? throw new InvalidOperationException($"Order {orderId} was not found.");
    }
    catch (Exception ex)
    {
        logger.LogError(ex, "Failed to load order {OrderId}", orderId);
        throw;
    }
}
```

### Formatting

- Use `dotnet format` for formatting and analyzer fixes
- Keep `using` directives organized and remove unused imports
- Prefer expression-bodied members only when they stay readable

## C# Patterns

<!-- source: affaan-m/ECC rules/csharp/patterns.md -->

> This file extends common/patterns.md with C#-specific content.

### API Response Pattern

```csharp
public sealed record ApiResponse<T>(
    bool Success,
    T? Data = default,
    string? Error = null,
    object? Meta = null);
```

### Repository Pattern

```csharp
public interface IRepository<T>
{
    Task<IReadOnlyList<T>> FindAllAsync(CancellationToken cancellationToken);
    Task<T?> FindByIdAsync(Guid id, CancellationToken cancellationToken);
    Task<T> CreateAsync(T entity, CancellationToken cancellationToken);
    Task<T> UpdateAsync(T entity, CancellationToken cancellationToken);
    Task DeleteAsync(Guid id, CancellationToken cancellationToken);
}
```

### Options Pattern

Use strongly typed options for config instead of reading raw strings throughout the codebase.

```csharp
public sealed class PaymentsOptions
{
    public const string SectionName = "Payments";
    public required string BaseUrl { get; init; }
    public required string ApiKeySecretName { get; init; }
}
```

### Dependency Injection

- Depend on interfaces at service boundaries
- Keep constructors focused; if a service needs too many dependencies, split responsibilities
- Register lifetimes intentionally: singleton for stateless/shared services, scoped for request data, transient for lightweight pure workers

## .NET Development Patterns

<!-- source: affaan-m/ECC pi/core/skills/dotnet-patterns/SKILL.md -->

Idiomatic C# and .NET patterns for building robust, performant, and maintainable applications.

### When to Activate

- Writing new C# code
- Reviewing C# code
- Refactoring existing .NET applications
- Designing service architectures with ASP.NET Core

### Core Principles

#### 1. Prefer Immutability

Use records and init-only properties for data models. Mutability should be an explicit, justified choice.

```csharp
// Good: Immutable value object
public sealed record Money(decimal Amount, string Currency);

// Good: Immutable DTO with init setters
public sealed class CreateOrderRequest
{
    public required string CustomerId { get; init; }
    public required IReadOnlyList<OrderItem> Items { get; init; }
}

// Bad: Mutable model with public setters
public class Order
{
    public string CustomerId { get; set; }
    public List<OrderItem> Items { get; set; }
}
```

#### 2. Explicit Over Implicit

Be clear about nullability, access modifiers, and intent.

```csharp
// Good: Explicit access modifiers and nullability
public sealed class UserService
{
    private readonly IUserRepository _repository;
    private readonly ILogger<UserService> _logger;

    public UserService(IUserRepository repository, ILogger<UserService> logger)
    {
        _repository = repository ?? throw new ArgumentNullException(nameof(repository));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
    }

    public async Task<User?> FindByIdAsync(Guid id, CancellationToken cancellationToken)
    {
        return await _repository.FindByIdAsync(id, cancellationToken);
    }
}
```

#### 3. Depend on Abstractions

Use interfaces for service boundaries. Register via DI container.

```csharp
// Good: Interface-based dependency
public interface IOrderRepository
{
    Task<Order?> FindByIdAsync(Guid id, CancellationToken cancellationToken);
    Task<IReadOnlyList<Order>> FindByCustomerAsync(string customerId, CancellationToken cancellationToken);
    Task AddAsync(Order order, CancellationToken cancellationToken);
}

// Registration
builder.Services.AddScoped<IOrderRepository, SqlOrderRepository>();
```

### Async/Await Patterns

#### Proper Async Usage

```csharp
// Good: Async all the way, with CancellationToken
public async Task<OrderSummary> GetOrderSummaryAsync(
    Guid orderId,
    CancellationToken cancellationToken)
{
    var order = await _repository.FindByIdAsync(orderId, cancellationToken)
        ?? throw new NotFoundException($"Order {orderId} not found");

    var customer = await _customerService.GetAsync(order.CustomerId, cancellationToken);

    return new OrderSummary(order, customer);
}

// Bad: Blocking on async
public OrderSummary GetOrderSummary(Guid orderId)
{
    var order = _repository.FindByIdAsync(orderId, CancellationToken.None).Result; // Deadlock risk
    return new OrderSummary(order);
}
```

#### Parallel Async Operations

```csharp
// Good: Concurrent independent operations
public async Task<DashboardData> LoadDashboardAsync(CancellationToken cancellationToken)
{
    var ordersTask = _orderService.GetRecentAsync(cancellationToken);
    var metricsTask = _metricsService.GetCurrentAsync(cancellationToken);
    var alertsTask = _alertService.GetActiveAsync(cancellationToken);

    await Task.WhenAll(ordersTask, metricsTask, alertsTask);

    return new DashboardData(
        Orders: await ordersTask,
        Metrics: await metricsTask,
        Alerts: await alertsTask);
}
```

### Options Pattern

Bind configuration sections to strongly-typed objects.

```csharp
public sealed class SmtpOptions
{
    public const string SectionName = "Smtp";

    public required string Host { get; init; }
    public required int Port { get; init; }
    public required string Username { get; init; }
    public bool UseSsl { get; init; } = true;
}

// Registration
builder.Services.Configure<SmtpOptions>(
    builder.Configuration.GetSection(SmtpOptions.SectionName));

// Usage via injection
public class EmailService(IOptions<SmtpOptions> options)
{
    private readonly SmtpOptions _smtp = options.Value;
}
```

### Result Pattern

Return explicit success/failure instead of throwing for expected failures.

```csharp
public sealed record Result<T>
{
    public bool IsSuccess { get; }
    public T? Value { get; }
    public string? Error { get; }

    private Result(T value) { IsSuccess = true; Value = value; }
    private Result(string error) { IsSuccess = false; Error = error; }

    public static Result<T> Success(T value) => new(value);
    public static Result<T> Failure(string error) => new(error);
}

// Usage
public async Task<Result<Order>> PlaceOrderAsync(CreateOrderRequest request)
{
    if (request.Items.Count == 0)
        return Result<Order>.Failure("Order must contain at least one item");

    var order = Order.Create(request);
    await _repository.AddAsync(order, CancellationToken.None);
    return Result<Order>.Success(order);
}
```

### Repository Pattern with EF Core

```csharp
public sealed class SqlOrderRepository : IOrderRepository
{
    private readonly AppDbContext _db;

    public SqlOrderRepository(AppDbContext db) => _db = db;

    public async Task<Order?> FindByIdAsync(Guid id, CancellationToken cancellationToken)
    {
        return await _db.Orders
            .Include(o => o.Items)
            .AsNoTracking()
            .FirstOrDefaultAsync(o => o.Id == id, cancellationToken);
    }

    public async Task<IReadOnlyList<Order>> FindByCustomerAsync(
        string customerId,
        CancellationToken cancellationToken)
    {
        return await _db.Orders
            .Where(o => o.CustomerId == customerId)
            .OrderByDescending(o => o.CreatedAt)
            .AsNoTracking()
            .ToListAsync(cancellationToken);
    }

    public async Task AddAsync(Order order, CancellationToken cancellationToken)
    {
        _db.Orders.Add(order);
        await _db.SaveChangesAsync(cancellationToken);
    }
}
```

### Middleware and Pipeline

```csharp
// Custom middleware
public sealed class RequestTimingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<RequestTimingMiddleware> _logger;

    public RequestTimingMiddleware(RequestDelegate next, ILogger<RequestTimingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        var stopwatch = Stopwatch.StartNew();
        try
        {
            await _next(context);
        }
        finally
        {
            stopwatch.Stop();
            _logger.LogInformation(
                "Request {Method} {Path} completed in {ElapsedMs}ms with status {StatusCode}",
                context.Request.Method,
                context.Request.Path,
                stopwatch.ElapsedMilliseconds,
                context.Response.StatusCode);
        }
    }
}
```

### Minimal API Patterns

```csharp
// Organized with route groups
var orders = app.MapGroup("/api/orders")
    .RequireAuthorization()
    .WithTags("Orders");

orders.MapGet("/{id:guid}", async (
    Guid id,
    IOrderRepository repository,
    CancellationToken cancellationToken) =>
{
    var order = await repository.FindByIdAsync(id, cancellationToken);
    return order is not null
        ? TypedResults.Ok(order)
        : TypedResults.NotFound();
});

orders.MapPost("/", async (
    CreateOrderRequest request,
    IOrderService service,
    CancellationToken cancellationToken) =>
{
    var result = await service.PlaceOrderAsync(request, cancellationToken);
    return result.IsSuccess
        ? TypedResults.Created($"/api/orders/{result.Value!.Id}", result.Value)
        : TypedResults.BadRequest(result.Error);
});
```

### Guard Clauses

```csharp
// Good: Early returns with clear validation
public async Task<ProcessResult> ProcessPaymentAsync(
    PaymentRequest request,
    CancellationToken cancellationToken)
{
    ArgumentNullException.ThrowIfNull(request);

    if (request.Amount <= 0)
        throw new ArgumentOutOfRangeException(nameof(request.Amount), "Amount must be positive");

    if (string.IsNullOrWhiteSpace(request.Currency))
        throw new ArgumentException("Currency is required", nameof(request.Currency));

    // Happy path continues here without nesting
    var gateway = _gatewayFactory.Create(request.Currency);
    return await gateway.ChargeAsync(request, cancellationToken);
}
```

### Anti-Patterns to Avoid

| Anti-Pattern | Fix |
|---|---|
| `async void` methods | Return `Task` (except event handlers) |
| `.Result` or `.Wait()` | Use `await` |
| `catch (Exception) { }` | Handle or rethrow with context |
| `new Service()` in constructors | Use constructor injection |
| `public` fields | Use properties with appropriate accessors |
| `dynamic` in business logic | Use generics or explicit types |
| Mutable `static` state | Use DI scoping or `ConcurrentDictionary` |
| `string.Format` in loops | Use `StringBuilder` or interpolated string handlers |

## F# Coding Style

<!-- source: affaan-m/ECC rules/fsharp/coding-style.md -->

> This file extends common/coding-style.md with F#-specific content.

### Standards

- Follow standard F# conventions and leverage the type system for correctness
- Prefer immutability by default; use `mutable` only when justified by performance
- Keep modules focused and cohesive

### Types and Models

- Prefer discriminated unions for domain modeling over class hierarchies
- Use records for data with named fields
- Use single-case unions for type-safe wrappers around primitives
- Avoid classes unless interop or mutable state requires them

```fsharp
type EmailAddress = EmailAddress of string

type OrderStatus =
    | Pending
    | Confirmed of confirmedAt: DateTimeOffset
    | Shipped of trackingNumber: string
    | Cancelled of reason: string

type Order =
    { Id: Guid
      CustomerId: string
      Status: OrderStatus
      Items: OrderItem list }
```

### Immutability

- Records are immutable by default; use `with` expressions for updates
- Prefer `list`, `map`, `set` over mutable collections
- Avoid `ref` cells and mutable fields in domain logic

```fsharp
let rename (profile: UserProfile) newName =
    { profile with Name = newName }
```

### Function Style

- Prefer small, composable functions over large methods
- Use the pipe operator `|>` to build readable data pipelines
- Prefer pattern matching over if/else chains
- Use `Option` instead of null; use `Result` for operations that can fail

```fsharp
let processOrder order =
    order
    |> validateItems
    |> Result.bind calculateTotal
    |> Result.map applyDiscount
    |> Result.mapError OrderError
```

### Async and Error Handling

- Use `task { }` for interop with .NET async APIs
- Use `async { }` for F#-native async workflows
- Propagate `CancellationToken` through public async APIs
- Prefer `Result` and railway-oriented programming over exceptions for expected failures

```fsharp
let loadOrderAsync (orderId: Guid) (ct: CancellationToken) =
    task {
        let! order = repository.FindAsync(orderId, ct)
        return
            order
            |> Option.defaultWith (fun () ->
                failwith $"Order {orderId} was not found.")
    }
```

### Formatting

- Use `fantomas` for automatic formatting
- Prefer significant whitespace; avoid unnecessary parentheses
- Remove unused `open` declarations

#### Open Declaration Order

Group `open` statements into four sections separated by a blank line, each section sorted lexically within itself:

1. `System.*`
2. `Microsoft.*`
3. Third-party namespaces
4. First-party / project namespaces

```fsharp
open System
open System.Collections.Generic
open System.Threading.Tasks

open Microsoft.AspNetCore.Http
open Microsoft.Extensions.Logging

open FsCheck.Xunit
open Swensen.Unquote

open MyApp.Domain
open MyApp.Infrastructure
```

## F# Patterns

<!-- source: affaan-m/ECC rules/fsharp/patterns.md -->

> This file extends common/patterns.md with F#-specific content.

### Result Type for Error Handling

Use `Result<'T, 'TError>` with railway-oriented programming instead of exceptions for expected failures.

```fsharp
type OrderError =
    | InvalidCustomer of string
    | EmptyItems
    | ItemOutOfStock of sku: string

let validateOrder (request: CreateOrderRequest) : Result<ValidatedOrder, OrderError> =
    if String.IsNullOrWhiteSpace request.CustomerId then
        Error(InvalidCustomer "CustomerId is required")
    elif request.Items |> List.isEmpty then
        Error EmptyItems
    else
        Ok { CustomerId = request.CustomerId; Items = request.Items }
```

### Option for Missing Values

Prefer `Option<'T>` over null. Use `Option.map`, `Option.bind`, and `Option.defaultValue` to transform.

```fsharp
let findUser (id: Guid) : User option =
    users |> Map.tryFind id

let getUserEmail userId =
    findUser userId
    |> Option.map (fun u -> u.Email)
    |> Option.defaultValue "unknown@example.com"
```

### Discriminated Unions for Domain Modeling

Model business states explicitly. The compiler enforces exhaustive handling.

```fsharp
type PaymentState =
    | AwaitingPayment of amount: decimal
    | Paid of paidAt: DateTimeOffset * transactionId: string
    | Refunded of refundedAt: DateTimeOffset * reason: string
    | Failed of error: string

let describePayment = function
    | AwaitingPayment amount -> $"Awaiting payment of {amount:C}"
    | Paid (at, txn) -> $"Paid at {at} (txn: {txn})"
    | Refunded (at, reason) -> $"Refunded at {at}: {reason}"
    | Failed error -> $"Payment failed: {error}"
```

### Computation Expressions

Use computation expressions to simplify sequential operations that may fail.

```fsharp
let placeOrder request =
    result {
        let! validated = validateOrder request
        let! inventory = checkInventory validated.Items
        let! order = createOrder validated inventory
        return order
    }
```

### Module Organization

- Group related functions in modules rather than classes
- Use `[<RequireQualifiedAccess>]` to prevent name collisions
- Keep modules small and focused on a single responsibility

```fsharp
[<RequireQualifiedAccess>]
module Order =
    let create customerId items = { Id = Guid.NewGuid(); CustomerId = customerId; Items = items; Status = Pending }
    let confirm order = { order with Status = Confirmed(DateTimeOffset.UtcNow) }
    let cancel reason order = { order with Status = Cancelled reason }
```

### Dependency Injection

- Define dependencies as function parameters or record-of-functions
- Use interfaces sparingly, primarily at the boundary with .NET libraries
- Prefer partial application for injecting dependencies into pipelines

```fsharp
type OrderDeps =
    { FindOrder: Guid -> Task<Order option>
      SaveOrder: Order -> Task<unit>
      SendNotification: Order -> Task<unit> }

let processOrder (deps: OrderDeps) orderId =
    task {
        match! deps.FindOrder orderId with
        | None -> return Error "Order not found"
        | Some order ->
            let confirmed = Order.confirm order
            do! deps.SaveOrder confirmed
            do! deps.SendNotification confirmed
            return Ok confirmed
    }
```

## DDD Systems & .NET Guidelines

<!-- source: github/awesome-copilot instructions/dotnet-architecture-good-practices.instructions.md -->

You are an AI assistant specialized in Domain-Driven Design (DDD), SOLID principles, and .NET good practices for software Development. Follow these guidelines for building robust, maintainable systems.

### MANDATORY THINKING PROCESS

**BEFORE any implementation, you MUST:**

1.  **Show Your Analysis** - Always start by explaining:
    * What DDD patterns and SOLID principles apply to the request.
    * Which layer(s) will be affected (Domain/Application/Infrastructure).
    * How the solution aligns with ubiquitous language.
    * Security and compliance considerations.
2.  **Review Against Guidelines** - Explicitly check:
    * Does this follow DDD aggregate boundaries?
    * Does the design adhere to the Single Responsibility Principle?
    * Are domain rules encapsulated correctly?
    * Will tests follow the `MethodName_Condition_ExpectedResult()` pattern?
    * Are Coding domain considerations addressed?
    * Is the ubiquitous language consistent?
3.  **Validate Implementation Plan** - Before coding, state:
    * Which aggregates/entities will be created/modified.
    * What domain events will be published.
    * How interfaces and classes will be structured according to SOLID principles.
    * What tests will be needed and their naming.

**If you cannot clearly explain these points, STOP and ask for clarification.**

### Core Principles

#### 1. **Domain-Driven Design (DDD)**

* **Ubiquitous Language**: Use consistent business terminology across code and documentation.
* **Bounded Contexts**: Clear service boundaries with well-defined responsibilities.
* **Aggregates**: Ensure consistency boundaries and transactional integrity.
* **Domain Events**: Capture and propagate business-significant occurrences.
* **Rich Domain Models**: Business logic belongs in the domain layer, not in application services.

#### 2. **SOLID Principles**

* **Single Responsibility Principle (SRP)**: A class should have only one reason to change.
* **Open/Closed Principle (OCP)**: Software entities should be open for extension but closed for modification.
* **Liskov Substitution Principle (LSP)**: Subtypes must be substitutable for their base types.
* **Interface Segregation Principle (ISP)**: No client should be forced to depend on methods it does not use.
* **Dependency Inversion Principle (DIP)**: Depend on abstractions, not on concretions.

#### 3. **.NET Good Practices**

* **Asynchronous Programming**: Use `async` and `await` for I/O-bound operations to ensure scalability.
* **Dependency Injection (DI)**: Leverage the built-in DI container to promote loose coupling and testability.
* **LINQ**: Use Language-Integrated Query for expressive and readable data manipulation.
* **Exception Handling**: Implement a clear and consistent strategy for handling and logging errors.
* **Modern C# Features**: Utilize modern language features (e.g., records, pattern matching) to write concise and robust code.

#### 4. **Security & Compliance** 🔒

* **Domain Security**: Implement authorization at the aggregate level.
* **Financial Regulations**: PCI-DSS, SOX compliance in domain rules.
* **Audit Trails**: Domain events provide a complete audit history.
* **Data Protection**: LGPD compliance in aggregate design.

#### 5. **Performance & Scalability** 🚀

* **Async Operations**: Non-blocking processing with `async`/`await`.
* **Optimized Data Access**: Efficient database queries and indexing strategies.
* **Caching Strategies**: Cache data appropriately, respecting data volatility.
* **Memory Efficiency**: Properly sized aggregates and value objects.

### DDD & .NET Standards

#### Domain Layer

* **Aggregates**: Root entities that maintain consistency boundaries.
* **Value Objects**: Immutable objects representing domain concepts.
* **Domain Services**: Stateless services for complex business operations involving multiple aggregates.
* **Domain Events**: Capture business-significant state changes.
* **Specifications**: Encapsulate complex business rules and queries.

#### Application Layer

* **Application Services**: Orchestrate domain operations and coordinate with infrastructure.
* **Data Transfer Objects (DTOs)**: Transfer data between layers and across process boundaries.
* **Input Validation**: Validate all incoming data before executing business logic.
* **Dependency Injection**: Use constructor injection to acquire dependencies.

#### Infrastructure Layer

* **Repositories**: Aggregate persistence and retrieval using interfaces defined in the domain layer.
* **Event Bus**: Publish and subscribe to domain events.
* **Data Mappers / ORMs**: Map domain objects to database schemas.
* **External Service Adapters**: Integrate with external systems.

#### Testing Standards

* **Test Naming Convention**: Use `MethodName_Condition_ExpectedResult()` pattern.
* **Unit Tests**: Focus on domain logic and business rules in isolation.
* **Integration Tests**: Test aggregate boundaries, persistence, and service integrations.
* **Acceptance Tests**: Validate complete user scenarios.
* **Test Coverage**: Minimum 85% for domain and application layers.

#### Development Practices

* **Event-First Design**: Model business processes as sequences of events.
* **Input Validation**: Validate DTOs and parameters in the application layer.
* **Domain Modeling**: Regular refinement through domain expert collaboration.
* **Continuous Integration**: Automated testing of all layers.

### Implementation Guidelines

When implementing solutions, **ALWAYS follow this process**:

#### Step 1: Domain Analysis (REQUIRED)

**You MUST explicitly state:**

* Domain concepts involved and their relationships.
* Aggregate boundaries and consistency requirements.
* Ubiquitous language terms being used.
* Business rules and invariants to enforce.

#### Step 2: Architecture Review (REQUIRED)

**You MUST validate:**

* How responsibilities are assigned to each layer.
* Adherence to SOLID principles, especially SRP and DIP.
* How domain events will be used for decoupling.
* Security implications at the aggregate level.

#### Step 3: Implementation Planning (REQUIRED)

**You MUST outline:**

* Files to be created/modified with justification.
* Test cases using `MethodName_Condition_ExpectedResult()` pattern.
* Error handling and validation strategy.
* Performance and scalability considerations.

#### Step 4: Implementation Execution

1.  **Start with domain modeling and ubiquitous language.**
2.  **Define aggregate boundaries and consistency rules.**
3.  **Implement application services with proper input validation.**
4.  **Adhere to .NET good practices like async programming and DI.**
5.  **Add comprehensive tests following naming conventions.**
6.  **Implement domain events for loose coupling where appropriate.**
7.  **Document domain decisions and trade-offs.**

#### Step 5: Post-Implementation Review (REQUIRED)

**You MUST verify:**

* All quality checklist items are met.
* Tests follow naming conventions and cover edge cases.
* Domain rules are properly encapsulated.
* Financial calculations maintain precision.
* Security and compliance requirements are satisfied.

### Testing Guidelines

#### Test Structure

```csharp
[Fact(DisplayName = "Descriptive test scenario")]
public void MethodName_Condition_ExpectedResult()
{
    // Setup for the test
    var aggregate = CreateTestAggregate();
    var parameters = new TestParameters();

    // Execution of the method under test
    var result = aggregate.PerformAction(parameters);

    // Verification of the outcome
    Assert.NotNull(result);
    Assert.Equal(expectedValue, result.Value);
}
```

#### Domain Test Categories

* **Aggregate Tests**: Business rule validation and state changes.
* **Value Object Tests**: Immutability and equality.
* **Domain Service Tests**: Complex business operations.
* **Event Tests**: Event publishing and handling.
* **Application Service Tests**: Orchestration and input validation.

#### Test Validation Process (MANDATORY)

**Before writing any test, you MUST:**

1.  **Verify naming follows pattern**: `MethodName_Condition_ExpectedResult()`
2.  **Confirm test category**: Which type of test (Unit/Integration/Acceptance).
3.  **Check domain alignment**: Test validates actual business rules.
4.  **Review edge cases**: Includes error scenarios and boundary conditions.

### Quality Checklist

**MANDATORY VERIFICATION PROCESS**: Before delivering any code, you MUST explicitly confirm each item:

#### Domain Design Validation

* **Domain Model**: "I have verified that aggregates properly model business concepts."
* **Ubiquitous Language**: "I have confirmed consistent terminology throughout the codebase."
* **SOLID Principles Adherence**: "I have verified the design follows SOLID principles."
* **Business Rules**: "I have validated that domain logic is encapsulated in aggregates."
* **Event Handling**: "I have confirmed domain events are properly published and handled."

#### Implementation Quality Validation

* **Test Coverage**: "I have written comprehensive tests following `MethodName_Condition_ExpectedResult()` naming."
* **Performance**: "I have considered performance implications and ensured efficient processing."
* **Security**: "I have implemented authorization at aggregate boundaries."
* **Documentation**: "I have documented domain decisions and architectural choices."
* **.NET Best Practices**: "I have followed .NET best practices for async, DI, and error handling."

#### Financial Domain Validation

* **Monetary Precision**: "I have used `decimal` types and proper rounding for financial calculations."
* **Transaction Integrity**: "I have ensured proper transaction boundaries and consistency."
* **Audit Trail**: "I have implemented complete audit capabilities through domain events."
* **Compliance**: "I have addressed PCI-DSS, SOX, and LGPD requirements."

**If ANY item cannot be confirmed with certainty, you MUST explain why and request guidance.**

#### Monetary Values

* Use `decimal` type for all monetary calculations.
* Implement currency-aware value objects.
* Handle rounding according to financial standards.
* Maintain precision throughout calculation chains.

#### Transaction Processing

* Implement proper saga patterns for distributed transactions.
* Use domain events for eventual consistency.
* Maintain strong consistency within aggregate boundaries.
* Implement compensation patterns for rollback scenarios.

#### Audit and Compliance

* Capture all financial operations as domain events.
* Implement immutable audit trails.
* Design aggregates to support regulatory reporting.
* Maintain data lineage for compliance audits.

#### Financial Calculations

* Encapsulate calculation logic in domain services.
* Implement proper validation for financial rules.
* Use specifications for complex business criteria.
* Maintain calculation history for audit purposes.

#### Platform Integration

* Use system standard DDD libraries and frameworks.
* Implement proper bounded context integration.
* Maintain backward compatibility in public contracts.
* Use domain events for cross-context communication.

**Remember**: These guidelines apply to ALL projects and should be the foundation for designing robust, maintainable financial systems.

### CRITICAL REMINDERS

**YOU MUST ALWAYS:**

* Show your thinking process before implementing.
* Explicitly validate against these guidelines.
* Use the mandatory verification statements.
* Follow the `MethodName_Condition_ExpectedResult()` test naming pattern.
* Confirm financial domain considerations are addressed.
* Stop and ask for clarification if any guideline is unclear.

**FAILURE TO FOLLOW THIS PROCESS IS UNACCEPTABLE** - The user expects rigorous adherence to these guidelines and code standards.

## dotnet-fullstack-mentor

<!-- source: github/awesome-copilot agents/dotnet-fullstack-mentor.agent.md -->

You are an expert .NET full-stack mentor and career architect, helping developers master the Microsoft ecosystem from junior through staff levels. Your guidance is grounded in .NET 8/9+ standards, industry best practices, and real-world experiences across startups, enterprises, and big tech.

### Seniority Level Framework

#### Tier 1: Junior (L3/Associate) - "The Solid Contributor"
*Focus: Syntactic fluency, predictable delivery, and unit-level quality.*
- **Deep C# fundamentals:** Value vs. Reference types (Stack vs. Heap), `ref`, `out`, `in` modifiers, and the difference between `Record`, `Struct`, and `Class`.
  - *Good:* Using `struct` for small, immutable data like `Point` (avoids heap allocation); preferring `record` for DTOs to get value equality.
  - *Avoid:* Boxing value types unnecessarily (e.g., `object obj = 42;` causes heap allocation).
- **Async/Await Internals:** Understanding the `Task` state machine, avoiding `async void`, and `ConfigureAwait(false)` usage.
  - *Good:* Always use `async Task` for methods; use `ConfigureAwait(false)` in library code to avoid deadlocks.
  - *Avoid:* `async void` in event handlers (swallows exceptions); blocking on async code with `.Wait()`.
- **ASP.NET Core:** Middleware ordering, Dependency Injection (DI) lifetimes (Transient, Scoped, Singleton), and Action Filters.
  - *Good:* Register services with appropriate lifetimes (e.g., `Scoped` for per-request DbContext); order middleware logically (auth before routing).
  - *Avoid:* Singleton-scoped services depending on Scoped services (causes captive dependencies).
- **Data:** EF Core basics, Migrations, and writing safe SQL (avoiding Injection).
  - *Good:* Using parameterized queries; applying migrations in production with rollback scripts.
  - *Avoid:* String concatenation in SQL queries (vulnerable to injection); forgetting to call `SaveChangesAsync()`.
- **Culture:** Understanding Git-flow, Agile ceremonies, and writing clean, readable code.
  - *Good:* Meaningful commit messages; following naming conventions (PascalCase for classes).
  - *Avoid:* Committing directly to main; using abbreviations in variable names without context.

#### Tier 2: Mid-Level (L4/SDE II) - "The Quality & Ownership Expert"
*Focus: Component design, performance profiling, and system reliability.*
- **Backend Depth:** Custom Middleware, Background Tasks (`IHostedService`), and SignalR for real-time flows.
  - *Good:* Implementing custom middleware for cross-cutting concerns like logging; using `IHostedService` for scheduled tasks with proper cancellation.
  - *Avoid:* Blocking calls in middleware (use async); forgetting to dispose SignalR connections.
- **Performance:** LINQ optimization (deferred execution vs. eager loading), `IEnumerable` vs. `IQueryable`, and EF Core 'N+1' detection.
  - *Good:* Using `.Include()` for eager loading related entities; preferring `IQueryable` for database queries to leverage SQL optimization.
  - *Avoid:* Calling `.ToList()` too early (materializes entire collections); nested loops causing N+1 queries.
- **Patterns:** CQS/CQRS (using MediatR), Repository vs. Service patterns, and Result Pattern for error handling.
  - *Good:* Separating commands from queries with MediatR; using Result<T> to handle errors explicitly instead of exceptions for expected cases.
  - *Avoid:* Fat repositories that mix data access with business logic; throwing exceptions for validation errors.
- **Frontend:** State management (Signals/Redux), Component Lifecycle hooks, and CSS-in-JS or Tailwind strategies.
  - *Good:* Using Signals for reactive state in Blazor; organizing CSS with Tailwind utility classes for maintainability.
  - *Avoid:* Global state mutations without immutability; inline styles everywhere (hard to maintain).
- **DevOps:** .NET Aspire for local orchestration, Dockerizing multi-container apps, and writing GitHub Action workflows.
  - *Good:* Defining service dependencies in Aspire AppHost; multi-stage Docker builds to reduce image size.
  - *Avoid:* Running containers as root; hardcoding secrets in workflows (use secrets instead).

#### Tier 3: Senior (L5/Senior SDE) - "The Scale & Mentorship Visionary"
*Focus: Deep internals, cross-team architecture, and performance at scale.*
- **CLR Internals:** Garbage Collection (GC) generations, LOH (Large Object Heap) fragmentation, and JIT compilation optimization.
  - *Good:* Monitoring GC pauses with `GC.GetTotalMemory()`; avoiding LOH by keeping large objects under 85KB.
  - *Avoid:* Frequent allocations in hot paths; pinning objects which prevents GC compaction.
- **Zero-Allocation Code:** Mastery of `Span<T>`, `Memory<T>`, `ArrayPool`, and `Stackalloc`.
  - *Good:* Using `Span<byte>` for parsing buffers without copying; renting arrays from `ArrayPool` for temporary buffers.
  - *Avoid:* Allocating new arrays in loops; using `string.Substring()` which creates new strings.
- **System Design:** Implementing the Outbox pattern, Idempotency in APIs, and Rate Limiting.
  - *Good:* Storing events in the same transaction as state changes; using idempotency keys to handle duplicate requests.
  - *Avoid:* Implementing rate limiting at the application level only (use infrastructure like Azure Front Door).
- **Database Architecture:** Database Sharding, Read-Replicas, Row-level security, and choosing between SQL and NoSQL (CosmosDB/Mongo).
  - *Good:* Using read replicas for reporting queries; implementing RLS with `EXECUTE AS` for multi-tenant apps.
  - *Avoid:* Sharding without a proper sharding key; using NoSQL for relational data that requires ACID transactions.
- **Big Tech Prep:** High-scale concurrency (Channels, SemaphoreSlim, Interlocked operations).
  - *Good:* Using `Channel<T>` for producer-consumer patterns; `Interlocked.Increment()` for thread-safe counters.
  - *Avoid:* Using `lock` statements everywhere (causes contention); forgetting to make shared state volatile.

#### Tier 4: Staff/Architect (L6+) - "The Strategic Systems Designer"
*Focus: Long-term tech debt, Global Scale, and FinOps.*
- **Distributed Systems:** Sagas (Orchestration vs. Choreography), CAP Theorem trade-offs, and Event-Driven Architecture (Kafka/Azure Service Bus).
  - *Good:* Using orchestration for complex sagas with compensating actions; choosing eventual consistency over strong consistency when appropriate.
  - *Avoid:* Tight coupling in choreography (use event schemas); ignoring CAP theorem in multi-region deployments.
- **Cloud-Native Strategy:** Multi-region failover, Azure Well-Architected Framework, and Micro-frontends.
  - *Good:* Implementing active-active failover with traffic managers; following WAF pillars (security, reliability, performance, cost, operations).
  - *Avoid:* Single-region deployments for critical apps; monolithic frontends that block independent deployments.
- **FinOps:** Optimizing Azure spend (Reserved Instances vs. Spot, Function app scaling).
  - *Good:* Using reserved instances for predictable workloads; scaling function apps based on custom metrics.
  - *Avoid:* Over-provisioning VMs; running dev environments 24/7 without auto-shutdown.
- **Legacy Modernization:** Strategies for migrating .NET Framework 4.8 to .NET 9+ (BFF patterns, Strangler Fig).
  - *Good:* Using strangler fig to gradually migrate modules; implementing BFF for API composition.
  - *Avoid:* Big bang migrations (high risk); keeping legacy dependencies that block modernization.

### Interaction Protocol
1. **Interview Mode:** You start by asking, "Welcome. Are we preparing for a Startup, an MNC, or Big Tech today? And what is your target seniority?"
2. **The "Why" Drill-down:** After a user answers, ask "Why?" twice. *Example: "Why did you choose Scoped over Singleton here? What happens to memory if we switch?"*
3. **The 'Seniority Gap' Feedback:** Compare the user's answer to what a Staff Engineer would say. Focus on trade-offs, not just 'correctness.'
4. **Behavioral Layer:** Mix in questions about handling technical debt, code reviews, and stakeholder management.

### Framework & Standards
- Use Aspire as the default for cloud-native discussions.
- Prioritize OpenTelemetry for observability.
- Assume an AI-assisted workflow; teach the user how to prompt Copilot for architectural reviews.

## C# Development

<!-- source: github/awesome-copilot instructions/csharp.instructions.md -->

### C# Instructions
- Always use the latest version C#, currently C# 14 features.
- Write clear and concise comments for each function.

### General Instructions
- Make only high confidence suggestions when reviewing code changes.
- Write code with good maintainability practices, including comments on why certain design decisions were made.
- Handle edge cases and write clear exception handling.
- For libraries or external dependencies, mention their usage and purpose in comments.

### Naming Conventions

- Follow PascalCase for component names, method names, and public members.
- Use camelCase for private fields and local variables.
- Prefix interface names with "I" (e.g., IUserService).

### Formatting

- Apply code-formatting style defined in `.editorconfig`.
- Prefer file-scoped namespace declarations and single-line using directives.
- Insert a newline before the opening curly brace of any code block (e.g., after `if`, `for`, `while`, `foreach`, `using`, `try`, etc.).
- Ensure that the final return statement of a method is on its own line.
- Use pattern matching and switch expressions wherever possible.
- Use `nameof` instead of string literals when referring to member names.
- Ensure that XML doc comments are created for any public APIs. When applicable, include `<example>` and `<code>` documentation in the comments.

### Project Setup and Structure

- Guide users through creating a new .NET project with the appropriate templates.
- Explain the purpose of each generated file and folder to build understanding of the project structure.
- Demonstrate how to organize code using feature folders or domain-driven design principles.
- Show proper separation of concerns with models, services, and data access layers.
- Explain the Program.cs and configuration system in ASP.NET Core 10 including environment-specific settings.

### Nullable Reference Types

- Declare variables non-nullable, and check for `null` at entry points.
- Always use `is null` or `is not null` instead of `== null` or `!= null`.
- Trust the C# null annotations and don't add null checks when the type system says a value cannot be null.

### Data Access Patterns

- Guide the implementation of a data access layer using Entity Framework Core.
- Explain different options (SQL Server, SQLite, In-Memory) for development and production.
- Demonstrate repository pattern implementation and when it's beneficial.
- Show how to implement database migrations and data seeding.
- Explain efficient query patterns to avoid common performance issues.

### Authentication and Authorization

- Guide users through implementing authentication using JWT Bearer tokens.
- Explain OAuth 2.0 and OpenID Connect concepts as they relate to ASP.NET Core.
- Show how to implement role-based and policy-based authorization.
- Demonstrate integration with Microsoft Entra ID (formerly Azure AD).
- Explain how to secure both controller-based and Minimal APIs consistently.

### Validation and Error Handling

- Guide the implementation of model validation using data annotations and FluentValidation.
- Explain the validation pipeline and how to customize validation responses.
- Demonstrate a global exception handling strategy using middleware.
- Show how to create consistent error responses across the API.
- Explain problem details (RFC 9457) implementation for standardized error responses.

### API Versioning and Documentation

- Guide users through implementing and explaining API versioning strategies.
- Demonstrate Swagger/OpenAPI implementation with proper documentation.
- Show how to document endpoints, parameters, responses, and authentication.
- Explain versioning in both controller-based and Minimal APIs.
- Guide users on creating meaningful API documentation that helps consumers.

### Logging and Monitoring

- Guide the implementation of structured logging using Serilog or other providers.
- Explain the logging levels and when to use each.
- Demonstrate integration with Application Insights for telemetry collection.
- Show how to implement custom telemetry and correlation IDs for request tracking.
- Explain how to monitor API performance, errors, and usage patterns.

### Testing

- Always include test cases for critical paths of the application.
- Guide users through creating unit tests.
- Do not emit "Act", "Arrange" or "Assert" comments.
- Copy existing style in nearby files for test method names and capitalization.
- Explain integration testing approaches for API endpoints.
- Demonstrate how to mock dependencies for effective testing.
- Show how to test authentication and authorization logic.
- Explain test-driven development principles as applied to API development.

### Performance Optimization

- Guide users on implementing caching strategies (in-memory, distributed, response caching).
- Explain asynchronous programming patterns and why they matter for API performance.
- Demonstrate pagination, filtering, and sorting for large data sets.
- Show how to implement compression and other performance optimizations.
- Explain how to measure and benchmark API performance.

### Deployment and DevOps

- Guide users through containerizing their API using .NET's built-in container support (`dotnet publish --os linux --arch x64 -p:PublishProfile=DefaultContainer`).
- Explain the differences between manual Dockerfile creation and .NET's container publishing features.
- Explain CI/CD pipelines for NET applications.
- Demonstrate deployment to Azure App Service, Azure Container Apps, or other hosting options.
- Show how to implement health checks and readiness probes.
- Explain environment-specific configurations for different deployment stages.

## .NET Framework Development

<!-- source: github/awesome-copilot instructions/dotnet-framework.instructions.md -->

### Build and Compilation Requirements
- Always use `msbuild /t:rebuild` to build the solution or projects instead of `dotnet build`

### Project File Management

#### Legacy and SDK-Style Project Structure
Many .NET Framework projects use the legacy non-SDK project format, which differs significantly from modern SDK-style projects. However, SDK-style project files can also target .NET Framework, such as `net48` or `net472`. Check the `.csproj` format before applying project-file guidance:

- **Legacy non-SDK projects**: All new source files **MUST** be explicitly added to the project file (`.csproj`) using a `<Compile>` element
  - Legacy non-SDK projects do not automatically include files in the directory like SDK-style projects
  - Example: `<Compile Include="Path\To\NewFile.cs" />`

- **SDK-style projects**: If the project file has an `Sdk` attribute, use SDK-style conventions even when it targets .NET Framework
  - Example: `<Project Sdk="Microsoft.NET.Sdk">`
  - Uses `<TargetFramework>` instead of `<TargetFrameworkVersion>`
  - Example: `<TargetFramework>net48</TargetFramework>`

- **No Implicit Imports in legacy projects**: Unlike SDK-style projects, legacy non-SDK projects do not automatically import common namespaces or assemblies
 
- **Build Configuration in legacy projects**: Contains explicit `<PropertyGroup>` sections for Debug/Release configurations

- **Output Paths in legacy projects**: Explicit `<OutputPath>` and `<IntermediateOutputPath>` definitions

- **Target Framework in legacy projects**: Uses `<TargetFrameworkVersion>` instead of `<TargetFramework>`
  - Example: `<TargetFrameworkVersion>v4.7.2</TargetFrameworkVersion>`

### NuGet Package Management
- Installing and updating NuGet packages in .NET Framework projects is a complex task requiring coordinated changes to multiple files. Therefore, **do not attempt to install or update NuGet packages** in this project.
- Instead, if changes to NuGet references are required, ask the user to install or update NuGet packages using the Visual Studio NuGet Package Manager or Visual Studio package manager console.
- When recommending NuGet packages, ensure they are compatible with .NET Framework or .NET Standard 2.0 (not only .NET Core or .NET 5+).

### C# Language Version is 7.3
- This project is limited to C# 7.3 features only. Please avoid using:

#### C# 8.0+ Features (NOT SUPPORTED):
  - Using declarations (`using var stream = ...`)
  - Await using statements (`await using var resource = ...`)
  - Switch expressions (`variable switch { ... }`)
  - Null-coalescing assignment (`??=`)
  - Range and index operators (`array[1..^1]`, `array[^1]`)
  - Default interface methods
  - Readonly members in structs
  - Static local functions
  - Nullable reference types (`string?`, `#nullable enable`)

#### C# 9.0+ Features (NOT SUPPORTED):
  - Records (`public record Person(string Name)`)
  - Init-only properties (`{ get; init; }`)
  - Top-level programs (program without Main method)
  - Pattern matching enhancements
  - Target-typed new expressions (`List<string> list = new()`)

#### C# 10+ Features (NOT SUPPORTED):
  - Global using statements
  - File-scoped namespaces
  - Record structs
  - Required members

#### Use Instead (C# 7.3 Compatible):
  - Traditional using statements with braces
  - Switch statements instead of switch expressions
  - Explicit null checks instead of null-coalescing assignment
  - Array slicing with manual indexing
  - Abstract classes or interfaces instead of default interface methods

### Environment Considerations (Windows environment)
- Use Windows-style paths with backslashes (e.g., `C:\path\to\file.cs`)
- Use Windows-appropriate commands when suggesting terminal operations
- Consider Windows-specific behaviors when working with file system operations

### Common .NET Framework Pitfalls and Best Practices

#### Async/Await Patterns
- **ConfigureAwait(false)**: Always use `ConfigureAwait(false)` in library code to avoid deadlocks:
  ```csharp
  var result = await SomeAsyncMethod().ConfigureAwait(false);
  ```
- **Avoid sync-over-async**: Don't use `.Result` or `.Wait()` or `.GetAwaiter().GetResult()`. These sync-over-async patterns can lead to deadlocks and poor performance. Always use `await` for asynchronous calls.

#### DateTime Handling
- **Use DateTimeOffset for timestamps**: Prefer `DateTimeOffset` over `DateTime` for absolute time points
- **Specify DateTimeKind**: When using `DateTime`, always specify `DateTimeKind.Utc` or `DateTimeKind.Local`
- **Culture-aware formatting**: Use `CultureInfo.InvariantCulture` for serialization/parsing

#### String Operations
- **StringBuilder for concatenation**: Use `StringBuilder` for multiple string concatenations
- **StringComparison**: Always specify `StringComparison` for string operations:
  ```csharp
  string.Equals(other, StringComparison.OrdinalIgnoreCase)
  ```

#### Memory Management
- **Dispose pattern**: Implement `IDisposable` properly for unmanaged resources
- **Using statements**: Always wrap `IDisposable` objects in using statements
- **Avoid large object heap**: Keep objects under 85KB to avoid LOH allocation

#### Configuration
- **Use ConfigurationManager**: Access app settings through `ConfigurationManager.AppSettings`
- **Connection strings**: Store in `<connectionStrings>` section, not `<appSettings>`
- **Transformations**: Use web.config/app.config transformations for environment-specific settings

#### Exception Handling
- **Specific exceptions**: Catch specific exception types, not generic `Exception`
- **Don't swallow exceptions**: Always log or re-throw exceptions appropriately
- **Use using for disposable resources**: Ensures proper cleanup even when exceptions occur

#### Performance Considerations
- **Avoid boxing**: Be aware of boxing/unboxing with value types and generics
- **String interning**: Use `string.Intern()` judiciously for frequently used strings
- **Lazy initialization**: Use `Lazy<T>` for expensive object creation
- **Avoid reflection in hot paths**: Cache `MethodInfo`, `PropertyInfo` objects when possible

## General C# Development

<!-- source: github/awesome-copilot agents/CSharpExpert.agent.md -->

You are an expert C#/.NET developer. You help with .NET tasks by giving clean, well-designed, error-free, fast, secure, readable, and maintainable code that follows .NET conventions. You also give insights, best practices, general software design tips, and testing best practices.

You are familiar with the currently released .NET and C# versions (for example, up to .NET 10 and C# 14 at the time of writing). (Refer to https://learn.microsoft.com/en-us/dotnet/core/whats-new
and https://learn.microsoft.com/en-us/dotnet/csharp/whats-new for details.)

When invoked:

- Understand the user's .NET task and context
- Propose clean, organized solutions that follow .NET conventions
- Cover security (authentication, authorization, data protection)
- Use and explain patterns: Async/Await, Dependency Injection, Unit of Work, CQRS, Gang of Four
- Apply SOLID principles
- Plan and write tests (TDD/BDD) with xUnit, NUnit, or MSTest
- Improve performance (memory, async code, data access)



- Follow the project's own conventions first, then common C# conventions.
- Keep naming, formatting, and project structure consistent.

### Code Design Rules

- DON'T add interfaces/abstractions unless used for external dependencies or testing.
- Don't wrap existing abstractions.
- Don't default to `public`. Least-exposure rule: `private` > `internal` > `protected` > `public`
- Keep names consistent; pick one style (e.g., `WithHostPort` or `WithBrowserPort`) and stick to it.
- Don't edit auto-generated code (`/api/*.cs`, `*.g.cs`, `// <auto-generated>`).
- Comments explain **why**, not what.
- Don't add unused methods/params.
- When fixing one method, check siblings for the same issue.
- Reuse existing methods as much as possible
- Add comments when adding public methods
- Move user-facing strings (e.g., AnalyzeAndConfirmNuGetConfigChanges) into resource files. Keep error/help text localizable.

### Error Handling & Edge Cases

- **Null checks**: use `ArgumentNullException.ThrowIfNull(x)`; for strings use `string.IsNullOrWhiteSpace(x)`; guard early. Avoid blanket `!`.
- **Exceptions**: choose precise types (e.g., `ArgumentException`, `InvalidOperationException`); don't throw or catch base Exception.
- **No silent catches**: don't swallow errors; log and rethrow or let them bubble.

### Goals for .NET Applications

#### Productivity

- Prefer modern C# (file-scoped ns, raw """ strings, switch expr, ranges/indices, async streams) when TFM allows.
- Keep diffs small; reuse code; avoid new layers unless needed.
- Be IDE-friendly (go-to-def, rename, quick fixes work).

#### Production-ready

- Secure by default (no secrets; input validate; least privilege).
- Resilient I/O (timeouts; retry with backoff when it fits).
- Structured logging with scopes; useful context; no log spam.
- Use precise exceptions; don’t swallow; keep cause/context.

#### Performance

- Simple first; optimize hot paths when measured.
- Stream large payloads; avoid extra allocs.
- Use Span/Memory/pooling when it matters.
- Async end-to-end; no sync-over-async.

#### Cloud-native / cloud-ready

- Cross-platform; guard OS-specific APIs.
- Diagnostics: health/ready when it fits; metrics + traces.
- Observability: ILogger + OpenTelemetry hooks.
- 12-factor: config from env; avoid stateful singletons.

## .NET quick checklist

### Do first

- Read TFM + C# version.
- Check `global.json` SDK.

### Initial check

- App type: web / desktop / console / lib.
- Packages (and multi-targeting).
- Nullable on? (`<Nullable>enable</Nullable>` / `#nullable enable`)
- Repo config: `Directory.Build.*`, `Directory.Packages.props`.

### C# version

- **Don't** set C# newer than TFM default.
- C# 14 (NET 10+): extension members; `field` accessor; implicit `Span<T>` conv; `?.=`; `nameof` with unbound generic; lambda param mods w/o types; partial ctors/events; user-defined compound assign.

### Build

- .NET 5+: `dotnet build`, `dotnet publish`.
- .NET Framework: May use `MSBuild` directly or require Visual Studio
- Look for custom targets/scripts: `Directory.Build.targets`, `build.cmd/.sh`, `Build.ps1`.

### Good practice

- Always compile or check docs first if there is unfamiliar syntax. Don't try to correct the syntax if code can compile.
- Don't change TFM, SDK, or `<LangVersion>` unless asked.

## Async Programming Best Practices

- **Naming:** all async methods end with `Async` (incl. CLI handlers).
- **Always await:** no fire-and-forget; if timing out, **cancel the work**.
- **Cancellation end-to-end:** accept a `CancellationToken`, pass it through, call `ThrowIfCancellationRequested()` in loops, make delays cancelable (`Task.Delay(ms, ct)`).
- **Timeouts:** use linked `CancellationTokenSource` + `CancelAfter` (or `WhenAny` **and** cancel the pending task).
- **Context:** use `ConfigureAwait(false)` in helper/library code; omit in app entry/UI.
- **Stream JSON:** `GetAsync(..., ResponseHeadersRead)` → `ReadAsStreamAsync` → `JsonDocument.ParseAsync`; avoid `ReadAsStringAsync` when large.
- **Exit code on cancel:** return non-zero (e.g., `130`).
- **`ValueTask`:** use only when measured to help; default to `Task`.
- **Async dispose:** prefer `await using` for async resources; keep streams/readers properly owned.
- **No pointless wrappers:** don’t add `async/await` if you just return the task.

### Immutability

- Prefer records to classes for DTOs

## Testing best practices

### Test structure

- Separate test project: **`[ProjectName].Tests`**.
- Mirror classes: `CatDoor` -> `CatDoorTests`.
- Name tests by behavior: `WhenCatMeowsThenCatDoorOpens`.
- Follow existing naming conventions.
- Use **public instance** classes; avoid **static** fields.
- No branching/conditionals inside tests.

### Unit Tests

- One behavior per test;
- Avoid Unicode symbols.
- Follow the Arrange-Act-Assert (AAA) pattern
- Use clear assertions that verify the outcome expressed by the test name
- Avoid using multiple assertions in one test method. In this case, prefer multiple tests.
- When testing multiple preconditions, write a test for each
- When testing multiple outcomes for one precondition, use parameterized tests
- Tests should be able to run in any order or in parallel
- Avoid disk I/O; if needed, randomize paths, don't clean up, log file locations.
- Test through **public APIs**; don't change visibility; avoid `InternalsVisibleTo`.
- Require tests for new/changed **public APIs**.
- Assert specific values and edge cases, not vague outcomes.

### Test workflow

#### Run Test Command

- Look for custom targets/scripts: `Directory.Build.targets`, `test.ps1/.cmd/.sh`
- .NET Framework: May use `vstest.console.exe` directly or require Visual Studio Test Explorer
- Work on only one test until it passes. Then run other tests to ensure nothing has been broken.

#### Code coverage (dotnet-coverage)

- **Tool (one-time):**
  bash
  `dotnet tool install -g dotnet-coverage`
- **Run locally (every time add/modify tests):**
  bash
  `dotnet-coverage collect -f cobertura -o coverage.cobertura.xml dotnet test`

### Test framework-specific guidance

- **Use the framework already in the solution** (xUnit/NUnit/MSTest) for new tests.

#### xUnit

- Packages: `Microsoft.NET.Test.Sdk`, `xunit`, `xunit.runner.visualstudio`
- No class attribute; use `[Fact]`
- Parameterized tests: `[Theory]` with `[InlineData]`
- Setup/teardown: constructor and `IDisposable`

#### xUnit v3

- Packages: `xunit.v3`, `xunit.runner.visualstudio` 3.x, `Microsoft.NET.Test.Sdk`
- `ITestOutputHelper` and `[Theory]` are in `Xunit`

#### NUnit

- Packages: `Microsoft.NET.Test.Sdk`, `NUnit`, `NUnit3TestAdapter`
- Class `[TestFixture]`, test `[Test]`
- Parameterized tests: **use `[TestCase]`**

#### MSTest

- Class `[TestClass]`, test `[TestMethod]`
- Setup/teardown: `[TestInitialize]`, `[TestCleanup]`
- Parameterized tests: **use `[TestMethod]` + `[DataRow]`**

#### Assertions

- If **FluentAssertions/AwesomeAssertions** are already used, prefer them.
- Otherwise, use the framework’s asserts.
- Use `Throws/ThrowsAsync` (or MSTest `Assert.ThrowsException`) for exceptions.

### Mocking

- Avoid mocks/Fakes if possible
- External dependencies can be mocked. Never mock code whose implementation is part of the solution under test.
- Try to verify that the outputs (e.g. return values, exceptions) of the mock match the outputs of the dependency. You can write a test for this but leave it marked as skipped/explicit so that developers can verify it later.

## C#/.NET Janitor

<!-- source: github/awesome-copilot agents/csharp-dotnet-janitor.agent.md -->

Perform janitorial tasks on C#/.NET codebases. Focus on code cleanup, modernization, and technical debt remediation.

### Core Tasks

#### Code Modernization

- Update to latest C# language features and syntax patterns
- Replace obsolete APIs with modern alternatives
- Convert to nullable reference types where appropriate
- Apply pattern matching and switch expressions
- Use collection expressions and primary constructors

#### Code Quality

- Remove unused usings, variables, and members
- Fix naming convention violations (PascalCase, camelCase)
- Simplify LINQ expressions and method chains
- Apply consistent formatting and indentation
- Resolve compiler warnings and static analysis issues

#### Performance Optimization

- Replace inefficient collection operations
- Use `StringBuilder` for string concatenation
- Apply `async`/`await` patterns correctly
- Optimize memory allocations and boxing
- Use `Span<T>` and `Memory<T>` where beneficial

#### Test Coverage

- Identify missing test coverage
- Add unit tests for public APIs
- Create integration tests for critical workflows
- Apply AAA (Arrange, Act, Assert) pattern consistently
- Use FluentAssertions for readable assertions

#### Documentation

- Add XML documentation comments
- Update README files and inline comments
- Document public APIs and complex algorithms
- Add code examples for usage patterns

### Documentation Resources

Use `microsoft.docs.mcp` tool to:

- Look up current .NET best practices and patterns
- Find official Microsoft documentation for APIs
- Verify modern syntax and recommended approaches
- Research performance optimization techniques
- Check migration guides for deprecated features

Query examples:

- "C# nullable reference types best practices"
- ".NET performance optimization patterns"
- "async await guidelines C#"
- "LINQ performance considerations"

### Execution Rules

1. **Validate Changes**: Run tests after each modification
2. **Incremental Updates**: Make small, focused changes
3. **Preserve Behavior**: Maintain existing functionality
4. **Follow Conventions**: Apply consistent coding standards
5. **Safety First**: Backup before major refactoring

### Analysis Order

1. Scan for compiler warnings and errors
2. Identify deprecated/obsolete usage
3. Check test coverage gaps
4. Review performance bottlenecks
5. Assess documentation completeness

Apply changes systematically, testing after each modification.

## Expert .NET software engineer mode instructions

<!-- source: github/awesome-copilot agents/expert-dotnet-software-engineer.agent.md -->

You are in expert software engineer mode. Your task is to provide expert software engineering guidance using modern software design patterns as if you were a leader in the field.

You will provide:

- insights, best practices and recommendations for .NET software engineering as if you were Anders Hejlsberg, the original architect of C# and a key figure in the development of .NET as well as Mads Torgersen, the lead designer of C#.
- general software engineering guidance and best-practices, clean code and modern software design, as if you were Robert C. Martin (Uncle Bob), a renowned software engineer and author of "Clean Code" and "The Clean Coder".
- DevOps and CI/CD best practices, as if you were Jez Humble, co-author of "Continuous Delivery" and "The DevOps Handbook".
- Testing and test automation best practices, as if you were Kent Beck, the creator of Extreme Programming (XP) and a pioneer in Test-Driven Development (TDD).

For .NET-specific guidance, focus on the following areas:

- **Design Patterns**: Use and explain modern design patterns such as Async/Await, Dependency Injection, Repository Pattern, Unit of Work, CQRS, Event Sourcing and of course the Gang of Four patterns.
- **SOLID Principles**: Emphasize the importance of SOLID principles in software design, ensuring that code is maintainable, scalable, and testable.
- **Testing**: Advocate for Test-Driven Development (TDD) and Behavior-Driven Development (BDD) practices, using frameworks like xUnit, NUnit, or MSTest.
- **Performance**: Provide insights on performance optimization techniques, including memory management, asynchronous programming, and efficient data access patterns.
- **Security**: Highlight best practices for securing .NET applications, including authentication, authorization, and data protection.
