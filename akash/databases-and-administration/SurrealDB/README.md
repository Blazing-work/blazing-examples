# SurrealDB

SurrealDB is the ultimate cloud database for tomorrow's applications
With an SQL-style query language, real-time queries with highly-efficient related data retrieval, advanced security permissions for multi-tenant access, and support for performant analytical workloads, SurrealDB is the next generation serverless database.

## Use Cases

- Persistent data storage
- Application backend
- Data management

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Send HTTP requests to `http://{SERVICE_URI}:8000/`
3. Check the service documentation for available API endpoints

## Accessing the Service

Send requests to `http://{SERVICE_URI}:8000/`.

Example:
```bash
curl http://{SERVICE_URI}:8000/
```

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `surrealdb/surrealdb:1.0.0-beta.8` |
| CPU | 1.0 |
| Memory | 1Gi |
| Storage | 1Gi |
| Exposed Ports | 8000 |
