# shiori

Shiori is a simple bookmarks manager written in the Go language.
Open URI from Leases tab to access web interface. Default user to access web interface:
username: shiori

## Use Cases

- Self-hosted utility
- Productivity tool
- System administration

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:8080/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}:8080/` in your browser.


### Secrets

The following values are configured as secrets and should be set securely:

- `SHIORI_HTTP_SECRET_KEY`

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `ghcr.io/go-shiori/shiori:v1.8.0-2-g585ea34` |
| CPU | 0.1 |
| Memory | 512Mi |
| Storage | 1Gi |
| Exposed Ports | 8080 |
