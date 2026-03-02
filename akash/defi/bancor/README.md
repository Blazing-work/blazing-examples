# bancor

[Bancor](https://app.bancor.network/) is a decentralized network of on-chain automated market makers (AMMs) supporting instant, low-cost trading, as well as Single-Sided Liquidity Provision and Liquidity Protection for any listed token.
This template allows you to deploy an app from [bancorprotocol/webapp-v3](https://github.com/bancorprotocol/webapp-v3) repository .
You can create your own static website from a React app and serve it as an image . This way, image will take up less than 30 MB of disk space.

## Use Cases

- Decentralized finance
- Blockchain node operation
- Network validation

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:3000/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}:3000/` in your browser.


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `REACT_APP_ALCHEMY_MAINNET` | `(empty)` |

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `nomorelies/bancor-webapp-v3:0.0.2` |
| CPU | 1.0 |
| Memory | 2gi |
| Storage | 2gi |
| Exposed Ports | 3000 |
