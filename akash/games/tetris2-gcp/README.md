# Tetris2 on GCP

Deploy a classic JavaScript Tetris game to Google Cloud Platform.

## Overview

This example deploys the `uzyexe/tetris` container image to a single GCP region
(europe-west1) with public HTTP ingress. GCP uses fixed, predictable pricing --
no auction mechanics involved.

## Key Concepts

- **`provider: gcp`** -- routes the workload to Google Kubernetes Engine
- **`network_tier: Standard`** -- uses GCP Standard tier (lower cost, regional routing)
- **`ip_version: IPV4`** -- allocates an IPv4 external address
- **`network.ingress.public: true`** -- exposes port 80 via a GKE LoadBalancer

## Resources

| Resource | Value   |
|----------|---------|
| CPU      | 0.25    |
| Memory   | 256 Mi  |
| Storage  | 512 Mi  |

## Run

```bash
# Via Blazing CLI
blazing deploy --file core.yaml

# Via Blazing UI
# Paste core.yaml into the cluster editor and click Deploy
```

## Cost

GCP pricing is fixed and predictable. The cost tab displays **BASE / PEAK / SAVINGS**
columns based on compute, network, and storage rates for the selected region and tier.
