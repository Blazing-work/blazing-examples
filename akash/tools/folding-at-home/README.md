# folding-at-home

Folding@home
Contribute towards disease research, by using spare processing capacity to perform calculations for the [Folding@home project][https://foldingathome.org/].
Docker image from [yurinnick](https://github.com/yurinnick/folding-at-home-docker).

## Use Cases

- Self-hosted utility
- Productivity tool
- System administration

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Connect to the service on port `7396`
3. Refer to the official documentation for usage instructions

## Accessing the Service

Connect to the service on port `7396`. Replace `{SERVICE_URI}` with your deployment's assigned URI.


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `TEAM` | `0` |
| `ENABLE_GPU` | `false` |
| `ENABLE_SMP` | `true` |

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `yurinnick/folding-at-home:latest` |
| CPU | 1.0 |
| Memory | 1Gi |
| Storage | 1Gi |
| Exposed Ports | 7396 |
