# Tetris2 on GCP Spot

Deploy the Tetris2 demo to GCP using spot (preemptible) instances.

## Overview

This example deploys the `uzyexe/tetris` container image to a single GCP region
(europe-west1) with public HTTP ingress and **spot node pools** enabled for burst
replicas. Baseline replicas run on standard on-demand nodes; additional replicas
scale onto spot nodes at 60-90% cost savings.

## Key Concepts

- **`node_pools.burst: spot`** -- burst replicas run on preemptible VMs
- **`node_pools.baseline: standard`** -- baseline replicas stay on on-demand (guaranteed)
- **`autoscaling.min_replicas: 1`** -- one baseline replica always running on standard
- **`autoscaling.max_replicas: 3`** -- up to 2 burst replicas on spot nodes
- **`network_tier: Standard`** -- GCP Standard tier (lower cost, regional routing)
- **`network.ingress.public: true`** -- exposes port 80 via a GKE LoadBalancer

## Resources

| Resource | Value   |
|----------|---------|
| CPU      | 0.5     |
| Memory   | 512 Mi  |
| Storage  | 512 Mi  |

## Run

```bash
# Via Blazing CLI
blazing deploy --file core.yaml

# Via Blazing UI
# Paste core.yaml into the cluster editor and click Deploy
```

## Cost

GCP spot pricing is fixed and predictable at $0.0472/core/hr (vs $0.1416 on-demand).
Spot VMs can be reclaimed with 30 seconds notice, but the baseline replica on standard
nodes ensures at least one instance is always available.

| Scenario | Standard | Spot | Estimated Cost |
|----------|----------|------|----------------|
| **Baseline (1 replica)** | 1 | 0 | $0.024/hr |
| **Peak (3 replicas)** | 1 | 2 | $0.071/hr |
| **All standard** | 3 | 0 | $0.071/hr |

Monthly savings at peak: ~48% vs all-standard.
