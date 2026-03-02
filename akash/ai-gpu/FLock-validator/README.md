# FLock-validator

[train.flock.io](http://train.flock.io/) is the gateway to [FLock.io](http://flock.io/)'s decentralized AI training platform, AI Arena. It is currently on incentivised testnet, and all participants who have earned FML rewards will receive mainnet airdrops.
To participate, you need to first [get whitelisted](https://blog.flock.io/news/trainflock), acquire [FML test tokens](https://train.flock.io/faucet) and test tokens for Base Sepolia, then [stake FML](https://train.flock.io/stake) on the task you wish to validate.  Afterwards, you can use this template to run validation script with Blazing Core compute; the script will fetch validation tasks and send scores automatically.
[FLock.io](http://flock.io/) is a decentralised AI co-creation platform aimed at democratising AI development and alignment, battling the concentration of power and data ownership in centralised corporations. It closed a $6m seed round in March 2024, led by Lightspeed Faction with participation from DCG, Volt, OKX Ventures among others. The core team, from Oxford University, has 10+ years of AI and blockchain experience.

## Use Cases

- AI model inference
- GPU-accelerated computation
- Machine learning workloads

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:3000/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}:3000/` in your browser.


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `TASK_ID` | `(empty)` |

### Secrets

The following values are configured as secrets and should be set securely:

- `FLOCK_API_KEY`
- `HF_TOKEN`

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `ghcr.io/flock-io/llm-loss-validator:v1.1.2` |
| CPU | 8.0 |
| Memory | 24Gi |
| Storage | 100Gi |
| Exposed Ports | 3000 |
