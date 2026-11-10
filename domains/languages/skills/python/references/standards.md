# Python — Standards and idioms

Part of `languages:python`. Load when writing or refactoring code: style, idioms, patterns, project layout.

## Python Coding Style

<!-- source: affaan-m/ECC rules/python/coding-style.md -->

> This file extends common/coding-style.md with Python specific content.

### Standards

- Follow **PEP 8** conventions
- Use **type annotations** on all function signatures

### Immutability

Prefer immutable data structures:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    name: str
    email: str

from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float
```

### Formatting

- **black** for code formatting
- **isort** for import sorting
- **ruff** for linting

### Reference

See skill: `languages:python` (`references/standards.md`) for comprehensive Python idioms and patterns.

## Python Patterns

<!-- source: affaan-m/ECC rules/python/patterns.md -->

> This file extends common/patterns.md with Python specific content.

### Protocol (Duck Typing)

```python
from typing import Protocol

class Repository(Protocol):
    def find_by_id(self, id: str) -> dict | None: ...
    def save(self, entity: dict) -> dict: ...
```

### Dataclasses as DTOs

```python
from dataclasses import dataclass

@dataclass
class CreateUserRequest:
    name: str
    email: str
    age: int | None = None
```

### Context Managers & Generators

- Use context managers (`with` statement) for resource management
- Use generators for lazy evaluation and memory-efficient iteration

### Reference

See skill: `languages:python` (`references/standards.md`) for comprehensive patterns including decorators, concurrency, and package organization.

## Python Development Patterns

<!-- source: affaan-m/ECC pi/core/skills/python-patterns/SKILL.md -->

Idiomatic Python patterns and best practices for building robust, efficient, and maintainable applications.

### When to Activate

- Writing new Python code
- Reviewing Python code
- Refactoring existing Python code
- Designing Python packages/modules

### Core Principles

#### 1. Readability Counts

Python prioritizes readability. Code should be obvious and easy to understand.

```python
# Good: Clear and readable
def get_active_users(users: list[User]) -> list[User]:
    """Return only active users from the provided list."""
    return [user for user in users if user.is_active]


# Bad: Clever but confusing
def get_active_users(u):
    return [x for x in u if x.a]
```

#### 2. Explicit is Better Than Implicit

Avoid magic; be clear about what your code does.

```python
# Good: Explicit configuration
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Bad: Hidden side effects
import some_module
some_module.setup()  # What does this do?
```

#### 3. EAFP - Easier to Ask Forgiveness Than Permission

Python prefers exception handling over checking conditions.

```python
# Good: EAFP style
def get_value(dictionary: dict, key: str, default_value: Any = None) -> Any:
    try:
        return dictionary[key]
    except KeyError:
        return default_value

# Bad: LBYL (Look Before You Leap) style
def get_value(dictionary: dict, key: str, default_value: Any = None) -> Any:
    if key in dictionary:
        return dictionary[key]
    else:
        return default_value
```

### Type Hints

#### Basic Type Annotations

```python
from typing import Optional, List, Dict, Any

def process_user(
    user_id: str,
    data: Dict[str, Any],
    active: bool = True
) -> Optional[User]:
    """Process a user and return the updated User or None."""
    if not active:
        return None
    return User(user_id, data)
```

#### Modern Type Hints (Python 3.9+)

```python
# Python 3.9+ - Use built-in types
def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# Python 3.8 and earlier - Use typing module
from typing import List, Dict

def process_items(items: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in items}
```

#### Type Aliases and TypeVar

```python
from typing import TypeVar, Union

# Type alias for complex types
JSON = Union[dict[str, Any], list[Any], str, int, float, bool, None]

def parse_json(data: str) -> JSON:
    return json.loads(data)

# Generic types
T = TypeVar('T')

def first(items: list[T]) -> T | None:
    """Return the first item or None if list is empty."""
    return items[0] if items else None
```

#### Protocol-Based Duck Typing

```python
from typing import Protocol

class Renderable(Protocol):
    def render(self) -> str:
        """Render the object to a string."""

def render_all(items: list[Renderable]) -> str:
    """Render all items that implement the Renderable protocol."""
    return "\n".join(item.render() for item in items)
```

### Error Handling Patterns

#### Specific Exception Handling

```python
# Good: Catch specific exceptions
def load_config(path: str) -> Config:
    try:
        with open(path) as f:
            return Config.from_json(f.read())
    except FileNotFoundError as e:
        raise ConfigError(f"Config file not found: {path}") from e
    except json.JSONDecodeError as e:
        raise ConfigError(f"Invalid JSON in config: {path}") from e

# Bad: Bare except
def load_config(path: str) -> Config:
    try:
        with open(path) as f:
            return Config.from_json(f.read())
    except:
        return None  # Silent failure!
```

#### Exception Chaining

```python
def process_data(data: str) -> Result:
    try:
        parsed = json.loads(data)
    except json.JSONDecodeError as e:
        # Chain exceptions to preserve the traceback
        raise ValueError(f"Failed to parse data: {data}") from e
```

#### Custom Exception Hierarchy

```python
class AppError(Exception):
    """Base exception for all application errors."""
    pass

class ValidationError(AppError):
    """Raised when input validation fails."""
    pass

class NotFoundError(AppError):
    """Raised when a requested resource is not found."""
    pass

# Usage
def get_user(user_id: str) -> User:
    user = db.find_user(user_id)
    if not user:
        raise NotFoundError(f"User not found: {user_id}")
    return user
```

### Context Managers

#### Resource Management

```python
# Good: Using context managers
def process_file(path: str) -> str:
    with open(path, 'r') as f:
        return f.read()

# Bad: Manual resource management
def process_file(path: str) -> str:
    f = open(path, 'r')
    try:
        return f.read()
    finally:
        f.close()
```

#### Custom Context Managers

```python
from contextlib import contextmanager

@contextmanager
def timer(name: str):
    """Context manager to time a block of code."""
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    print(f"{name} took {elapsed:.4f} seconds")

# Usage
with timer("data processing"):
    process_large_dataset()
```

#### Context Manager Classes

```python
class DatabaseTransaction:
    def __init__(self, connection):
        self.connection = connection

    def __enter__(self):
        self.connection.begin_transaction()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        return False  # Don't suppress exceptions

# Usage
with DatabaseTransaction(conn):
    user = conn.create_user(user_data)
    conn.create_profile(user.id, profile_data)
```

### Comprehensions and Generators

#### List Comprehensions

```python
# Good: List comprehension for simple transformations
names = [user.name for user in users if user.is_active]

# Bad: Manual loop
names = []
for user in users:
    if user.is_active:
        names.append(user.name)

# Complex comprehensions should be expanded
# Bad: Too complex
result = [x * 2 for x in items if x > 0 if x % 2 == 0]

