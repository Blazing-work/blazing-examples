# bitbucket

Bitbucket Server (now Bitbucket Data Center) is a self-hosted Git repository management solution with built-in CI/CD.

## Use Cases

- Self-hosted Git hosting
- Code review with pull requests
- CI/CD pipelines
- Branch permissions and code quality gates

## Getting Started

1. Complete the setup wizard with your license key
2. Create your first project and repository
3. Clone and push code using Git over HTTP or SSH

## Accessing the Service

Open the Bitbucket web interface at `http://{SERVICE_URI}:7990/`

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `atlassian/bitbucket-server:8.2.1` |
| CPU | 2.0 |
| Memory | 4gi |
| Storage | 4Gi |
| Exposed Ports | 7990 |

## Documentation

For full documentation, visit: [https://support.atlassian.com/bitbucket-data-center/](https://support.atlassian.com/bitbucket-data-center/)
