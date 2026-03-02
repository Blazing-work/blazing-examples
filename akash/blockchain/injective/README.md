# injective

Injective’s mission is to create a truly free and inclusive financial system through decentralization.
With the fastest blockchain built for finance, and plug-and-play Web3 modules, Injective’s ecosystem is reshaping a broken financial system with dApps that are highly interoperable, scalable and truly decentralized.

## Use Cases

- Blockchain node operation
- Validator services
- Decentralized network participation

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:9090/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}:9090/` in your browser.


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `MONIKER` | `my-moniker-1` |
| `CHAIN_JSON` | `https://raw.githubusercontent.com/cosmos/chain-registry/m...` |
| `P2P_POLKACHU` | `1` |
| `SNAPSHOT_DATA_PATH` | `data` |
| `SNAPSHOT_WASM_PATH` | `wasm` |
| `SNAPSHOT_URL` | `https://tools.highstakes.ch/files/injective.tar.gz` |
| `MINIMUM_GAS_PRICES` | `500000000inj` |
| `INJECTIVED_IAVL_DISABLE_FASTNODE` | `true` |
| `INJECTIVED_API_ENABLE` | `true` |

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `ghcr.io/akash-network/cosmos-omnibus:v0.3.42-injective-v1.11.6-1688984159` |
| CPU | 8.0 |
| Memory | 64Gi |
| Storage | 7Gi |
| Exposed Ports | 9090 |