# Good: Use a generator function
def filter_and_transform(items: Iterable[int]) -> list[int]:
    result = []
    for x in items:
        if x > 0 and x % 2 == 0:
            result.append(x * 2)
    return result
```

#### Generator Expressions

```python
# Good: Generator for lazy evaluation
total = sum(x * x for x in range(1_000_000))

# Bad: Creates large intermediate list
total = sum([x * x for x in range(1_000_000)])
```

#### Generator Functions

```python
def read_large_file(path: str) -> Iterator[str]:
    """Read a large file line by line."""
    with open(path) as f:
        for line in f:
            yield line.strip()

# Usage
for line in read_large_file("huge.txt"):
    process(line)
```

### Data Classes and Named Tuples

#### Data Classes

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class User:
    """User entity with automatic __init__, __repr__, and __eq__."""
    id: str
    name: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True

# Usage
user = User(
    id="123",
    name="Alice",
    email="alice@example.com"
)
```

#### Data Classes with Validation

```python
@dataclass
class User:
    email: str
    age: int

    def __post_init__(self):
        # Validate email format
        if "@" not in self.email:
            raise ValueError(f"Invalid email: {self.email}")
        # Validate age range
        if self.age < 0 or self.age > 150:
            raise ValueError(f"Invalid age: {self.age}")
```

#### Named Tuples

```python
from typing import NamedTuple

class Point(NamedTuple):
    """Immutable 2D point."""
    x: float
    y: float

    def distance(self, other: 'Point') -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

# Usage
p1 = Point(0, 0)
p2 = Point(3, 4)
print(p1.distance(p2))  # 5.0
```

### Decorators

#### Function Decorators

```python
import functools
import time

def timer(func: Callable) -> Callable:
    """Decorator to time function execution."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)

# slow_function() prints: slow_function took 1.0012s
```

#### Parameterized Decorators

```python
def repeat(times: int):
    """Decorator to repeat a function multiple times."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

@repeat(times=3)
def greet(name: str) -> str:
    return f"Hello, {name}!"

# greet("Alice") returns ["Hello, Alice!", "Hello, Alice!", "Hello, Alice!"]
```

#### Class-Based Decorators

```python
class CountCalls:
    """Decorator that counts how many times a function is called."""
    def __init__(self, func: Callable):
        functools.update_wrapper(self, func)
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"{self.func.__name__} has been called {self.count} times")
        return self.func(*args, **kwargs)

@CountCalls
def process():
    pass

# Each call to process() prints the call count
```

### Concurrency Patterns

#### Threading for I/O-Bound Tasks

```python
import concurrent.futures
import threading

def fetch_url(url: str) -> str:
    """Fetch a URL (I/O-bound operation)."""
    import urllib.request
    with urllib.request.urlopen(url) as response:
        return response.read().decode()

def fetch_all_urls(urls: list[str]) -> dict[str, str]:
    """Fetch multiple URLs concurrently using threads."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(fetch_url, url): url for url in urls}
        results = {}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                results[url] = future.result()
            except Exception as e:
                results[url] = f"Error: {e}"
    return results
```

#### Multiprocessing for CPU-Bound Tasks

```python
def process_data(data: list[int]) -> int:
    """CPU-intensive computation."""
    return sum(x ** 2 for x in data)

def process_all(datasets: list[list[int]]) -> list[int]:
    """Process multiple datasets using multiple processes."""
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(process_data, datasets))
    return results
```

#### Async/Await for Concurrent I/O

```python
import asyncio

async def fetch_async(url: str) -> str:
    """Fetch a URL asynchronously."""
    import aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def fetch_all(urls: list[str]) -> dict[str, str]:
    """Fetch multiple URLs concurrently."""
    tasks = [fetch_async(url) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return dict(zip(urls, results))
```

### Package Organization

#### Standard Project Layout

```
myproject/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── main.py
│       ├── api/
│       │   ├── __init__.py
│       │   └── routes.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── user.py
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api.py
│   └── test_models.py
├── pyproject.toml
├── README.md
└── .gitignore
```

#### Import Conventions

```python
# Good: Import order - stdlib, third-party, local
import os
import sys
from pathlib import Path

import requests
from fastapi import FastAPI

from mypackage.models import User
from mypackage.utils import format_name

# Good: Use isort for automatic import sorting
# pip install isort
```

#### __init__.py for Package Exports

```python
# mypackage/__init__.py
"""mypackage - A sample Python package."""

__version__ = "1.0.0"

# Export main classes/functions at package level
from mypackage.models import User, Post
from mypackage.utils import format_name

__all__ = ["User", "Post", "format_name"]
```

### Memory and Performance

#### Using __slots__ for Memory Efficiency

```python
# Bad: Regular class uses __dict__ (more memory)
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

# Good: __slots__ reduces memory usage
class Point:
    __slots__ = ['x', 'y']

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
```

#### Generator for Large Data

```python
# Bad: Returns full list in memory
def read_lines(path: str) -> list[str]:
    with open(path) as f:
        return [line.strip() for line in f]

# Good: Yields lines one at a time
def read_lines(path: str) -> Iterator[str]:
    with open(path) as f:
        for line in f:
            yield line.strip()
```

#### Avoid String Concatenation in Loops

```python
# Bad: O(n²) due to string immutability
result = ""
for item in items:
    result += str(item)

# Good: O(n) using join
result = "".join(str(item) for item in items)

# Good: Using StringIO for building
from io import StringIO

buffer = StringIO()
for item in items:
    buffer.write(str(item))
result = buffer.getvalue()
```

### Python Tooling Integration

#### Essential Commands

```bash
# Code formatting
black .
isort .

# Linting
ruff check .
pylint mypackage/

# Type checking
mypy .

# Testing
pytest --cov=mypackage --cov-report=html

# Security scanning
bandit -r .

# Dependency management
pip-audit
safety check
```

#### pyproject.toml Configuration

```toml
[project]
name = "mypackage"
version = "1.0.0"
requires-python = ">=3.9"
dependencies = [
    "requests>=2.31.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.5.0",
]

[tool.black]
line-length = 88
target-version = ['py39']

[tool.ruff]
line-length = 88
select = ["E", "F", "I", "N", "W"]

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=mypackage --cov-report=term-missing"
```

### Quick Reference: Python Idioms

| Idiom | Description |
|-------|-------------|
| EAFP | Easier to Ask Forgiveness than Permission |
| Context managers | Use `with` for resource management |
| List comprehensions | For simple transformations |
| Generators | For lazy evaluation and large datasets |
| Type hints | Annotate function signatures |
| Dataclasses | For data containers with auto-generated methods |
| `__slots__` | For memory optimization |
| f-strings | For string formatting (Python 3.6+) |
| `pathlib.Path` | For path operations (Python 3.4+) |
| `enumerate` | For index-element pairs in loops |

