# Simplification — derived guides

Part of `code-quality:simplification`.

## Refactor

<!-- source: github/awesome-copilot skills/refactor/SKILL.md#common-code-smells-fixes -->

### Common Code Smells & Fixes

#### 1. Long Method/Function

```diff
# BAD: 200-line function that does everything
- async function processOrder(orderId) {
-   // 50 lines: fetch order
-   // 30 lines: validate order
-   // 40 lines: calculate pricing
-   // 30 lines: update inventory
-   // 20 lines: create shipment
-   // 30 lines: send notifications
- }

# GOOD: Broken into focused functions
+ async function processOrder(orderId) {
+   const order = await fetchOrder(orderId);
+   validateOrder(order);
+   const pricing = calculatePricing(order);
+   await updateInventory(order);
+   const shipment = await createShipment(order);
+   await sendNotifications(order, pricing, shipment);
+   return { order, pricing, shipment };
+ }
```

#### 2. Duplicated Code

```diff
# BAD: Same logic in multiple places
- function calculateUserDiscount(user) {
-   if (user.membership === 'gold') return user.total * 0.2;
-   if (user.membership === 'silver') return user.total * 0.1;
-   return 0;
- }
-
- function calculateOrderDiscount(order) {
-   if (order.user.membership === 'gold') return order.total * 0.2;
-   if (order.user.membership === 'silver') return order.total * 0.1;
-   return 0;
- }

# GOOD: Extract common logic
+ function getMembershipDiscountRate(membership) {
+   const rates = { gold: 0.2, silver: 0.1 };
+   return rates[membership] || 0;
+ }
+
+ function calculateUserDiscount(user) {
+   return user.total * getMembershipDiscountRate(user.membership);
+ }
+
+ function calculateOrderDiscount(order) {
+   return order.total * getMembershipDiscountRate(order.user.membership);
+ }
```

#### 3. Large Class/Module

```diff
# BAD: God object that knows too much
- class UserManager {
-   createUser() { /* ... */ }
-   updateUser() { /* ... */ }
-   deleteUser() { /* ... */ }
-   sendEmail() { /* ... */ }
-   generateReport() { /* ... */ }
-   handlePayment() { /* ... */ }
-   validateAddress() { /* ... */ }
-   // 50 more methods...
- }

# GOOD: Single responsibility per class
+ class UserService {
+   create(data) { /* ... */ }
+   update(id, data) { /* ... */ }
+   delete(id) { /* ... */ }
+ }
+
+ class EmailService {
+   send(to, subject, body) { /* ... */ }
+ }
+
+ class ReportService {
+   generate(type, params) { /* ... */ }
+ }
+
+ class PaymentService {
+   process(amount, method) { /* ... */ }
+ }
```

#### 4. Long Parameter List

```diff
# BAD: Too many parameters
- function createUser(email, password, name, age, address, city, country, phone) {
-   /* ... */
- }

# GOOD: Group related parameters
+ interface UserData {
+   email: string;
+   password: string;
+   name: string;
+   age?: number;
+   address?: Address;
+   phone?: string;
+ }
+
+ function createUser(data: UserData) {
+   /* ... */
+ }

# EVEN BETTER: Use builder pattern for complex construction
+ const user = UserBuilder
+   .email('test@example.com')
+   .password('secure123')
+   .name('Test User')
+   .address(address)
+   .build();
```

#### 5. Feature Envy

```diff
# BAD: Method that uses another object's data more than its own
- class Order {
-   calculateDiscount(user) {
-     if (user.membershipLevel === 'gold') {
+       return this.total * 0.2;
+     }
+     if (user.accountAge > 365) {
+       return this.total * 0.1;
+     }
+     return 0;
+   }
+ }

# GOOD: Move logic to the object that owns the data
+ class User {
+   getDiscountRate(orderTotal) {
+     if (this.membershipLevel === 'gold') return 0.2;
+     if (this.accountAge > 365) return 0.1;
+     return 0;
+   }
+ }
+
+ class Order {
+   calculateDiscount(user) {
+     return this.total * user.getDiscountRate(this.total);
+   }
+ }
```

#### 6. Primitive Obsession

```diff
# BAD: Using primitives for domain concepts
- function sendEmail(to, subject, body) { /* ... */ }
- sendEmail('user@example.com', 'Hello', '...');

- function createPhone(country, number) {
-   return `${country}-${number}`;
- }

# GOOD: Use domain types
+ class Email {
+   private constructor(public readonly value: string) {
+     if (!Email.isValid(value)) throw new Error('Invalid email');
+   }
+   static create(value: string) { return new Email(value); }
+   static isValid(email: string) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email); }
+ }
+
+ class PhoneNumber {
+   constructor(
+     public readonly country: string,
+     public readonly number: string
+   ) {
+     if (!PhoneNumber.isValid(country, number)) throw new Error('Invalid phone');
+   }
+   toString() { return `${this.country}-${this.number}`; }
+   static isValid(country: string, number: string) { /* ... */ }
+ }
+
+ // Usage
+ const email = Email.create('user@example.com');
+ const phone = new PhoneNumber('1', '555-1234');
```

