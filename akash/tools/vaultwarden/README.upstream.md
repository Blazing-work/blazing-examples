# vaultwarden

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

Access the Vault web UI at `http://{SERVICE_URI}:80/ui/` or use the CLI:
```bash
export VAULT_ADDR="http://{SERVICE_URI}:80"
vault status
```


### Secrets

The following values are configured as secrets and should be set securely:

- `ADMIN_TOKEN`

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `vaultwarden/server:alpine` |
| CPU | 0.3 |
| Memory | 256Mi |
| Storage | 8Mi |
| Exposed Ports | 80 |

## Documentation

For full documentation, visit: [https://developer.hashicorp.com/vault/docs](https://developer.hashicorp.com/vault/docs)