### Anti-Patterns to Avoid

```python
# Bad: Mutable default arguments
def append_to(item, items=[]):
    items.append(item)
    return items

# Good: Use None and create new list
def append_to(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

# Bad: Checking type with type()
if type(obj) == list:
    process(obj)

# Good: Use isinstance
if isinstance(obj, list):
    process(obj)

# Bad: Comparing to None with ==
if value == None:
    process()

# Good: Use is
if value is None:
    process()

# Bad: from module import *
from os.path import *

# Good: Explicit imports
from os.path import join, exists

# Bad: Bare except
try:
    risky_operation()
except:
    pass

# Good: Specific exception
try:
    risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
```

__Remember__: Python code should be readable, explicit, and follow the principle of least surprise. When in doubt, prioritize clarity over cleverness.

## Python Resilience Patterns

<!-- source: wshobson/agents plugins/python-development/skills/python-resilience/SKILL.md -->

Build fault-tolerant Python applications that gracefully handle transient failures, network issues, and service outages. Resilience patterns keep systems running when dependencies are unreliable.

### When to Use This Skill

- Adding retry logic to external service calls
- Implementing timeouts for network operations
- Building fault-tolerant microservices
- Handling rate limiting and backpressure
- Creating infrastructure decorators
- Designing circuit breakers

### Core Concepts

#### 1. Transient vs Permanent Failures

Retry transient errors (network timeouts, temporary service issues). Don't retry permanent errors (invalid credentials, bad requests).

#### 2. Exponential Backoff

Increase wait time between retries to avoid overwhelming recovering services.

#### 3. Jitter

Add randomness to backoff to prevent thundering herd when many clients retry simultaneously.

#### 4. Bounded Retries

Cap both attempt count and total duration to prevent infinite retry loops.

### Quick Start

```python
from tenacity import retry, stop_after_attempt, wait_exponential_jitter

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential_jitter(initial=1, max=10),
)
def call_external_service(request: dict) -> dict:
    return httpx.post("https://api.example.com", json=request).json()
```

### Fundamental Patterns

#### Pattern 1: Basic Retry with Tenacity

Use the `tenacity` library for production-grade retry logic. For simpler cases, consider built-in retry functionality or a lightweight custom implementation.

```python
from tenacity import (
    retry,
    stop_after_attempt,
    stop_after_delay,
    wait_exponential_jitter,
    retry_if_exception_type,
)

TRANSIENT_ERRORS = (ConnectionError, TimeoutError, OSError)

@retry(
    retry=retry_if_exception_type(TRANSIENT_ERRORS),
    stop=stop_after_attempt(5) | stop_after_delay(60),
    wait=wait_exponential_jitter(initial=1, max=30),
)
def fetch_data(url: str) -> dict:
    """Fetch data with automatic retry on transient failures."""
    response = httpx.get(url, timeout=30)
    response.raise_for_status()
    return response.json()
```

#### Pattern 2: Retry Only Appropriate Errors

Whitelist specific transient exceptions. Never retry:

- `ValueError`, `TypeError` - These are bugs, not transient issues
- `AuthenticationError` - Invalid credentials won't become valid
- HTTP 4xx errors (except 429) - Client errors are permanent

```python
from tenacity import retry, retry_if_exception_type
import httpx

# Define what's retryable
RETRYABLE_EXCEPTIONS = (
    ConnectionError,
    TimeoutError,
    httpx.ConnectTimeout,
    httpx.ReadTimeout,
)

@retry(
    retry=retry_if_exception_type(RETRYABLE_EXCEPTIONS),
    stop=stop_after_attempt(3),
    wait=wait_exponential_jitter(initial=1, max=10),
)
def resilient_api_call(endpoint: str) -> dict:
    """Make API call with retry on network issues."""
    return httpx.get(endpoint, timeout=10).json()
```

#### Pattern 3: HTTP Status Code Retries

Retry specific HTTP status codes that indicate transient issues.

```python
from tenacity import retry, retry_if_result, stop_after_attempt
import httpx

RETRY_STATUS_CODES = {429, 502, 503, 504}

def should_retry_response(response: httpx.Response) -> bool:
    """Check if response indicates a retryable error."""
    return response.status_code in RETRY_STATUS_CODES

@retry(
    retry=retry_if_result(should_retry_response),
    stop=stop_after_attempt(3),
    wait=wait_exponential_jitter(initial=1, max=10),
)
def http_request(method: str, url: str, **kwargs) -> httpx.Response:
    """Make HTTP request with retry on transient status codes."""
    return httpx.request(method, url, timeout=30, **kwargs)
```

#### Pattern 4: Combined Exception and Status Retry

Handle both network exceptions and HTTP status codes.

```python
from tenacity import (
    retry,
    retry_if_exception_type,
    retry_if_result,
    stop_after_attempt,
    wait_exponential_jitter,
    before_sleep_log,
)
import logging
import httpx

logger = logging.getLogger(__name__)

TRANSIENT_EXCEPTIONS = (
    ConnectionError,
    TimeoutError,
    httpx.ConnectError,
    httpx.ReadTimeout,
)
RETRY_STATUS_CODES = {429, 500, 502, 503, 504}

def is_retryable_response(response: httpx.Response) -> bool:
    return response.status_code in RETRY_STATUS_CODES

@retry(
    retry=(
        retry_if_exception_type(TRANSIENT_EXCEPTIONS) |
        retry_if_result(is_retryable_response)
    ),
    stop=stop_after_attempt(5),
    wait=wait_exponential_jitter(initial=1, max=30),
    before_sleep=before_sleep_log(logger, logging.WARNING),
)
def robust_http_call(
    method: str,
    url: str,
    **kwargs,
) -> httpx.Response:
    """HTTP call with comprehensive retry handling."""
    return httpx.request(method, url, timeout=30, **kwargs)
```

### Detailed worked examples and patterns

Detailed sections (starting with `## Advanced Patterns`) live in `references/details.md`. Read that file when the navigation summary above is insufficient.

### Best Practices Summary

1. **Retry only transient errors** - Don't retry bugs or authentication failures
2. **Use exponential backoff** - Give services time to recover
3. **Add jitter** - Prevent thundering herd from synchronized retries
4. **Cap total duration** - `stop_after_attempt(5) | stop_after_delay(60)`
5. **Log every retry** - Silent retries hide systemic problems
6. **Use decorators** - Keep retry logic separate from business logic
7. **Inject dependencies** - Make infrastructure testable
8. **Set timeouts everywhere** - Every network call needs a timeout
9. **Fail gracefully** - Return cached/default values for non-critical paths
10. **Monitor retry rates** - High retry rates indicate underlying issues

