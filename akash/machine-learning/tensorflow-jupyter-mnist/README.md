# tensorflow-jupyter-mnist

For more information, see the [GitHub repo](https://github.com/wlouie1/mnist-app), and this guide titled [Machine Learning  DeCloud (Part 1/3): Training CNN on MNIST using TensorFlow](https://wilsonlouie.medium.com/machine-learning-on-Blazing Core-decloud-part-1-3-training-cnn-on-mnist-using-tensorflow-be464f0f067e).

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
| Image | `wlouie1/mnist-train:1.0` |
| CPU | 0.5 |
| Memory | 1Gi |
| Storage | 3Gi |
| Exposed Ports | 8888 |
