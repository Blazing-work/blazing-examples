# CockroachDB

CockroachDB is a distributed SQL database built for cloud-native applications with strong consistency and horizontal scalability.

## Use Cases

- Globally distributed applications
- Multi-region deployments
- PostgreSQL-compatible workloads
- High-availability transactional systems

## Getting Started

1. Wait for the node to report as healthy
2. Access the DB Console at `http://{URI}:8080`
3. Connect via SQL and create your first database

## Accessing the Service

Connect using the CockroachDB SQL shell:
```bash
cockroach sql --url="postgresql://{SERVICE_URI}:26257/defaultdb?sslmode=disable"
```
Or use any PostgreSQL client — CockroachDB is wire-compatible with PostgreSQL.

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `cockroachdb/cockroach:latest` |
| CPU | 1.0 |
| Memory | 1Gi |
| Storage | 1Gi |
| Exposed Ports | 26257 |

## Documentation

For full documentation, visit: [https://www.cockroachlabs.com/docs/](https://www.cockroachlabs.com/docs/)
