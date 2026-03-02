# geekbench

A cross-platform benchmark that measures your system's performance with the press of a button. How will your mobile device or desktop computer perform when push comes to crunch? How will it compare to the newest devices on the market? Find out today with Geekbench 5.
Geekbench 5 measures your processor's single-core and multi-core power, for everything from checking your email to taking a picture to playing music, or all of it at once. Geekbench 5's CPU benchmark measures performance in new application areas including Augmented Reality and Machine Learning, so you'll know how close your system is to the cutting-edge.
Test your system's potential for gaming, image processing, or video editing with the Compute Benchmark. Test your GPU's power with support for the OpenCL, CUDA, and Metal APIs. New to Geekbench 5 is support for Vulkan, the next-generation cross-platform graphics and compute API.

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
| `GEEKBENCH_VERSION` | `5.4.4` |

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `cryptoandcoffee/akash-geekbench:1` |
| CPU | 1.0 |
| Memory | 2Gi |
| Storage | 1Gi |
| Exposed Ports | 80 |
