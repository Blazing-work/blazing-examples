# doccano

For more information about management of user, please visit the official documentation at <https://doccano.github.io/doccano/>.

## Use Cases

- Model training and fine-tuning
- Data processing pipelines
- Experiment tracking

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


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `ADMIN_USERNAME` | `admin` |
| `ADMIN_EMAIL` | `admin@example.com` |

### Secrets

The following values are configured as secrets and should be set securely:

- `ADMIN_PASSWORD`

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `doccano/doccano` |
| CPU | 1.0 |
| Memory | 512Mi |
| Storage | 2048Mi |
| Exposed Ports | 8000 |
