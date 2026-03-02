# Llama-3-8B

vLLM is a high-throughput, memory-efficient inference engine for large language models with an OpenAI-compatible API.

## Use Cases

- LLM inference serving
- OpenAI API drop-in replacement
- Batch text generation
- Chat completions

## Getting Started

1. Wait for the model to finish loading (check logs for "Application startup complete")
2. Send requests to the OpenAI-compatible endpoints
3. Use `/v1/models` to verify which model is loaded

## Accessing the Service

The service exposes an OpenAI-compatible API:
```bash
curl http://{SERVICE_URI}:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "MODEL_NAME", "messages": [{"role": "user", "content": "Hello!"}]}'
```


### Secrets

The following values are configured as secrets and should be set securely:

- `HF_TOKEN`

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `vllm/vllm-openai:v0.6.2` |
| CPU | 6.0 |
| Memory | 16Gi |
| Storage | 10Gi |
| Exposed Ports | 8000 |

## Documentation

For full documentation, visit: [https://docs.vllm.ai/](https://docs.vllm.ai/)