#### 7. Magic Numbers/Strings

```diff
# BAD: Unexplained values
- if (user.status === 2) { /* ... */ }
- const discount = total * 0.15;
- setTimeout(callback, 86400000);

# GOOD: Named constants
+ const UserStatus = {
+   ACTIVE: 1,
+   INACTIVE: 2,
+   SUSPENDED: 3
+ } as const;
+
+ const DISCOUNT_RATES = {
+   STANDARD: 0.1,
+   PREMIUM: 0.15,
+   VIP: 0.2
+ } as const;
+
+ const ONE_DAY_MS = 24 * 60 * 60 * 1000;
+
+ if (user.status === UserStatus.INACTIVE) { /* ... */ }
+ const discount = total * DISCOUNT_RATES.PREMIUM;
+ setTimeout(callback, ONE_DAY_MS);
```

#### 8. Nested Conditionals

```diff
# BAD: Arrow code
- function process(order) {
-   if (order) {
-     if (order.user) {
-       if (order.user.isActive) {
-         if (order.total > 0) {
-           return processOrder(order);
+         } else {
+           return { error: 'Invalid total' };
+         }
+       } else {
+         return { error: 'User inactive' };
+       }
+     } else {
+       return { error: 'No user' };
+     }
+   } else {
+     return { error: 'No order' };
+   }
+ }

# GOOD: Guard clauses / early returns
+ function process(order) {
+   if (!order) return { error: 'No order' };
+   if (!order.user) return { error: 'No user' };
+   if (!order.user.isActive) return { error: 'User inactive' };
+   if (order.total <= 0) return { error: 'Invalid total' };
+   return processOrder(order);
+ }

# EVEN BETTER: Using Result type
+ function process(order): Result<ProcessedOrder, Error> {
+   return Result.combine([
+     validateOrderExists(order),
+     validateUserExists(order),
+     validateUserActive(order.user),
+     validateOrderTotal(order)
+   ]).flatMap(() => processOrder(order));
+ }
```

#### 9. Dead Code

```diff
# BAD: Unused code lingers
- function oldImplementation() { /* ... */ }
- const DEPRECATED_VALUE = 5;
- import { unusedThing } from './somewhere';
- // Commented out code
- // function oldCode() { /* ... */ }

# GOOD: Remove it
+ // Delete unused functions, imports, and commented code
+ // If you need it again, git history has it
```

#### 10. Inappropriate Intimacy

```diff
# BAD: One class reaches deep into another
- class OrderProcessor {
-   process(order) {
-     order.user.profile.address.street;  // Too intimate
-     order.repository.connection.config;  // Breaking encapsulation
+   }
+ }

# GOOD: Ask, don't tell
+ class OrderProcessor {
+   process(order) {
+     order.getShippingAddress();  // Order knows how to get it
+     order.save();  // Order knows how to save itself
+   }
+ }
```

---

## Write Coding Standards From File

<!-- source: github/awesome-copilot skills/write-coding-standards-from-file/SKILL.md#variable-and-parameter-configuration-conditions -->

### Variable and Parameter Configuration Conditions

#### `${fileName}.length > 1 || ${folderName} != undefined`

* If true, toggle `${fixInconsistencies}` to false.

#### `${addToREADME} == true`

* Insert the coding standards into the `README.md` instead of outputting to the prompt or creating a new file.
* If true, toggle both `${createNewFile}` and `${outputSpecToPrompt}` to false.

#### `${addToREADMEInsertions} == "atBegin"`

* If `${addToREADME}` is true, then insert the coding standards data at the **beginning** of the `README.md` file after the title.

#### `${addToREADMEInsertions} == "middle"`

* If `${addToREADME}` is true, then insert the coding standards data at the **middle** of the `README.md` file, changing the standards title heading to match that of the `README.md` composition.

#### `${addToREADMEInsertions} == "beforeEnd"`

* If `${addToREADME}` is true, then insert the coding standards data at the **end** of the `README.md` file, inserting a new line after the last character, then inserting the data on a new line.

#### `${addToREADMEInsertions} == "bestFitUsingContext"`

* If `${addToREADME}` is true, then insert the coding standards data at the **best fitting line** of the `README.md` file in regards to the context of the `README.md` composition and flow of data.