## python-resilience — detailed worked examples

<!-- source: wshobson/agents plugins/python-development/skills/python-resilience/references/details.md -->

### Advanced Patterns

#### Pattern 5: Logging Retry Attempts

Track retry behavior for debugging and alerting.

```python
from tenacity import retry, stop_after_attempt, wait_exponential
import structlog

logger = structlog.get_logger()

def log_retry_attempt(retry_state):
    """Log detailed retry information."""
    exception = retry_state.outcome.exception()
    logger.warning(
        "Retrying operation",
        attempt=retry_state.attempt_number,
        exception_type=type(exception).__name__,
        exception_message=str(exception),
        next_wait_seconds=retry_state.next_action.sleep if retry_state.next_action else None,
    )

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, max=10),
    before_sleep=log_retry_attempt,
)
def call_with_logging(request: dict) -> dict:
    """External call with retry logging."""
    ...
```

#### Pattern 6: Timeout Decorator

Create reusable timeout decorators for consistent timeout handling.

```python
import asyncio
from functools import wraps
from typing import TypeVar, Callable

T = TypeVar("T")

def with_timeout(seconds: float):
    """Decorator to add timeout to async functions."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            return await asyncio.wait_for(
                func(*args, **kwargs),
                timeout=seconds,
            )
        return wrapper
    return decorator

@with_timeout(30)
async def fetch_with_timeout(url: str) -> dict:
    """Fetch URL with 30 second timeout."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
```

#### Pattern 7: Cross-Cutting Concerns via Decorators

Stack decorators to separate infrastructure from business logic.

```python
from functools import wraps
from typing import TypeVar, Callable
import structlog

logger = structlog.get_logger()
T = TypeVar("T")

def traced(name: str | None = None):
    """Add tracing to function calls."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        span_name = name or func.__name__

        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            logger.info("Operation started", operation=span_name)
            try:
                result = await func(*args, **kwargs)
                logger.info("Operation completed", operation=span_name)
                return result
            except Exception as e:
                logger.error("Operation failed", operation=span_name, error=str(e))
                raise
        return wrapper
    return decorator

# Stack multiple concerns
@traced("fetch_user_data")
@with_timeout(30)
@retry(stop=stop_after_attempt(3), wait=wait_exponential_jitter())
async def fetch_user_data(user_id: str) -> dict:
    """Fetch user with tracing, timeout, and retry."""
    ...
```

#### Pattern 8: Dependency Injection for Testability

Pass infrastructure components through constructors for easy testing.

```python
from dataclasses import dataclass
from typing import Protocol

class Logger(Protocol):
    def info(self, msg: str, **kwargs) -> None: ...
    def error(self, msg: str, **kwargs) -> None: ...

class MetricsClient(Protocol):
    def increment(self, metric: str, tags: dict | None = None) -> None: ...
    def timing(self, metric: str, value: float) -> None: ...

@dataclass
class UserService:
    """Service with injected infrastructure."""

    repository: UserRepository
    logger: Logger
    metrics: MetricsClient

    async def get_user(self, user_id: str) -> User:
        self.logger.info("Fetching user", user_id=user_id)
        start = time.perf_counter()

        try:
            user = await self.repository.get(user_id)
            self.metrics.increment("user.fetch.success")
            return user
        except Exception as e:
            self.metrics.increment("user.fetch.error")
            self.logger.error("Failed to fetch user", user_id=user_id, error=str(e))
            raise
        finally:
            elapsed = time.perf_counter() - start
            self.metrics.timing("user.fetch.duration", elapsed)

# Easy to test with fakes
service = UserService(
    repository=FakeRepository(),
    logger=FakeLogger(),
    metrics=FakeMetrics(),
)
```

#### Pattern 9: Fail-Safe Defaults

Degrade gracefully when non-critical operations fail.

```python
from typing import TypeVar
from collections.abc import Callable

T = TypeVar("T")

def fail_safe(default: T, log_failure: bool = True):
    """Return default value on failure instead of raising."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if log_failure:
                    logger.warning(
                        "Operation failed, using default",
                        function=func.__name__,
                        error=str(e),
                    )
                return default
        return wrapper
    return decorator

@fail_safe(default=[])
async def get_recommendations(user_id: str) -> list[str]:
    """Get recommendations, return empty list on failure."""
    ...
```

## Python Background Jobs & Task Queues

<!-- source: wshobson/agents plugins/python-development/skills/python-background-jobs/SKILL.md -->

Decouple long-running or unreliable work from request/response cycles. Return immediately to the user while background workers handle the heavy lifting asynchronously.

### When to Use This Skill

- Processing tasks that take longer than a few seconds
- Sending emails, notifications, or webhooks
- Generating reports or exporting data
- Processing uploads or media transformations
- Integrating with unreliable external services
- Building event-driven architectures

### Core Concepts

#### 1. Task Queue Pattern

API accepts request, enqueues a job, returns immediately with a job ID. Workers process jobs asynchronously.

#### 2. Idempotency

Tasks may be retried on failure. Design for safe re-execution.

#### 3. Job State Machine

Jobs transition through states: pending → running → succeeded/failed.

#### 4. At-Least-Once Delivery

Most queues guarantee at-least-once delivery. Your code must handle duplicates.

### Quick Start

This skill uses Celery for examples, a widely adopted task queue. Alternatives like RQ, Dramatiq, and cloud-native solutions (AWS SQS, GCP Tasks) are equally valid choices.

```python
from celery import Celery

app = Celery("tasks", broker="redis://localhost:6379")

@app.task
def send_email(to: str, subject: str, body: str) -> None:
    # This runs in a background worker
    email_client.send(to, subject, body)

# In your API handler
send_email.delay("user@example.com", "Welcome!", "Thanks for signing up")
```

### Fundamental Patterns

#### Pattern 1: Return Job ID Immediately

For operations exceeding a few seconds, return a job ID and process asynchronously.

```python
from uuid import uuid4
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"

@dataclass
class Job:
    id: str
    status: JobStatus
    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None
    result: dict | None = None
    error: str | None = None

# API endpoint
async def start_export(request: ExportRequest) -> JobResponse:
    """Start export job and return job ID."""
    job_id = str(uuid4())

    # Persist job record
    await jobs_repo.create(Job(
        id=job_id,
        status=JobStatus.PENDING,
        created_at=datetime.utcnow(),
    ))

    # Enqueue task for background processing
    await task_queue.enqueue(
        "export_data",
        job_id=job_id,
        params=request.model_dump(),
    )

    # Return immediately with job ID
    return JobResponse(
        job_id=job_id,
        status="pending",
        poll_url=f"/jobs/{job_id}",
    )
```

#### Pattern 2: Celery Task Configuration

Configure Celery tasks with proper retry and timeout settings.

