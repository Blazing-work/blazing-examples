# postgres

PostgreSQL is a powerful, open-source object-relational database system with over 35 years of active development.

## Use Cases

- Application backend storage
- Data warehousing and analytics
- Geospatial data with PostGIS
- JSON document storage

## Getting Started

1. Wait for the service to reach "Running" status
2. Connect with the credentials configured in your deployment
3. Create your application tables and start querying

## Accessing the Service

Connect using any PostgreSQL client:
```bash
psql -h {SERVICE_URI} -p 5432 -U admin -d mydb
```

### Default Credentials

- **Username**: `admin`
- **Password**: Set via `POSTGRES_PASSWORD` secret

## Configuration

- `POSTGRES_DB` sets the default database name
- `POSTGRES_USER` sets the superuser name
- `PGDATA` controls where data files are stored

### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `PGDATA` | `/var/lib/postgresql/data/pgdata` |
| `POSTGRES_USER` | `admin` |
| `POSTGRES_DB` | `mydb` |

### Secrets

The following values are configured as secrets and should be set securely:

- `POSTGRES_PASSWORD`

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `postgres` |
| CPU | 1.0 |
| Memory | 1Gi |
| Storage | 1Gi |
| Exposed Ports | 5432 |

## Documentation

For full documentation, visit: [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/)
