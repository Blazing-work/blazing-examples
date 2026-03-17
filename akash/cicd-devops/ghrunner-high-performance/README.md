# GitHub CI Runner — 32-Core / 128 GB on DFC

Deploy a high-performance [self-hosted GitHub Actions runner](https://docs.github.com/en/actions/concepts/runners/self-hosted-runners) with 32 vCPUs and 128 GB RAM on DFC.

Sized for monorepo builds, parallel test suites, container image builds (via Podman), and heavy compilation workloads.

## Setup

1. Get a runner registration token from `https://github.com/<org>/<repo>/settings/actions/runners/new`
2. Store it as a secret named `runner_token` in your Blazing project
3. Update `REPO_URL` in `core.yaml` to point to your repository (or replace with `ORG_NAME` for org-level runners)
4. Deploy with `blazing deploy`

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `REPO_URL` | — | Target repository (e.g., `https://github.com/acme/monorepo`) |
| `RUNNER_NAME` | `dfc-32core` | Runner name visible in GitHub Actions |
| `RUNNER_LABELS` | `self-hosted,linux,x64,dfc-32core` | Labels for job routing |
| `EPHEMERAL` | `true` | Fresh container per job (recommended for security) |

## Container Builds with Podman

Docker-in-Docker requires privileged mode, which Akash providers block. This template uses **Podman** instead — a rootless, daemonless, Docker-compatible container engine that works in unprivileged environments.

Install Podman as a step in your workflow, or bake it into a custom runner image:

```yaml
jobs:
  build:
    runs-on: [self-hosted, dfc-32core]
    steps:
      - uses: actions/checkout@v4
      - name: Install Podman
        run: apt-get update && apt-get install -y podman
      - name: Build and push image
        run: |
          podman build -t ghcr.io/org/myapp:latest .
          podman login ghcr.io -u ${{ github.actor }} -p ${{ secrets.GITHUB_TOKEN }}
          podman push ghcr.io/org/myapp:latest
```

Podman is a drop-in replacement for Docker CLI — `podman build`, `podman run`, `podman push` all work the same way.

## Usage in GitHub Actions

```yaml
jobs:
  build:
    runs-on: [self-hosted, dfc-32core]
    steps:
      - uses: actions/checkout@v4
      - run: make build -j32
```

## Org-Level Runner

To register the runner at the org level (serves all repos), replace `REPO_URL` with:

```yaml
variables:
  ORG_NAME: your-github-org
  RUNNER_NAME: dfc-32core
  RUNNER_LABELS: self-hosted,linux,x64,dfc-32core
  RUNNER_SCOPE: org
```

## Notes

- **Ephemeral mode**: The runner container is destroyed after each job. This prevents state leakage between jobs and is the recommended approach for shared runners.
- **Why Podman over Docker**: Akash and DFC run workloads in unprivileged containers. Docker-in-Docker needs `--privileged` for nested cgroups and overlayfs. Podman runs entirely in userspace with no daemon — fully compatible with unprivileged environments.
- **Storage**: 100 GB accommodates large monorepo checkouts, Podman layer caches, and build artifacts. Increase if your builds require more workspace.
- **DFC preferred**: `core.yaml` routes to DFC first with Akash fallback. `core.raw.yaml` uses Akash only.

See the [runner image wiki](https://github.com/myoung34/docker-github-actions-runner/wiki/Usage) for full configuration options.