```python
from celery import Celery

app = Celery("tasks", broker="redis://localhost:6379")

# Global configuration
app.conf.update(
    task_time_limit=3600,          # Hard limit: 1 hour
    task_soft_time_limit=3000,      # Soft limit: 50 minutes
    task_acks_late=True,            # Acknowledge after completion
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1,   # Don't prefetch too many tasks
)

@app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(ConnectionError, TimeoutError),
)
def process_payment(self, payment_id: str) -> dict:
    """Process payment with automatic retry on transient errors."""
    try:
        result = payment_gateway.charge(payment_id)
        return {"status": "success", "transaction_id": result.id}
    except PaymentDeclinedError as e:
        # Don't retry permanent failures
        return {"status": "declined", "reason": str(e)}
    except TransientError as e:
        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=2 ** self.request.retries * 60)
```

#### Pattern 3: Make Tasks Idempotent

Workers may retry on crash or timeout. Design for safe re-execution.

```python
@app.task(bind=True)
def process_order(self, order_id: str) -> None:
    """Process order idempotently."""
    order = orders_repo.get(order_id)

    # Already processed? Return early
    if order.status == OrderStatus.COMPLETED:
        logger.info("Order already processed", order_id=order_id)
        return

    # Already in progress? Check if we should continue
    if order.status == OrderStatus.PROCESSING:
        # Use idempotency key to avoid double-charging
        pass

    # Process with idempotency key
    result = payment_provider.charge(
        amount=order.total,
        idempotency_key=f"order-{order_id}",  # Critical!
    )

    orders_repo.update(order_id, status=OrderStatus.COMPLETED)
```

**Idempotency Strategies:**

1. **Check-before-write**: Verify state before action
2. **Idempotency keys**: Use unique tokens with external services
3. **Upsert patterns**: `INSERT ... ON CONFLICT UPDATE`
4. **Deduplication window**: Track processed IDs for N hours

#### Pattern 4: Job State Management

Persist job state transitions for visibility and debugging.

```python
class JobRepository:
    """Repository for managing job state."""

    async def create(self, job: Job) -> Job:
        """Create new job record."""
        await self._db.execute(
            """INSERT INTO jobs (id, status, created_at)
               VALUES ($1, $2, $3)""",
            job.id, job.status.value, job.created_at,
        )
        return job

    async def update_status(
        self,
        job_id: str,
        status: JobStatus,
        **fields,
    ) -> None:
        """Update job status with timestamp."""
        updates = {"status": status.value, **fields}

        if status == JobStatus.RUNNING:
            updates["started_at"] = datetime.utcnow()
        elif status in (JobStatus.SUCCEEDED, JobStatus.FAILED):
            updates["completed_at"] = datetime.utcnow()

        await self._db.execute(
            "UPDATE jobs SET status = $1, ... WHERE id = $2",
            updates, job_id,
        )

        logger.info(
            "Job status updated",
            job_id=job_id,
            status=status.value,
        )
```

### Detailed worked examples and patterns

Detailed sections (starting with `## Advanced Patterns`) live in `references/details.md`. Read that file when the navigation summary above is insufficient.

### Best Practices Summary

1. **Return immediately** - Don't block requests for long operations
2. **Persist job state** - Enable status polling and debugging
3. **Make tasks idempotent** - Safe to retry on any failure
4. **Use idempotency keys** - For external service calls
5. **Set timeouts** - Both soft and hard limits
6. **Implement DLQ** - Capture permanently failed tasks
7. **Log transitions** - Track job state changes
8. **Retry appropriately** - Exponential backoff for transient errors
9. **Don't retry permanent failures** - Validation errors, invalid credentials
10. **Monitor queue depth** - Alert on backlog growth

## python-background-jobs — detailed worked examples

<!-- source: wshobson/agents plugins/python-development/skills/python-background-jobs/references/details.md -->

### Advanced Patterns

#### Pattern 5: Dead Letter Queue

Handle permanently failed tasks for manual inspection.

```python
@app.task(bind=True, max_retries=3)
def process_webhook(self, webhook_id: str, payload: dict) -> None:
    """Process webhook with DLQ for failures."""
    try:
        result = send_webhook(payload)
        if not result.success:
            raise WebhookFailedError(result.error)
    except Exception as e:
        if self.request.retries >= self.max_retries:
            # Move to dead letter queue for manual inspection
            dead_letter_queue.send({
                "task": "process_webhook",
                "webhook_id": webhook_id,
                "payload": payload,
                "error": str(e),
                "attempts": self.request.retries + 1,
                "failed_at": datetime.utcnow().isoformat(),
            })
            logger.error(
                "Webhook moved to DLQ after max retries",
                webhook_id=webhook_id,
                error=str(e),
            )
            return

        # Exponential backoff retry
        raise self.retry(exc=e, countdown=2 ** self.request.retries * 60)
```

#### Pattern 6: Status Polling Endpoint

Provide an endpoint for clients to check job status.

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/jobs/{job_id}")
async def get_job_status(job_id: str) -> JobStatusResponse:
    """Get current status of a background job."""
    job = await jobs_repo.get(job_id)

    if job is None:
        raise HTTPException(404, f"Job {job_id} not found")

    return JobStatusResponse(
        job_id=job.id,
        status=job.status.value,
        created_at=job.created_at,
        started_at=job.started_at,
        completed_at=job.completed_at,
        result=job.result if job.status == JobStatus.SUCCEEDED else None,
        error=job.error if job.status == JobStatus.FAILED else None,
        # Helpful for clients
        is_terminal=job.status in (JobStatus.SUCCEEDED, JobStatus.FAILED),
    )
```

#### Pattern 7: Task Chaining and Workflows

Compose complex workflows from simple tasks.

```python
from celery import chain, group, chord

# Simple chain: A → B → C
workflow = chain(
    extract_data.s(source_id),
    transform_data.s(),
    load_data.s(destination_id),
)

# Parallel execution: A, B, C all at once
parallel = group(
    send_email.s(user_email),
    send_sms.s(user_phone),
    update_analytics.s(event_data),
)

# Chord: Run tasks in parallel, then a callback
# Process all items, then send completion notification
workflow = chord(
    [process_item.s(item_id) for item_id in item_ids],
    send_completion_notification.s(batch_id),
)

workflow.apply_async()
```

#### Pattern 8: Alternative Task Queues

Choose the right tool for your needs.

**RQ (Redis Queue)**: Simple, Redis-based
```python
from rq import Queue
from redis import Redis

queue = Queue(connection=Redis())
job = queue.enqueue(send_email, "user@example.com", "Subject", "Body")
```

**Dramatiq**: Modern Celery alternative
```python
import dramatiq
from dramatiq.brokers.redis import RedisBroker