#### `${addStandardsTest} == true`

* Once the coding standards file is complete, write a test file to ensure the file or files passed to it adhere to the coding standards.

#### `${createNewFile} == true`

* Create a new file using the value, or one of the possible values, from `${newFileName}`.
* If true, toggle both `${outputSpecToPrompt}` and `${addToREADME}` to false.

#### `${fetchStyleURL} == true`

* Additionally use the data fetched from the links nested under level three heading `### Fetch Links` as context for creating standards, specifications, and styling data for the new file, prompt, or `README.md`.
* For each relevant item in `### Fetch Links`, run `#fetch ${item}`.

#### `${findInconsistencies} == true`

* Evaluate syntax related to indentations, line-breaks, comments, conditional and function nesting, quotation wrappers i.e. `'` or `"` for strings, etc., and categorize.
* For each category, make a count, and if one item does not match the majority of the count, then commit to temporary memory.
* Depending on the status of `${fixInconsistencies}`, either edit and fix the low count categories to match the majority, or output to prompt inconsistencies stored in temporary memory.

#### `${fixInconsistencies} == true`

* Edit and fix the low count categories of syntax data to match the majority of corresponding syntax data using inconsistencies stored in temporary memory.

#### `typeof ${newFileName} == "string"`

* If specifically defined as a `string`, create a new file using the value from `${newFileName}`.

#### `typeof ${newFileName} != "string"`

* If **NOT** specifically defined as a `string`, but instead an `object` or an array, create a new file using a value from `${newFileName}` by applying this rule:
  - For each file name in `${newFileName}`, if file does not exist, use that file name and `break`, else continue to the next.

#### `${outputSpecToPrompt} == true`

* Output the coding standards to the prompt instead of creating a file or adding to README.
* If true, toggle both `${createNewFile}` and `${addToREADME}` to false.

#### `${useTemplate} == "v" || ${useTemplate} == "verbose"`

* Use data under the level three heading `### "v", "verbose"` as guiding template when composing the data for coding standards.

#### `${useTemplate} == "m" || ${useTemplate} == "minimal"`

* Use data under the level three heading `### "m", "minimal"` as guiding template when composing the data for coding standards.

#### `${useTemplate} == "b" || ${useTemplate} == "best"`

* Use either the data under the level three heading `### "v", "verbose"` or `### "m", "minimal"`, depending on the data extracted from `${fileName}`, and use the best fit as guiding template when composing the data for coding standards.

#### `${useTemplate} == "custom" || ${useTemplate} == "<ANY_NAME>"`

* Use the custom prompt, instructions, template, or other data passed as guiding template when composing the data for coding standards.

## Python Code Style & Documentation

<!-- source: wshobson/agents plugins/python-development/skills/python-code-style/SKILL.md#advanced-patterns -->

### Advanced Patterns

#### Pattern 5: Google-Style Docstrings

Write docstrings for all public classes, methods, and functions.

**Simple Function:**

```python
def get_user(user_id: str) -> User:
    """Retrieve a user by their unique identifier."""
    ...
```

**Complex Function:**

```python
def process_batch(
    items: list[Item],
    max_workers: int = 4,
    on_progress: Callable[[int, int], None] | None = None,
) -> BatchResult:
    """Process items concurrently using a worker pool.

    Processes each item in the batch using the configured number of
    workers. Progress can be monitored via the optional callback.

    Args:
        items: The items to process. Must not be empty.
        max_workers: Maximum concurrent workers. Defaults to 4.
        on_progress: Optional callback receiving (completed, total) counts.

    Returns:
        BatchResult containing succeeded items and any failures with
        their associated exceptions.

    Raises:
        ValueError: If items is empty.
        ProcessingError: If the batch cannot be processed.

    Example:
        >>> result = process_batch(items, max_workers=8)
        >>> print(f"Processed {len(result.succeeded)} items")
    """
    ...
```

**Class Docstring:**

```python
class UserService:
    """Service for managing user operations.

    Provides methods for creating, retrieving, updating, and
    deleting users with proper validation and error handling.

    Attributes:
        repository: The data access layer for user persistence.
        logger: Logger instance for operation tracking.

    Example:
        >>> service = UserService(repository, logger)
        >>> user = service.create_user(CreateUserInput(...))
    """

    def __init__(self, repository: UserRepository, logger: Logger) -> None:
        """Initialize the user service.

        Args:
            repository: Data access layer for users.
            logger: Logger for tracking operations.
        """
        self.repository = repository
        self.logger = logger
```

#### Pattern 6: Line Length and Formatting

Set line length to 120 characters for modern displays while maintaining readability.

