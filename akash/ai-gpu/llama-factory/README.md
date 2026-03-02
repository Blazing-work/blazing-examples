# llama-factory

LLaMA-Factory is the #1 most requested open-source AI training/fine-tuning platform with 54k GitHub stars. It supports WebUI for no-code fine-tuning (just click and train), over 100 foundation models (Llama, Mistral, Qwen), built-in datasets, and one-click deployment.
After deployment, access the LLaMA-Factory WebUI at the provided endpoint on port 7860.
- Models: LLaMA, LLaVA, Mistral, Mixtral-MoE, Qwen, Qwen2-VL, DeepSeek, Yi, Gemma, ChatGLM, Phi, etc.

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
| Image | `hiyouga/llamafactory:latest` |
| CPU | 16.0 |
| Memory | 128Gi |
| Storage | 500Gi |
| Exposed Ports | 7860 |
