# Tetris2 on Akash

Deploy a classic JavaScript Tetris game to the Akash decentralized cloud.

## Overview

This example deploys the `uzyexe/tetris` container image to a single Akash region
with public HTTP ingress. Akash uses reverse-auction pricing -- you set a `max_price`
bid and providers compete to host your workload at the lowest cost.

## Key Concepts

- **`providers.akash.status: prefer`** -- routes the workload to Akash providers
- **`max_price: 15.00`** -- maximum monthly bid in USD for the reverse auction
- **`region_id: akash-global`** -- Akash's global provider pool (no fixed geography)
- **`network.ingress.public: true`** -- exposes port 80 via a public URI assigned by the provider

## Resources

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

Akash pricing is determined by reverse auction. The cost tab displays **PERIOD | MAX**
columns. Your actual cost will be at or below the `max_price` bid.
