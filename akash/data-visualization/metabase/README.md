# metabase

[Metabase](https://www.metabase.com/) is the easy, open-source way for everyone in your company to ask questions and learn from data.
3. Open URI from Leases tab to access Metabase.
For more information, please see the [Running Metabase on Docker](https://www.metabase.com/docs/latest/installation-and-operation/running-metabase-on-dockeress) documentation.

## Use Cases

- Data dashboards
- Analytics visualization
- Reporting

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:3000/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}:3000/` in your browser.


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `MB_DB_TYPE` | `postgres` |
| `MB_DB_DBNAME` | `metabaseappdb` |
| `MB_DB_PORT` | `5432` |
| `MB_DB_USER` | `metabase` |
| `MB_DB_PASS` | `mysecretpassword` |
| `MB_DB_HOST` | `postgres` |
| `POSTGRES_USER` | `metabase` |
| `POSTGRES_DB` | `metabaseappdb` |

### Secrets

The following values are configured as secrets and should be set securely:

- `POSTGRES_PASSWORD`


## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `metabase/metabase:v0.54.19.3` |
| CPU | 1.0 |
| Memory | 1Gi |
| Storage | 2Gi |
| Exposed Ports | 3000 |


## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `postgres:14.19-alpine3.21` |
| CPU | 1.0 |
| Memory | 1Gi |
| Storage | 2Gi |
| Exposed Ports | 5432 |
