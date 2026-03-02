# gogs

Gogs is a painless self-hosted Git service.
3. Open URI from Leases tab with forwarded port 3000 to access Gogs.
For more information, please see the [Docker for Gogs](https://github.com/gogs/gogs/tree/main/docker) documentation.

## Use Cases

- Continuous integration
- Continuous deployment
- Developer tooling

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Connect to the service on port `22`
3. Refer to the official documentation for usage instructions

## Accessing the Service

Connect to the service on port `22`. Replace `{SERVICE_URI}` with your deployment's assigned URI.

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `gogs/gogs:0.13` |
| CPU | 2.0 |
| Memory | 512Mi |
| Storage | 1Gi |
| Exposed Ports | 22 |
