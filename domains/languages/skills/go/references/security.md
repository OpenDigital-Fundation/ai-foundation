# Go — Security

Part of `languages:go`. Load when code that handles untrusted input, auth, secrets, files, network or SQL.

## Go Security

<!-- source: affaan-m/ECC rules/golang/security.md -->

> This file extends common/security.md with Go specific content.

### Secret Management

```go
apiKey := os.Getenv("OPENAI_API_KEY")
if apiKey == "" {
    log.Fatal("OPENAI_API_KEY not configured")
}
```

### Security Scanning

- Use **gosec** for static security analysis:
  ```bash
  gosec ./...
  ```

### Context & Timeouts

Always use `context.Context` for timeout control:

```go
ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
defer cancel()
```
