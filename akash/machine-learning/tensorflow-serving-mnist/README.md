# tensorflow-serving-mnist

For more information, see the [GitHub repo](https://github.com/wlouie1/mnist-app), and this guide titled [Machine Learning  DeCloud (Part 2/3): TensorFlow Model Serving](https://wilsonlouie.medium.com/machine-learning-on-Blazing Core-decloud-part-2-3-tensorflow-model-serving-12e30d77a156).

## Use Cases

- Model training and fine-tuning
- Data processing pipelines
- Experiment tracking

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:8501/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}:8501/` in your browser or send HTTP requests to this address.

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `wlouie1/mnist-tf-serve:1.0` |
| CPU | 0.2 |
| Memory | 512Mi |
| Storage | 512Mi |
| Exposed Ports | 8501 |
