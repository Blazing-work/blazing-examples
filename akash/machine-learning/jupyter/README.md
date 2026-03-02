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
| Image | `jupyter/tensorflow-notebook` |
| CPU | 2.0 |
| Memory | 2Gi |
| Storage | 10Gi |
| Exposed Ports | 8888 |