dramatiq.set_broker(RedisBroker())

@dramatiq.actor
def send_email(to: str, subject: str, body: str) -> None:
    email_client.send(to, subject, body)
```

**Cloud-native options:**
- AWS SQS + Lambda
- Google Cloud Tasks
- Azure Functions

## Python Observability

<!-- source: wshobson/agents plugins/python-development/skills/python-observability/SKILL.md -->

Instrument Python applications with structured logs, metrics, and traces. When something breaks in production, you need to answer "what, where, and why" without deploying new code.

### When to Use This Skill

- Adding structured logging to applications
- Implementing metrics collection with Prometheus
- Setting up distributed tracing across services
- Propagating correlation IDs through request chains
- Debugging production issues
- Building observability dashboards

### Core Concepts

#### 1. Structured Logging

Emit logs as JSON with consistent fields for production environments. Machine-readable logs enable powerful queries and alerts. For local development, consider human-readable formats.

#### 2. The Four Golden Signals

Track latency, traffic, errors, and saturation for every service boundary.

#### 3. Correlation IDs

Thread a unique ID through all logs and spans for a single request, enabling end-to-end tracing.

#### 4. Bounded Cardinality

Keep metric label values bounded. Unbounded labels (like user IDs) explode storage costs.

### Quick Start

```python
import structlog

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
)

logger = structlog.get_logger()
logger.info("Request processed", user_id="123", duration_ms=45)
```

### Fundamental Patterns

#### Pattern 1: Structured Logging with Structlog

Configure structlog for JSON output with consistent fields.

```python
import logging
import structlog

def configure_logging(log_level: str = "INFO") -> None:
    """Configure structured logging for the application."""
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, log_level.upper())
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

# Initialize at application startup
configure_logging("INFO")
logger = structlog.get_logger()
```

#### Pattern 2: Consistent Log Fields

Every log entry should include standard fields for filtering and correlation.

```python
import structlog
from contextvars import ContextVar

# Store correlation ID in context
correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")

logger = structlog.get_logger()

def process_request(request: Request) -> Response:
    """Process request with structured logging."""
    logger.info(
        "Request received",
        correlation_id=correlation_id.get(),
        method=request.method,
        path=request.path,
        user_id=request.user_id,
    )

    try:
        result = handle_request(request)
        logger.info(
            "Request completed",
            correlation_id=correlation_id.get(),
            status_code=200,
            duration_ms=elapsed,
        )
        return result
    except Exception as e:
        logger.error(
            "Request failed",
            correlation_id=correlation_id.get(),
            error_type=type(e).__name__,
            error_message=str(e),
        )
        raise
```

#### Pattern 3: Semantic Log Levels

Use log levels consistently across the application.

| Level | Purpose | Examples |
|-------|---------|----------|
| `DEBUG` | Development diagnostics | Variable values, internal state |
| `INFO` | Request lifecycle, operations | Request start/end, job completion |
| `WARNING` | Recoverable anomalies | Retry attempts, fallback used |
| `ERROR` | Failures needing attention | Exceptions, service unavailable |

```python
# DEBUG: Detailed internal information
logger.debug("Cache lookup", key=cache_key, hit=cache_hit)

# INFO: Normal operational events
logger.info("Order created", order_id=order.id, total=order.total)

# WARNING: Abnormal but handled situations
logger.warning(
    "Rate limit approaching",
    current_rate=950,
    limit=1000,
    reset_seconds=30,
)

# ERROR: Failures requiring investigation
logger.error(
    "Payment processing failed",
    order_id=order.id,
    error=str(e),
    payment_provider="stripe",
)
```

Never log expected behavior at `ERROR`. A user entering a wrong password is `INFO`, not `ERROR`.

#### Pattern 4: Correlation ID Propagation

Generate a unique ID at ingress and thread it through all operations.

```python
from contextvars import ContextVar
import uuid
import structlog

correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")

def set_correlation_id(cid: str | None = None) -> str:
    """Set correlation ID for current context."""
    cid = cid or str(uuid.uuid4())
    correlation_id.set(cid)
    structlog.contextvars.bind_contextvars(correlation_id=cid)
    return cid

# FastAPI middleware example
from fastapi import Request

async def correlation_middleware(request: Request, call_next):
    """Middleware to set and propagate correlation ID."""
    # Use incoming header or generate new
    cid = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
    set_correlation_id(cid)

    response = await call_next(request)
    response.headers["X-Correlation-ID"] = cid
    return response
```

Propagate to outbound requests:

```python
import httpx

