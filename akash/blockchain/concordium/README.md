# concordium

A template for running a mainnet node on the Concordium blockchain.
[Concordium docs](https://docs.concordium.com/en/mainnet/docs/index.html)
[Support portal](https://forum.concordium.com/)

## Use Cases

- Blockchain node operation
- Validator services
- Decentralized network participation

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Connect to the service on port `20000`
3. Refer to the official documentation for usage instructions

## Accessing the Service

Connect to the service on port `20000`. Replace `{SERVICE_URI}` with your deployment's assigned URI.


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `CONCORDIUM_NODE_CONNECTION_BOOTSTRAP_NODES` | `bootstrap.mainnet.concordium.software:8888` |
| `CONCORDIUM_NODE_CONSENSUS_GENESIS_DATA_FILE` | `/mainnet-genesis.dat` |
| `CONCORDIUM_NODE_CONSENSUS_DOWNLOAD_BLOCKS_FROM` | `https://catchup.mainnet.concordium.software/blocks.idx` |
| `CONCORDIUM_NODE_DATA_DIR` | `/mnt/data` |
| `CONCORDIUM_NODE_CONFIG_DIR` | `/mnt/data` |
| `CONCORDIUM_NODE_LISTEN_PORT` | `8888` |
| `CONCORDIUM_NODE_CONNECTION_DESIRED_NODES` | `5` |
| `CONCORDIUM_NODE_CONNECTION_MAX_ALLOWED_NODES` | `10` |
| `CONCORDIUM_NODE_GRPC2_LISTEN_ADDRESS` | `0.0.0.0` |
| `CONCORDIUM_NODE_GRPC2_LISTEN_PORT` | `20000` |
| `CONCORDIUM_NODE_CONNECTION_HARD_CONNECTION_LIMIT` | `20` |
| `CONCORDIUM_NODE_CONNECTION_THREAD_POOL_SIZE` | `2` |
| `CONCORDIUM_NODE_CONNECTION_BOOTSTRAPPING_INTERVAL` | `1800` |
| `CONCORDIUM_NODE_RUNTIME_HASKELL_RTS_FLAGS` | `-N2,-I0` |
| `CONCORDIUM_NODE_COLLECTOR_NODE_NAME` | `Concordium_node` |
| `CONCORDIUM_NODE_COLLECTOR_URL` | `https://dashboard.mainnet.concordium.software/nodes/post` |
| `CONCORDIUM_NODE_COLLECTOR_COLLECT_INTERVAL` | `5000` |
| `CONCORDIUM_NODE_COLLECTOR_GRPC_HOST` | `http://mainnet-node:20000` |


## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `concordium/mainnet-node:10.0.5-0` |
| CPU | 4.0 |
| Memory | 8Gi |
| Storage | 300Gi |
| Exposed Ports | 20000 |


## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `concordium/mainnet-node:10.0.5-0` |
| CPU | 0.5 |
| Memory | 1Gi |
| Storage | 1Gi |
| Exposed Ports | 20000 |
