# zammad

Zammad is a web-based, open source user support/ticketing solution. <br>
Documentation: https://docs.zammad.org

## Use Cases

- Self-hosted utility
- Productivity tool
- System administration

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:80/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}/` in your browser.

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `zammad/zammad:5.0.0-147` |
| CPU | 1.0 |
| Memory | 4Gi |
| Storage | 2Gi |
| Exposed Ports | 80 |
