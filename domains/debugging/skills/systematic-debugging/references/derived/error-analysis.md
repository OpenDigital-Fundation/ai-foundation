# Systematic debugging — error analysis

Part of `debugging:systematic-debugging`. Adapted reference material; the owner procedure, project conventions, scope and authorization rules take precedence. Examples are not automatically executed.

## Error Analysis and Resolution

<!-- source: wshobson/agents plugins/error-debugging/commands/error-analysis.md#error-prevention-strategies -->

### Error Prevention Strategies

#### Input Validation and Type Safety

**Defensive Programming:**

```typescript
// TypeScript: Leverage type system for compile-time safety
interface PaymentRequest {
  amount: number;
  currency: string;
  customerId: string;
  paymentMethodId: string;
}

function processPayment(request: PaymentRequest): PaymentResult {
  // Runtime validation for external inputs
  if (request.amount <= 0) {
    throw new ValidationError("Amount must be positive");
  }

  if (!["USD", "EUR", "GBP"].includes(request.currency)) {
    throw new ValidationError("Unsupported currency");
  }

  // Use Zod or Yup for complex validation
  const schema = z.object({
    amount: z.number().positive().max(1000000),
    currency: z.enum(["USD", "EUR", "GBP"]),
    customerId: z.string().uuid(),
    paymentMethodId: z.string().min(1),
  });

  const validated = schema.parse(request);

  // Now safe to process
  return chargeCustomer(validated);
}
```

**Python Type Hints and Validation:**

```python
from typing import Optional
from pydantic import BaseModel, validator, Field
from decimal import Decimal

class PaymentRequest(BaseModel):
    amount: Decimal = Field(..., gt=0, le=1000000)
    currency: str
    customer_id: str
    payment_method_id: str

    @validator('currency')
    def validate_currency(cls, v):
        if v not in ['USD', 'EUR', 'GBP']:
            raise ValueError('Unsupported currency')
        return v

    @validator('customer_id', 'payment_method_id')
    def validate_ids(cls, v):
        if not v or len(v) < 1:
            raise ValueError('ID cannot be empty')
        return v

def process_payment(request: PaymentRequest) -> PaymentResult:
    # Pydantic validates automatically on instantiation
    # Type hints provide IDE support and static analysis
    return charge_customer(request)
```

#### Error Boundaries and Graceful Degradation

**React Error Boundaries:**

```typescript
import React, { Component, ErrorInfo, ReactNode } from 'react';
import * as Sentry from '@sentry/react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log to error tracking service
    Sentry.captureException(error, {
      contexts: {
        react: {
          componentStack: errorInfo.componentStack
        }
      }
    });

    console.error('Uncaught error:', error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div role="alert">
          <h2>Something went wrong</h2>
          <details>
            <summary>Error details</summary>
            <pre>{this.state.error?.message}</pre>
          </details>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
```

**Circuit Breaker Pattern:**

```python
from datetime import datetime, timedelta
from enum import Enum
import time

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60, success_threshold=2):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.success_threshold = success_threshold
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED

    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitBreakerOpenError("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        self.failure_count = 0
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.success_count = 0

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def _should_attempt_reset(self):
        return (datetime.now() - self.last_failure_time) > timedelta(seconds=self.timeout)

# Usage
payment_circuit = CircuitBreaker(failure_threshold=5, timeout=60)

def process_payment_with_circuit_breaker(payment_data):
    try:
        result = payment_circuit.call(external_payment_api.charge, payment_data)
        return result
    except CircuitBreakerOpenError:
        # Graceful degradation: queue for later processing
        payment_queue.enqueue(payment_data)
        return {"status": "queued", "message": "Payment will be processed shortly"}
```

#### Retry Logic with Exponential Backoff

```typescript
// TypeScript retry implementation
interface RetryOptions {
  maxAttempts: number;
  baseDelayMs: number;
  maxDelayMs: number;
  exponentialBase: number;
  retryableErrors?: string[];
}

async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  options: RetryOptions = {
    maxAttempts: 3,
    baseDelayMs: 1000,
    maxDelayMs: 30000,
    exponentialBase: 2,
  },
): Promise<T> {
  let lastError: Error;

  for (let attempt = 0; attempt < options.maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;

      // Check if error is retryable
      if (
        options.retryableErrors &&
        !options.retryableErrors.includes(error.name)
      ) {
        throw error; // Don't retry non-retryable errors
      }

      if (attempt < options.maxAttempts - 1) {
        const delay = Math.min(
          options.baseDelayMs * Math.pow(options.exponentialBase, attempt),
          options.maxDelayMs,
        );

        // Add jitter to prevent thundering herd
        const jitter = Math.random() * 0.1 * delay;
        const actualDelay = delay + jitter;

        console.log(
          `Attempt ${attempt + 1} failed, retrying in ${actualDelay}ms`,
        );
        await new Promise((resolve) => setTimeout(resolve, actualDelay));
      }
    }
  }

  throw lastError!;
}

// Usage
const result = await retryWithBackoff(
  () => fetch("https://api.example.com/data"),
  {
    maxAttempts: 3,
    baseDelayMs: 1000,
    maxDelayMs: 10000,
    exponentialBase: 2,
    retryableErrors: ["NetworkError", "TimeoutError"],
  },
);
```
