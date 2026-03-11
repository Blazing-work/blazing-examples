# Tetris2 on DFC

Deploy a classic JavaScript Tetris game to DFC (Digital Frontier Cloud).

## Overview

This example deploys the `uzyexe/tetris` container image to a single DFC region
(dfc-pt-lisbon, Lisbon, Portugal) with public HTTP ingress. DFC is an Akash-compatible
provider that uses Akash blockchain infrastructure underneath, but with fixed Spot pricing
instead of reverse-auction mechanics.

## Key Concepts

- **`providers.dfc.status: prefer`** -- routes the workload to DFC providers
- **`region_id: dfc-pt-lisbon`** -- DFC's Lisbon datacenter
- **`network.ingress.public: true`** -- exposes port 80 via a public URI
- **Akash blockchain IDs** -- deployments get `dseq` and `provider_address` from the Akash contract

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

DFC uses fixed Spot pricing (not reverse auction). The cost tab displays
**BASE / PEAK / SAVINGS** columns, similar to GCP. Despite running on Akash
infrastructure, DFC cost rendering follows the GCP display path.