async def call_downstream_service(endpoint: str, data: dict) -> dict:
    """Call downstream service with correlation ID."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            endpoint,
            json=data,
            headers={"X-Correlation-ID": correlation_id.get()},
        )
        return response.json()
```

### Detailed worked examples and patterns

Detailed sections (starting with `## Advanced Patterns`) live in `references/details.md`. Read that file when the navigation summary above is insufficient.

### Best Practices Summary

1. **Use structured logging** - JSON logs with consistent fields
2. **Propagate correlation IDs** - Thread through all requests and logs
3. **Track the four golden signals** - Latency, traffic, errors, saturation
4. **Bound label cardinality** - Never use unbounded values as metric labels
5. **Log at appropriate levels** - Don't cry wolf with ERROR
6. **Include context** - User ID, request ID, operation name in logs
7. **Use context managers** - Consistent timing and error handling
8. **Separate concerns** - Observability code shouldn't pollute business logic
9. **Test your observability** - Verify logs and metrics in integration tests
10. **Set up alerts** - Metrics are useless without alerting

## python-observability — detailed worked examples

<!-- source: wshobson/agents plugins/python-development/skills/python-observability/references/details.md -->

### Advanced Patterns

#### Pattern 5: The Four Golden Signals with Prometheus

Track these metrics for every service boundary:

```python
from prometheus_client import Counter, Histogram, Gauge

# Latency: How long requests take
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "Request latency in seconds",
    ["method", "endpoint", "status"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10],
)

# Traffic: Request rate
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

# Errors: Error rate
ERROR_COUNT = Counter(
    "http_errors_total",
    "Total HTTP errors",
    ["method", "endpoint", "error_type"],
)

# Saturation: Resource utilization
DB_POOL_USAGE = Gauge(
    "db_connection_pool_used",
    "Number of database connections in use",
)
```

Instrument your endpoints:

```python
import time
from functools import wraps

def track_request(func):
    """Decorator to track request metrics."""
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        method = request.method
        # Use the route template ("/users/{user_id}"), not the raw path,
        # so IDs in URLs do not create a new label value per request.
        # Inside a mounted sub-app this is the sub-app's own template, so
        # add a fixed per-app label if two mounts share route paths.
        route = request.scope.get("route")
        endpoint = route.path if route else "unmatched"
        start = time.perf_counter()

        try:
            response = await func(request, *args, **kwargs)
            status = str(response.status_code)
            return response
        except Exception as e:
            status = "500"
            ERROR_COUNT.labels(
                method=method,
                endpoint=endpoint,
                error_type=type(e).__name__,
            ).inc()
            raise
        finally:
            duration = time.perf_counter() - start
            REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()
            REQUEST_LATENCY.labels(method=method, endpoint=endpoint, status=status).observe(duration)

    return wrapper
```

#### Pattern 6: Bounded Cardinality

Avoid labels with unbounded values to prevent metric explosion.

```python
# BAD: User ID has potentially millions of values
REQUEST_COUNT.labels(method="GET", user_id=user.id)  # Don't do this!

# GOOD: Bounded values only
REQUEST_COUNT.labels(method="GET", endpoint="/users", status="200")

# If you need per-user metrics, use a different approach:
# - Log the user_id and query logs
# - Use a separate analytics system
# - Bucket users by type/tier, in a metric that declares that label
REQUESTS_BY_TIER = Counter(
    "http_requests_by_tier_total",
    "HTTP requests by user tier",
    ["method", "endpoint", "user_tier"],
)
REQUESTS_BY_TIER.labels(
    method="GET",
    endpoint="/users",
    user_tier="premium",  # Bounded set of values
)
```

#### Pattern 7: Timed Operations with Context Manager

Create a reusable timing context manager for operations.

```python
from contextlib import contextmanager
import time
import structlog

logger = structlog.get_logger()

@contextmanager
def timed_operation(name: str, **extra_fields):
    """Context manager for timing and logging operations."""
    start = time.perf_counter()
    logger.debug("Operation started", operation=name, **extra_fields)

    try:
        yield
    except Exception as e:
        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.error(
            "Operation failed",
            operation=name,
            duration_ms=round(elapsed_ms, 2),
            error=str(e),
            **extra_fields,
        )
        raise
    else:
        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "Operation completed",
            operation=name,
            duration_ms=round(elapsed_ms, 2),
            **extra_fields,
        )

# Usage
with timed_operation("fetch_user_orders", user_id=user.id):
    orders = await order_repository.get_by_user(user.id)
```

#### Pattern 8: OpenTelemetry Tracing

Set up distributed tracing with OpenTelemetry.

**Note:** OpenTelemetry is actively evolving. Check the [official Python documentation](https://opentelemetry.io/docs/languages/python/) for the latest API patterns and best practices.

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

def configure_tracing(service_name: str, otlp_endpoint: str) -> None:
    """Configure OpenTelemetry tracing."""
    provider = TracerProvider()
    processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=otlp_endpoint))
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

async def process_order(order_id: str) -> Order:
    """Process order with tracing."""
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order_id)

        with tracer.start_as_current_span("validate_order"):
            validate_order(order_id)

        with tracer.start_as_current_span("charge_payment"):
            charge_payment(order_id)

        with tracer.start_as_current_span("send_confirmation"):
            send_confirmation(order_id)

        return order
```

## Python Type Safety

<!-- source: wshobson/agents plugins/python-development/skills/python-type-safety/SKILL.md -->

Leverage Python's type system to catch errors at static analysis time. Type annotations serve as enforced documentation that tooling validates automatically.

### When to Use This Skill

- Adding type hints to existing code
- Creating generic, reusable classes
- Defining structural interfaces with protocols
- Configuring mypy or pyright for strict checking
- Understanding type narrowing and guards
- Building type-safe APIs and libraries

### Core Concepts

#### 1. Type Annotations

Declare expected types for function parameters, return values, and variables.

#### 2. Generics

Write reusable code that preserves type information across different types.

#### 3. Protocols

Define structural interfaces without inheritance (duck typing with type safety).

#### 4. Type Narrowing

Use guards and conditionals to narrow types within code blocks.

### Quick Start

```python
def get_user(user_id: str) -> User | None:
    """Return type makes 'might not exist' explicit."""
    ...

# Type checker enforces handling None case
user = get_user("123")
if user is None:
    raise UserNotFoundError("123")
print(user.name)  # Type checker knows user is User here
```

### Fundamental Patterns

#### Pattern 1: Annotate All Public Signatures

Every public function, method, and class should have type annotations.

```python
def get_user(user_id: str) -> User:
    """Retrieve user by ID."""
    ...

def process_batch(
    items: list[Item],
    max_workers: int = 4,
) -> BatchResult[ProcessedItem]:
    """Process items concurrently."""
    ...

class UserRepository:
    def __init__(self, db: Database) -> None:
        self._db = db

    async def find_by_id(self, user_id: str) -> User | None:
        """Return User if found, None otherwise."""
        ...

    async def find_by_email(self, email: str) -> User | None:
        ...

    async def save(self, user: User) -> User:
        """Save and return user with generated ID."""
        ...
```

Use `mypy --strict` or `pyright` in CI to catch type errors early. For existing projects, enable strict mode incrementally using per-module overrides.

#### Pattern 2: Use Modern Union Syntax

Python 3.10+ provides cleaner union syntax.

```python
# Preferred (3.10+)
def find_user(user_id: str) -> User | None:
    ...

def parse_value(v: str) -> int | float | str:
    ...

# Older style (still valid, needed for 3.9)
from typing import Optional, Union

def find_user(user_id: str) -> Optional[User]:
    ...
```

#### Pattern 3: Type Narrowing with Guards

Use conditionals to narrow types for the type checker.

```python
def process_user(user_id: str) -> UserData:
    user = find_user(user_id)

    if user is None:
        raise UserNotFoundError(f"User {user_id} not found")

    # Type checker knows user is User here, not User | None
    return UserData(
        name=user.name,
        email=user.email,
    )

def process_items(items: list[Item | None]) -> list[ProcessedItem]:
    # Filter and narrow types
    valid_items = [item for item in items if item is not None]
    # valid_items is now list[Item]
    return [process(item) for item in valid_items]
```

#### Pattern 4: Generic Classes

Create type-safe reusable containers.

```python
from typing import TypeVar, Generic

T = TypeVar("T")
E = TypeVar("E", bound=Exception)

class Result(Generic[T, E]):
    """Represents either a success value or an error."""

    def __init__(
        self,
        value: T | None = None,
        error: E | None = None,
    ) -> None:
        if (value is None) == (error is None):
            raise ValueError("Exactly one of value or error must be set")
        self._value = value
        self._error = error

    @property
    def is_success(self) -> bool:
        return self._error is None

    @property
    def is_failure(self) -> bool:
        return self._error is not None

    def unwrap(self) -> T:
        """Get value or raise the error."""
        if self._error is not None:
            raise self._error
        return self._value  # type: ignore[return-value]

    def unwrap_or(self, default: T) -> T:
        """Get value or return default."""
        if self._error is not None:
            return default
        return self._value  # type: ignore[return-value]

# Usage preserves types
def parse_config(path: str) -> Result[Config, ConfigError]:
    try:
        return Result(value=Config.from_file(path))
    except ConfigError as e:
        return Result(error=e)

result = parse_config("config.yaml")
if result.is_success:
    config = result.unwrap()  # Type: Config
```

### Detailed worked examples and patterns

Detailed sections (starting with `## Advanced Patterns`) live in `references/details.md`. Read that file when the navigation summary above is insufficient.

### Best Practices Summary

1. **Annotate all public APIs** - Functions, methods, class attributes
2. **Use `T | None`** - Modern union syntax over `Optional[T]`
3. **Run strict type checking** - `mypy --strict` in CI
4. **Use generics** - Preserve type info in reusable code
5. **Define protocols** - Structural typing for interfaces
6. **Narrow types** - Use guards to help the type checker
7. **Bound type vars** - Restrict generics to meaningful types
8. **Create type aliases** - Meaningful names for complex types
9. **Minimize `Any`** - Use specific types or generics. `Any` is acceptable for truly dynamic data or when interfacing with untyped third-party code
10. **Document with types** - Types are enforceable documentation

## python-type-safety — detailed worked examples

<!-- source: wshobson/agents plugins/python-development/skills/python-type-safety/references/details.md -->

### Advanced Patterns

#### Pattern 5: Generic Repository

Create type-safe data access patterns.

```python
from typing import TypeVar, Generic
from abc import ABC, abstractmethod

T = TypeVar("T")
ID = TypeVar("ID")

class Repository(ABC, Generic[T, ID]):
    """Generic repository interface."""

    @abstractmethod
    async def get(self, id: ID) -> T | None:
        """Get entity by ID."""
        ...

    @abstractmethod
    async def save(self, entity: T) -> T:
        """Save and return entity."""
        ...

    @abstractmethod
    async def delete(self, id: ID) -> bool:
        """Delete entity, return True if existed."""
        ...

class UserRepository(Repository[User, str]):
    """Concrete repository for Users with string IDs."""

    async def get(self, id: str) -> User | None:
        row = await self._db.fetchrow(
            "SELECT * FROM users WHERE id = $1", id
        )
        return User(**row) if row else None

    async def save(self, entity: User) -> User:
        ...

    async def delete(self, id: str) -> bool:
        ...
```

#### Pattern 6: TypeVar with Bounds

Restrict generic parameters to specific types.

```python
from typing import TypeVar
from pydantic import BaseModel

ModelT = TypeVar("ModelT", bound=BaseModel)

def validate_and_create(model_cls: type[ModelT], data: dict) -> ModelT:
    """Create a validated Pydantic model from dict."""
    return model_cls.model_validate(data)

# Works with any BaseModel subclass
class User(BaseModel):
    name: str
    email: str

user = validate_and_create(User, {"name": "Alice", "email": "a@b.com"})
# user is typed as User

# Type error: str is not a BaseModel subclass
result = validate_and_create(str, {"name": "Alice"})  # Error!
```

#### Pattern 7: Protocols for Structural Typing

Define interfaces without requiring inheritance.

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Serializable(Protocol):
    """Any class that can be serialized to/from dict."""

    def to_dict(self) -> dict:
        ...

    @classmethod
    def from_dict(cls, data: dict) -> "Serializable":
        ...

# User satisfies Serializable without inheriting from it
class User:
    def __init__(self, id: str, name: str) -> None:
        self.id = id
        self.name = name

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name}

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(id=data["id"], name=data["name"])

def serialize(obj: Serializable) -> str:
    """Works with any Serializable object."""
    return json.dumps(obj.to_dict())

# Works - User matches the protocol
serialize(User("1", "Alice"))

# Runtime checking with @runtime_checkable
isinstance(User("1", "Alice"), Serializable)  # True
```

#### Pattern 8: Common Protocol Patterns

Define reusable structural interfaces.

```python
from typing import Protocol

class Closeable(Protocol):
    """Resource that can be closed."""
    def close(self) -> None: ...

class AsyncCloseable(Protocol):
    """Async resource that can be closed."""
    async def close(self) -> None: ...

class Readable(Protocol):
    """Object that can be read from."""
    def read(self, n: int = -1) -> bytes: ...

class HasId(Protocol):
    """Object with an ID property."""
    @property
    def id(self) -> str: ...

class Comparable(Protocol):
    """Object that supports comparison."""
    def __lt__(self, other: "Comparable") -> bool: ...
    def __le__(self, other: "Comparable") -> bool: ...
```

#### Pattern 9: Type Aliases

Create meaningful type names.

**Note:** The `type Alias = ...` statement syntax (PEP 695) was introduced in **Python 3.12**, not 3.10. For projects targeting earlier versions (including 3.10/3.11), use the `TypeAlias` annotation (PEP 613, available since Python 3.10).

```python
# Python 3.12+ type statement (PEP 695)
type UserId = str
type UserDict = dict[str, Any]

# Python 3.12+ type statement with generics (PEP 695)
type Handler[T] = Callable[[Request], T]
type AsyncHandler[T] = Callable[[Request], Awaitable[T]]
```

```python
# Python 3.10-3.11 style (needed for broader compatibility)
from typing import TypeAlias
from collections.abc import Callable, Awaitable

UserId: TypeAlias = str
Handler: TypeAlias = Callable[[Request], Response]
```

```python
# Usage
def register_handler(path: str, handler: Handler[Response]) -> None:
    ...
```

#### Pattern 10: Callable Types

Type function parameters and callbacks.

```python
from collections.abc import Callable, Awaitable

# Sync callback
ProgressCallback = Callable[[int, int], None]  # (current, total)

# Async callback
AsyncHandler = Callable[[Request], Awaitable[Response]]

# With named parameters (using Protocol)
class OnProgress(Protocol):
    def __call__(
        self,
        current: int,
        total: int,
        *,
        message: str = "",
    ) -> None: ...

def process_items(
    items: list[Item],
    on_progress: ProgressCallback | None = None,
) -> list[Result]:
    for i, item in enumerate(items):
        if on_progress:
            on_progress(i, len(items))
        ...
```

### Configuration

#### Strict Mode Checklist

For `mypy --strict` compliance:

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
no_implicit_optional = true
```

Incremental adoption goals:
- All function parameters annotated
- All return types annotated
- Class attributes annotated
- Minimize `Any` usage (acceptable for truly dynamic data)
- Generic collections use type parameters (`list[str]` not `list`)

For existing codebases, enable strict mode per-module using `# mypy: strict` or configure per-module overrides in `pyproject.toml`.
