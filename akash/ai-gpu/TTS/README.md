# TTS

[TTS](https://github.com/coqui-ai/TTS) is a library for advanced Text-to-Speech generation. It's built on the latest research, was designed to achieve the best trade-off among ease-of-training, speed and quality. TTS comes with pretrained models, tools for measuring dataset quality and already used in 20+ languages for products and research projects.
[TTS Docs](https://tts.readthedocs.io/en/latest/index.html)
[Docker Images](https://tts.readthedocs.io/en/latest/docker_images.html)

## Use Cases

- AI model inference
- GPU-accelerated computation
- Machine learning workloads

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Send HTTP requests to `http://{SERVICE_URI}:5002/`
3. Check the service documentation for available API endpoints

## Accessing the Service

Send requests to `http://{SERVICE_URI}:5002/`.

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `nomorelies/tts:v1.0` |
| CPU | 4.0 |
| Memory | 8Gi |
| Storage | 16Gi |
| Exposed Ports | 5002 |
