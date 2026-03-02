# dria

[Dria](https://dria.co/) unites consumer hardware to generate high-quality, high-throughput, low-cost synthetic data. [Dria Knowledge Network](https://dria.co/edge-ai) is a decentralized network that allows many AI agents to collaborate on tasks that improve AI/ML models with synthetic data.
A [Dria Compute Node](https://github.com/firstbatchxyz/dkn-compute-node) is a unit of computation within the Dria Knowledge Network, and it serves local / API-based LLMs to handle tasks within the network, and get rewards for it.
Check [dkn-compute-node](https://hub.docker.com/r/firstbatch/dkn-compute-node/tags) Docker repository to see if there is a new version and update `dkn` service `image`.

## Use Cases

- AI model inference
- GPU-accelerated computation
- Machine learning workloads

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:80/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}/` in your browser.


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `DKN_MODELS` | `gemma3:4b` |
| `OLLAMA_AUTO_PULL` | `true` |
| `OLLAMA_HOST` | `http://ollama` |
| `OLLAMA_PORT` | `11434` |
| `DKN_EXEC_PLATFORM` | `akash/v0.6.1` |

### Secrets

The following values are configured as secrets and should be set securely:

- `DKN_WALLET_SECRET_KEY`
- `OPENAI_API_KEY`
- `OPENROUTER_API_KEY`


## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `firstbatch/dkn-compute-node:v0.6.1` |
| CPU | 2.0 |
| Memory | 2Gi |
| Storage | 1Gi |
| Exposed Ports | 80 |


## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `ollama/ollama` |
| CPU | 4.0 |
| Memory | 10Gi |
| Storage | 24Gi |
| Exposed Ports | 11434 |
