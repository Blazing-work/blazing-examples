# postgres-restore

An auto-restoring Postgres server running , with backups taken on a configurable schedule. Backups are stored on decentralised storage using Filebase.
Ultimately this is a two container setup, one PostgreSQL server and one scheduler container to restore the database on boot, and run a cronjob to back it up.
See [ovrclk/akash-postgres-restore](https://github.com/ovrclk/akash-postgres-restore) for more information.


### Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `ghcr.io/ovrclk/akash-postgres-restore:v0.0.4` |
| CPU | 1.0 |
| Memory | 1Gi |
| Storage | 1Gi |


### Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `postgres:12.6` |
| CPU | 1.0 |
| Memory | 1Gi |
| Storage | 1Gi |
| Exposed Ports | 5432 |
