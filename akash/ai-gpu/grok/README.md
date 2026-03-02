# grok

<img src="grok-app.png">
Grok-1 is a 314 billion parameter Mixture-of-Experts model trained from scratch by xAI.
This deployment requires 8x H100 80GB or equivalent GPUs. With ~400 MB/s download speed, downloading grok model can take up to 25 minutes, while loading checkpoints can take up to 10 minutes.

## Use Cases

- AI model inference
- GPU-accelerated computation
- Machine learning workloads

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:8080/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}:8080/` in your browser.


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `MAX_NEW_TOKENS` | `256` |

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `cvpfus/grok-Blazing Core:0.20` |
| CPU | 64.0 |
| Memory | 1280Gi |
| Storage | 2048Gi |
| Exposed Ports | 8080 |
