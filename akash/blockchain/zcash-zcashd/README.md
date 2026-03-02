# zcash-zcashd

Zcashd is a full node written in C++. For a step-by-step guide on how to deploy and configure your SDL, check out the [ZecHub DAO guide here.](https://github.com/ZecHub/zechub/blob/main/site/guides/Akash_Network_zcashd.md)
Source Code: <https://github.com/ZcashFoundation/zcashd>

## Use Cases

- Blockchain node operation
- Validator services
- Decentralized network participation

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:8233/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}:8233/` in your browser or send HTTP requests to this address.


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `ZCASHD_NETWORK` | `mainnet` |
| `ZCASHD_SHOWMETRICS` | `1` |

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `electriccoinco/zcashd` |
| CPU | 4.0 |
| Memory | 16Gi |
| Storage | 350Gi |
| Exposed Ports | 8233 |
