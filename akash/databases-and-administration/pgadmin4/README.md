# pgadmin4

pgAdmin4
pgAdmin is the most popular and feature rich Open Source administration and development platform for PostgreSQL, the most advanced Open Source database in the world.

## Use Cases

- Persistent data storage
- Application backend
- Data management

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:80/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}/` in your browser.


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `PGADMIN_DEFAULT_EMAIL` | `admin@gmail.com` |

### Secrets

The following values are configured as secrets and should be set securely:

- `PGADMIN_DEFAULT_PASSWORD`

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `dpage/pgadmin4` |
| CPU | 1.0 |
| Memory | 1Gi |
| Storage | 1Gi |
| Exposed Ports | 80 |
