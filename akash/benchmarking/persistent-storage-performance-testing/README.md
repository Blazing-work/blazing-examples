# persistent-storage-performance-testing

How to use:
1. specify the storage class of the provider you want to test (beta1, beta2 or beta3)
2. Specify the root password in case you wish to connect to your deployment via ssh (not neccessary)

## Use Cases

- Performance testing
- System benchmarking
- Network testing

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:80/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}/` in your browser.


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `my_root_password` | `{{my_root_password}}` |

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `ubuntu:latest` |
| CPU | 1.0 |
| Memory | 1Gi |
| Storage | 10Gi |
| Exposed Ports | 80 |
