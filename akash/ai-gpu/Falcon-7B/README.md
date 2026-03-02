## Use Cases

- AI model inference
- GPU-accelerated computation
- Machine learning workloads

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
| Image | `andrey01/falcon7b:0.4` |
| CPU | 8.0 |
| Memory | 100Gi |
| Storage | 200Gi |
| Exposed Ports | 8000 |
