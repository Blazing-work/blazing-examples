# gitea

Gitea is a lightweight, self-hosted Git service providing repository hosting, code review, and CI/CD.

## Use Cases

- Self-hosted Git repository management
- Code review and pull requests
- CI/CD pipelines with Gitea Actions
- Team collaboration and project management

## Getting Started

1. Navigate to the web UI to complete the installation wizard
2. Create your first repository
3. Push code using Git over HTTP or SSH

## Accessing the Service

Open the Gitea web interface at `http://{SERVICE_URI}:3000/`

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `gitea/gitea:1.25.0-rc0-rootless` |
| CPU | 0.5 |
| Memory | 1gi |
| Storage | 1Gi |
| Exposed Ports | 3000 |

## Documentation

For full documentation, visit: [https://docs.gitea.io/](https://docs.gitea.io/)
