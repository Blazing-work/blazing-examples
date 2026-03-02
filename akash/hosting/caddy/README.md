# caddy

Caddy 2 is a powerful, enterprise-ready, open source web server with automatic HTTPS written in Go.

## Use Cases

- Web hosting
- Application deployment
- Static site serving

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:80/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}/` in your browser.

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `stefanprodan/caddy` |
| CPU | 1.0 |
| Memory | 512Mi |
| Storage | 512Mi |
| Exposed Ports | 80 |
