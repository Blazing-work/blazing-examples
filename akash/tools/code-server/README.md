# Code Server

## Use Cases

- Self-hosted utility
- Productivity tool
- System administration

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:8443/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}:8443/` in your browser or send HTTP requests to this address.

### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `PUID` | `1000` |
| `PGID` | `1000` |
| `PASSWORD` | `password` |

### Secrets

The following values are configured as secrets and should be set securely:

- `SUDO_PASSWORD`

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `ghcr.io/linuxserver/code-server` |
| CPU | 2.0 |
| Memory | 4Gi |
| Storage | 1Gi |
| Exposed Ports | 8443 |
