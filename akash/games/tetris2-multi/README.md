# Tetris2 Multi-Provider

Deploy a classic JavaScript Tetris game across three cloud providers simultaneously.

## Overview

This example deploys the `uzyexe/tetris` container image to a single cluster spanning
three providers at once: Akash, GCP, and DFC. Each provider has its own region,
pricing model, and infrastructure characteristics. This is the most comprehensive
Tetris2 deployment variant, demonstrating Blazing Core's multi-cloud orchestration.

## Providers

| Provider | Region            | Pricing Model   | Primary |
|----------|-------------------|-----------------|---------|
| Akash    | akash-global      | Reverse auction | Yes     |
| GCP      | gcp-europe-west1  | Fixed (Standard)| No      |
| DFC      | dfc-pt-lisbon     | Fixed (Spot)    | No      |

## Key Concepts

- **`providers.akash.max_price: 15.00`** -- sets the Akash reverse-auction bid cap
- **`providers.gcp.network_tier: Standard`** -- GCP Standard tier for cost savings
- **`providers.dfc.status: prefer`** -- DFC uses Akash blockchain infrastructure
- **3 explicit regions** -- workload is deployed to all three simultaneously
- **Mixed pricing** -- each region has its own cost model visible in the cost tab

## Resources (per region)

| Resource | Value   |
|----------|---------|
| CPU      | 1.0     |
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

Because the cluster includes an Akash region (`hasAkashRegion=true`), the cost tab
displays **PERIOD | MAX** columns instead of BASE/PEAK/SAVINGS. The header shows
"MAX MONTHLY:" with an Akash reverse-auction indicator. The per-region breakdown
lists all 3 providers, with the Akash row showing an amber MAX badge.
