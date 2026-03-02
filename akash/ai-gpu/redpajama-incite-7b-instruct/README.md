# redpajama-incite-7b-instruct

RedPajama-INCITE-7B-Instruct is a text generation application. It was developed by Together and leaders from the open-source AI community including Ontocord.ai, ETH DS3Lab, AAI CERC, Université de Montréal, MILA - Québec AI Institute, Stanford Center for Research on Foundation Models (CRFM), Stanford Hazy Research research group and LAION.
The model was fine-tuned for few-shot applications on the data of GPT-JT, with exclusion of tasks that overlap with the HELM core scenarios.
For more information -> https://huggingface.co/togethercomputer/RedPajama-INCITE-7B-Instruct

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
| Image | `yuravorobei/redpajama_incite_7b_instruct:0.3` |
| CPU | 4.0 |
| Memory | 30Gi |
| Storage | 35Gi |
| Exposed Ports | 7860 |
