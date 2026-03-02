# flan-t5-xxl

FLAN-T5 is a combination of two: a network and a model. Here, FLAN is Finetuned Language Net and T5 is a language model developed and published by Google in 2020. This model provides an improvement on the T5 model by improving the effectiveness of the zero-shot learning. FLAN-T5 model comes with many variants based on the numbers of parameters: FLAN-T5 small (80M); FLAN-T5 base (250M); FLAN-T5 large (780M); FLAN-T5 XL (3B); FLAN-T5 XXL (11B).
This deployment uses the XXL variant with 11B parameters.
Hugging Face repository https://huggingface.co/google/flan-t5-xxl

## Use Cases

- AI model inference
- GPU-accelerated computation
- Machine learning workloads

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Connect to the service on port `7575`
3. Refer to the official documentation for usage instructions

## Accessing the Service

Connect to the service on port `7575`. Replace `{SERVICE_URI}` with your deployment's assigned URI.

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `cryptopasser/flan-t5:0.5` |
| CPU | 4.0 |
| Memory | 20Gi |
| Storage | 60Gi |
| Exposed Ports | 7575 |
