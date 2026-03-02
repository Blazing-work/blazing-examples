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
| Image | `ghcr.io/ovrclk/goosebin:20210902b` |
| CPU | 0.1 |
| Memory | 256Mi |
| Exposed Ports | 8000 |


## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `redis:6.2.5` |
| CPU | 0.1 |
| Memory | 256Mi |
| Exposed Ports | 6379 |
