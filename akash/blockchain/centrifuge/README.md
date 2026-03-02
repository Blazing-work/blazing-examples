# centrifuge

Centrifuge Chain is blockchain built with Rust and the Polkadot SDK, purpose built for real-world assets.
To access the JSON-RPC server and check the synchronization status, run the following `curl` command:
curl -X POST \

## Use Cases

- Blockchain node operation
- Validator services
- Decentralized network participation

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:9933/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}:9933/` in your browser or send HTTP requests to this address.

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `centrifugeio/centrifuge-chain:v0.15.6` |
| CPU | 4.0 |
| Memory | 16GB |
| Storage | 1Ti |
| Exposed Ports | 9933 |
