# tensorflow-jupyter-ezkl

For more information, see both the [GitHub repo](https://github.com/inference-labs-inc/docker-ezkl) and [EZKL](https://github.com/zkonduit/ezkl).

## Use Cases

- Model training and fine-tuning
- Data processing pipelines
- Experiment tracking

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:8888/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}:8888/` in your browser.

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `inferencelabs/ezkl-notebook` |
| CPU | 64.0 |
| Memory | 256GB |
| Storage | 100Gi |
| Exposed Ports | 8888 |
