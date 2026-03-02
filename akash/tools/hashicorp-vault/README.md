# hashicorp-vault

HashiCorp Vault is a tool for securely managing secrets, encryption keys, and access to sensitive data.

## Use Cases

- Secret management (API keys, passwords, certificates)
- Dynamic credential generation
- Data encryption as a service
- Identity-based access control

## Getting Started

1. Access the web UI or set `VAULT_ADDR` for the CLI
2. Initialize and unseal the vault
3. Enable secret engines and store your first secret

## Accessing the Service

Access the Vault web UI at `http://{SERVICE_URI}:8200/ui/` or use the CLI:
```bash
export VAULT_ADDR="http://{SERVICE_URI}:8200"
vault status
```


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `VAULT_DEV_ROOT_TOKEN_ID` | `mysecrettoken` |
| `VAULT_DEV_LISTEN_ADDRESS` | `0.0.0.0:8200` |

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `vault` |
| CPU | 1.0 |
| Memory | 512Mi |
| Storage | 1Gi |
| Exposed Ports | 8200 |

## Documentation

For full documentation, visit: [https://developer.hashicorp.com/vault/docs](https://developer.hashicorp.com/vault/docs)
