# Github Runner — High Performance

Deploy a [self-hosted runner](https://docs.github.com/en/actions/concepts/runners/self-hosted-runners) with 32 vCPUs and 128 GB RAM using this template.

1. Get the token for registering your runner `https://github.com/<org>/<repo>/settings/actions/runners/new`
2. Set your repo & token in [deploy.yaml](deploy.yaml) file
3. Target this runner in your workflow with `runs-on: [self-hosted, dfc-32core]`

Please see [the wiki](https://github.com/myoung34/docker-github-actions-runner/wiki/Usage) for examples and usage.
