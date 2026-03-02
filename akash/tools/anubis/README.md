# anubis

Anubis weighs the soul of your connection using a proof-of-work challenge in order to protect upstream resources from scraper bots.
TL;DR: If you don't want to use (centralized) solution like Cloudflare to protect your system from bots, use Anubis.
**From the docs:**

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


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `BIND` | `:8080` |
| `DIFFICULTY` | `4` |
| `METRICS_BIND` | `:9090` |
| `SERVE_ROBOTS_TXT` | `true` |
| `TARGET` | `http://nginx` |
| `OG_PASSTHROUGH` | `true` |
| `OG_EXPIRY_TIME` | `24h` |


## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `ghcr.io/techarohq/anubis:latest` |
| CPU | 1.0 |
| Memory | 1Gi |
| Storage | 200Mi |
| Exposed Ports | 8080 |


## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `nginx` |
| CPU | 0.1 |
| Memory | 256Mi |
| Exposed Ports | 80 |
