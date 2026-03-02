# bitcoincashnode

Bitcoin Cash
============
Bitcoin Cash is a digital currency that enables instant payments to anyone, anywhere in the world. It uses peer-to-peer technology to operate with no central authority: managing transactions and issuing money are carried out collectively by the network. Bitcoin Cash is a descendant of Bitcoin. It became a separate currency from the version supported by Bitcoin Core when the two split on August 1, 2017. Bitcoin Cash and the Bitcoin Core version of Bitcoin share the same transaction history up until the split.

## Use Cases

- Blockchain node operation
- Validator services
- Decentralized network participation

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:8332/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}:8332/` in your browser or send HTTP requests to this address.

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `ghcr.io/ubunteroz/akash-bitcoincashnode:latest` |
| CPU | 4.0 |
| Memory | 16Gi |
| Storage | 128Gi |
| Exposed Ports | 8332 |
