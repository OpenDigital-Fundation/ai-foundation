# Python — Security

Part of `languages:python`. Load when code that handles untrusted input, auth, secrets, files, network or SQL.

## Python Security

<!-- source: affaan-m/ECC rules/python/security.md -->

> This file extends [common/security.md](../common/security.md) with Python specific content.

### Secret Management

```python
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ["OPENAI_API_KEY"]  # Raises KeyError if missing
```

### Security Scanning

- Use **bandit** for static security analysis:
  ```bash
  bandit -r src/
  ```

### Reference

See skill: `languages:python` (`references/frameworks/django.md`) for Django-specific security guidelines (if applicable).
