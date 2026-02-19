# Expected Output

## Running

```bash
python flow.py
```

## Requirements

- `pip install blazing`
- No docker-compose needed — uses LocalSecretsService (in-process emulator)

## Output

```
=== Secrets Management with SecretsConnector ===

--- Pattern 1: DatabaseService with SecretsConnector ---
  Connection URL present: True
  DB user: admin, password set: True

--- Pattern 2: APIClientService with SecretsConnector ---
  Authenticated: True
  Secret env vars: 3 (['API_KEY', 'API_SECRET', 'API_VERSION'])

--- Pattern 3: LocalStack with secrets service ---
  Stripe key starts with: sk_live...
  Total secrets: 1

=== Done ===
```

## Notes

- Secrets are encrypted at rest — plaintext values are never written to disk
- `LocalSecretsService` provides the same `SecretsConnector` interface as the production backend (Vault / AWS Secrets Manager)
- `secrets.as_env_dict()` is useful for injecting secrets as environment variables into subprocesses
- For production, replace `LocalSecretsService` with the cloud-backed `SecretsService` connector
