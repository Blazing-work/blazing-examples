# curve

Curve UI
<p align="center">
<img src="https://raw.githubusercontent.com/curvefi/curve-ui/feature/add-info/assets/curve-image.jpeg" />

## Use Cases

- Decentralized finance
- Blockchain node operation
- Network validation

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
| Image | `davaymne/curve-ui:latest` |
| CPU | 0.1 |
| Memory | 512Mi |
| Storage | 2.5Gi |
| Exposed Ports | 8000 |