```python
# Good: Readable line breaks
def create_user(
    email: str,
    name: str,
    role: UserRole = UserRole.MEMBER,
    notify: bool = True,
) -> User:
    ...

# Good: Chain method calls clearly
result = (
    db.query(User)
    .filter(User.active == True)
    .order_by(User.created_at.desc())
    .limit(10)
    .all()
)

# Good: Format long strings
error_message = (
    f"Failed to process user {user_id}: "
    f"received status {response.status_code} "
    f"with body {response.text[:100]}"
)
```

#### Pattern 7: Project Documentation

**README Structure:**

```markdown
# Project Name

Brief description of what the project does.

## Installation

\`\`\`bash
pip install myproject
\`\`\`

## Quick Start

\`\`\`python
from myproject import Client

client = Client(api_key="...")
result = client.process(data)
\`\`\`

## Configuration

Document environment variables and configuration options.

## Development

\`\`\`bash
pip install -e ".[dev]"
pytest
\`\`\`
```

**CHANGELOG Format (Keep a Changelog):**

```markdown
# Changelog

## [Unreleased]

### Added
- New feature X

### Changed
- Modified behavior of Y

### Fixed
- Bug in Z
```

## Technical Debt Manager

<!-- source: davila7/claude-code-templates cli-tool/components/agents/development-tools/technical-debt-manager.md#technical-debt-categories -->

### Technical Debt Categories

#### 1. Code Quality Debt
**Detection Methods:**
- Cyclomatic complexity > 15 (functions should be < 10)
- Code duplication > 3% (industry standard < 5%)
- Long functions/classes (> 200 lines indicates poor separation of concerns)
- Deep nesting levels (> 4 levels suggests refactoring needed)
- God objects (classes with > 10 responsibilities)
- Feature envy (excessive method calls to other classes)

**Tools:**
- Language-specific linters (ESLint, Pylint, RuboCop)
- Complexity analyzers (radon, lizard, SonarQube)
- Duplication detectors (jscpd, PMD CPD)

#### 2. Test Debt
**Detection Methods:**
- Test coverage < 80% (critical paths must be 100%)
- Missing integration/e2e tests
- Flaky tests (intermittent failures)
- Test execution time > 10 minutes
- Brittle tests (coupled to implementation details)
- Lack of test documentation

**Tools:**
- Coverage reporters (Jest, pytest-cov, SimpleCov)
- Test quality analyzers (mutation testing with Stryker, PITest)
- CI/CD pipeline metrics

#### 3. Documentation Debt
**Detection Methods:**
- Missing README or outdated setup instructions
- Undocumented APIs (missing OpenAPI/Swagger specs)
- No architecture decision records (ADRs)
- Commented-out code blocks
- TODOs/FIXMEs without issue tracking
- Missing inline documentation for complex logic

**Tools:**
- Documentation coverage tools (documentation.js, Sphinx)
- TODO trackers (Leasot, todo-or-die)
- Link checkers (markdown-link-check)

#### 4. Dependency Debt
**Detection Methods:**
- Packages > 2 major versions behind
- Known CVEs (security vulnerabilities)
- Deprecated dependencies
- Unused dependencies (dead imports)
- License compliance issues
- Transitive dependency conflicts

**Tools:**
- npm audit, yarn audit, pip-audit
- Snyk, Dependabot, Renovate
- License scanners (FOSSA, license-checker)
- Dependency analyzers (depcheck, pip-autoremove)

#### 5. Design Debt
**Detection Methods:**
- Circular dependencies between modules
- Tight coupling (high fan-in/fan-out)
- Missing abstraction layers
- Violation of SOLID principles
- Inconsistent design patterns
- Monolithic architectures resisting change

**Tools:**
- Dependency analyzers (Madge, deptree, graphviz)
- Architecture linters (ArchUnit, dependency-cruiser)
- Code complexity visualizers

#### 6. Infrastructure Debt
**Detection Methods:**
- Outdated runtime versions (Node.js, Python, Ruby)
- Missing CI/CD pipelines
- Manual deployment processes
- Lack of infrastructure as code (IaC)
- Missing monitoring/observability
- No disaster recovery plan

**Tools:**
- Container scanners (Trivy, Grype)
- IaC validators (Terraform validate, CloudFormation linter)
- Security scanners (OWASP ZAP, Bandit)

#### 7. Performance Debt
**Detection Methods:**
- N+1 database queries
- Missing database indexes
- Unoptimized asset bundles
- Memory leaks
- Blocking I/O operations
- Missing caching layers

**Tools:**
- Profilers (clinic.js, py-spy, ruby-prof)
- Database query analyzers (EXPLAIN, pg_stat_statements)
- Bundle analyzers (webpack-bundle-analyzer, source-map-explorer)
