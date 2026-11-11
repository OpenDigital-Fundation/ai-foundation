# Secrets hygiene — secrets management

Part of `security:secrets-hygiene`. Adapted reference material; the owner procedure, project conventions, scope and authorization rules take precedence. Examples are not automatically executed.

This is an optional integration example, not an instruction to provision a provider. Pin reviewed images/actions, use scoped workload identity, confirm access/cost and credential rotation with the owner, and prevent logs from exposing secrets. Do not activate cloud rotation or install a controller automatically.

## Secrets Management

<!-- source: davila7/claude-code-templates cli-tool/components/skills/security/secrets-management/SKILL.md#hashicorp-vault-integration,external-secrets-operator,secret-rotation -->

### HashiCorp Vault Integration

#### Setup Vault

```bash
# Start Vault dev server
vault server -dev

# Set environment
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='root'

# Enable secrets engine
vault secrets enable -path=secret kv-v2

# Store secret
vault kv put secret/database/config username=admin password=secret
```

#### GitHub Actions with Vault

```yaml
name: Deploy with Vault Secrets

on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@<reviewed-commit-sha>

    - name: Import Secrets from Vault
      uses: hashicorp/vault-action@<reviewed-commit-sha>
      with:
        url: https://vault.example.com:8200
        token: ${{ secrets.VAULT_TOKEN }}
        secrets: |
          secret/data/database username | DB_USERNAME ;
          secret/data/database password | DB_PASSWORD ;
          secret/data/api key | API_KEY

    - name: Use secrets
      run: |
        echo "Connecting to database as $DB_USERNAME"
        # Use $DB_PASSWORD, $API_KEY
```

#### GitLab CI with Vault

```yaml
deploy:
  image: vault:<version>
  before_script:
    - export VAULT_ADDR=https://vault.example.com:8200
    - export VAULT_TOKEN=$VAULT_TOKEN
    - apk add curl jq
  script:
    - |
      DB_PASSWORD=$(vault kv get -field=password secret/database/config)
      API_KEY=$(vault kv get -field=key secret/api/credentials)
      echo "Deploying with secrets..."
      # Use $DB_PASSWORD, $API_KEY
```

**Reference:** See `references/vault-setup.md`

### Secret Rotation

#### Automated Rotation with AWS

```python
import boto3
import json

def lambda_handler(event, context):
    client = boto3.client('secretsmanager')

    # Get current secret
    response = client.get_secret_value(SecretId='my-secret')
    current_secret = json.loads(response['SecretString'])

    # Generate new password
    new_password = generate_strong_password()

    # Update database password
    update_database_password(new_password)

    # Update secret
    client.put_secret_value(
        SecretId='my-secret',
        SecretString=json.dumps({
            'username': current_secret['username'],
            'password': new_password
        })
    )

    return {'statusCode': 200}
```

#### Manual Rotation Process

1. Generate new secret
2. Update secret in secret store
3. Update applications to use new secret
4. Verify functionality
5. Revoke old secret

### External Secrets Operator

#### Kubernetes Integration

```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: production
spec:
  provider:
    vault:
      server: "https://vault.example.com:8200"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "production"

---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: database-credentials
    creationPolicy: Owner
  data:
  - secretKey: username
    remoteRef:
      key: database/config
      property: username
  - secretKey: password
    remoteRef:
      key: database/config
      property: password
```
