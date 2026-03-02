# Axolotlai

## Use Cases

- AI model inference
- GPU-accelerated computation
- Machine learning workloads

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:8888/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}:8888/` in your browser.

### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `HF_DATASETS_CACHE` | `/workspace/data/huggingface-cache/datasets` |
| `HUGGINGFACE_HUB_CACHE` | `/workspace/data/huggingface-cache/hub` |
| `TRANSFORMERS_CACHE` | `/workspace/data/huggingface-cache/hub` |
| `BASE_VOLUME` | `/workspace/data` |
| `AXOLOTL_CONFIG_DIR` | `/src/config` |
| `JUPYTER_ENABLE_LAB` | `yes` |

### Secrets

The following values are configured as secrets and should be set securely:

- `WANDB_API_KEY`
- `HF_TOKEN`
- `JUPYTER_TOKEN`

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `axolotlai/axolotl-cloud:main-latest` |
| CPU | 24.0 |
| Memory | 251Gi |
| Storage | 550Gi |
| Exposed Ports | 8888 |
