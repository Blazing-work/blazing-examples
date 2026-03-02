# minio

MinIO is a high-performance, S3-compatible object storage system designed for large-scale data infrastructure.

## Use Cases

- S3-compatible object storage
- Data lake storage
- Backup and archival
- AI/ML training data storage
- Container-native storage

## Getting Started

1. Access the MinIO Console at port 9001
2. Create your first bucket
3. Use `mc` CLI or any S3-compatible SDK to upload objects

## Accessing the Service

Access the MinIO Console (web UI) at `http://{SERVICE_URI}:9001/` or use the S3 API at `http://{SERVICE_URI}:9000/`

### Default Credentials

- **Username**: `Set via `MINIO_ROOT_USER``
- **Password**: Set via `MINIO_ROOT_PASSWORD`

## Configuration

- `MINIO_ROOT_USER` sets the admin access key
- `MINIO_ROOT_PASSWORD` sets the admin secret key

### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `AWS_DEFAULT_REGION` | `us-east-1` |
| `AWS_ACCESS_KEY_ID` | `minio` |

### Secrets

The following values are configured as secrets and should be set securely:

- `MINIO_ACCESS_KEY`
- `MINIO_SECRET_KEY`
- `AWS_SECRET_ACCESS_KEY`

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `minio/minio:latest` |
| CPU | 2.0 |
| Memory | 20Gi |
| Storage | 100Gi |
| Exposed Ports | 9000 |

## Documentation

For full documentation, visit: [https://min.io/docs/minio/linux/index.html](https://min.io/docs/minio/linux/index.html)
