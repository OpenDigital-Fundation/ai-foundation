# Architecture review — legacy modernizer

Part of `architecture:architecture-review`. Adapted reference material; the owner procedure, project conventions, scope and authorization rules take precedence. Examples are not automatically executed.

## Legacy Modernizer

<!-- source: Jeffallan/claude-skills skills/legacy-modernizer/SKILL.md#code-examples -->

### Code Examples

#### Strangler Fig Facade (Python)
```python
# facade.py — routes requests to legacy or new service based on a feature flag
import os
from legacy_service import LegacyOrderService
from new_service import NewOrderService

class OrderServiceFacade:
    def __init__(self):
        self._legacy = LegacyOrderService()
        self._new = NewOrderService()

    def get_order(self, order_id: str):
        if os.getenv("USE_NEW_ORDER_SERVICE", "false").lower() == "true":
            return self._new.fetch(order_id)
        return self._legacy.get(order_id)
```

#### Feature Flag Wrapper
```python
# feature_flags.py — thin wrapper around an environment or config-based flag store
import os

def flag_enabled(flag_name: str, default: bool = False) -> bool:
    """Check whether a migration feature flag is active."""
    return os.getenv(flag_name, str(default)).lower() == "true"

# Usage
if flag_enabled("USE_NEW_PAYMENT_GATEWAY"):
    result = new_gateway.charge(order)
else:
    result = legacy_gateway.charge(order)
```

#### Characterization Test Template (pytest)
```python
# test_characterization_orders.py
# Captures existing legacy behavior as a golden-master safety net.
import pytest
from legacy_service import LegacyOrderService

service = LegacyOrderService()

@pytest.mark.parametrize("order_id,expected_status", [
    ("ORD-001", "SHIPPED"),
    ("ORD-002", "PENDING"),
    ("ORD-003", "CANCELLED"),
])
def test_order_status_golden_master(order_id, expected_status):
    """Fail loudly if legacy behavior changes unexpectedly."""
    result = service.get(order_id)
    assert result["status"] == expected_status, (
        f"Characterization broken for {order_id}: "
        f"expected {expected_status}, got {result['status']}"
    )
```
