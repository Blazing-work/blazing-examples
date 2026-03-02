# synthetix.exchange

The code for the [Synthetix.Exchange](https://synthetix.exchange) dApp.<br />
It is powered by [synthetix-data](https://github.com/Synthetixio/synthetix-data) and [synthetix-js](https://github.com/Synthetixio/synthetix-js).
First of all you need to create docker image and push it to docker hub.

## Use Cases

- Decentralized finance
- Blockchain node operation
- Network validation

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:80/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}/` in your browser.

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `selchenkov/synthetix.exchange:latest` |
| CPU | 1.0 |
| Memory | 512Mi |
| Storage | 512Mi |
| Exposed Ports | 80 |
