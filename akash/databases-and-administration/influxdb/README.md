# influxdb

InfluxDB is a time series database built from the ground up to handle high write and query loads.
InfluxDB is meant to be used as a backing store for any use case involving large amounts of
timestamped data, including DevOps monitoring, application metrics, IoT sensor data, and

## Use Cases

- Persistent data storage
- Application backend
- Data management

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:8086/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}:8086/` in your browser or send HTTP requests to this address.


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `INFLUXDB_ADMIN_USER` | `admin` |

### Secrets

The following values are configured as secrets and should be set securely:

- `INFLUXDB_ADMIN_PASSWORD`

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `influxdb` |
| CPU | 1.0 |
| Memory | 1Gi |
| Storage | 1Gi |
| Exposed Ports | 8086 |
