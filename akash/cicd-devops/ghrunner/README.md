# ghrunner

Deploy a [self-hosted runner](https://docs.github.com/en/actions/concepts/runners/self-hosted-runners) using this template.
1. Get the token for registering your runner `https://github.com/<org>/<repo>/settings/actions/runners/new`
Please see [the wiki](https://github.com/myoung34/docker-github-actions-runner/wiki/Usage) for examples and usage.

## Use Cases

- Continuous integration
- Continuous deployment
- Developer tooling

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:80/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}/` in your browser.


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `REPO_URL` | `https://github.com/<org>/<repo>` |
| `RUNNER_NAME` | `ghrunner` |

### Secrets

The following values are configured as secrets and should be set securely:

- `RUNNER_TOKEN`

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `ghcr.io/myoung34/docker-github-actions-runner:2.330.0-ubuntu-noble` |
| CPU | 1.0 |
| Memory | 2gb |
| Storage | 10gb |
| Exposed Ports | 80 |
