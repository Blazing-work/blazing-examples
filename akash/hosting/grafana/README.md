# grafana

Grafana is the leading open-source platform for monitoring and observability, with support for Prometheus, Graphite, InfluxDB, and many more data sources.

## Use Cases

- Infrastructure monitoring dashboards
- Application performance monitoring
- Log aggregation visualization
- Business metrics and KPIs
- Alerting and notifications

## Getting Started

1. Log in with admin/admin and set a new password
2. Add your first data source (Prometheus, InfluxDB, etc.)
3. Import a community dashboard or create your own
4. Set up alerting rules for critical metrics

## Accessing the Service

Open the Grafana web UI at `http://{SERVICE_URI}:3000/`

### Default Credentials

- **Username**: `admin`
- **Password**: admin (you will be prompted to change on first login)

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `grafana/grafana` |
| CPU | 1.0 |
| Memory | 1Gi |
| Storage | 512Mi |
| Exposed Ports | 3000 |

## Documentation

For full documentation, visit: [https://grafana.com/docs/grafana/latest/](https://grafana.com/docs/grafana/latest/)
