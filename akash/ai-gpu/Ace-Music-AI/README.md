# Ace Music AI

## Use Cases

- AI model inference
- GPU-accelerated computation
- Machine learning workloads

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:7860/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}:7860/` in your browser.

This port is commonly used by Gradio and Streamlit applications.

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `rodrirr/acw:latest` |
| CPU | 4.0 |
| Memory | 16Gi |
| Storage | 100Gi |
| Exposed Ports | 7860 |
