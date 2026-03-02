# witnesschain-watchtower

To participate, you need to first [register your Watchtower Keys](https://docs.witnesschain.com/infinity-watch/proof-of-location-mainnet/run-a-watchtower/for-partner-node-runners/running-on-Blazing Core-cloud#id-1.-registering-the-watchtower-key).  Afterwards, you can use this template to configure and run the Witness Chain watchtower with Blazing Core compute; the watchtower will prove itself first and then enable a PoL challenger automatically.
[Witness Chain](http://witnesschain.com/) is a decentralised verifiable observation network of watchtowers; witnessing and processing data from devices connecting physical world, spread all over the globe. This network of observed physical attributes are then programmed for state-of-the-art physical state consensus protocols like proof of location, proof of bandwidth etc. Unlocking a whole new programmable witness paradigm!
For comprehensive guides and documentation, refer to the [documentation](https://docs.witnesschain.com/).

## Use Cases

- Blockchain node operation
- Validator services
- Decentralized network participation

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:80/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}/` in your browser.


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `latitude` | `(empty)` |
| `longitude` | `(empty)` |
| `radius` | `1000` |
| `privateKey` | `(empty)` |
| `walletPublicKey` | `(empty)` |
| `keyType` | `ethereum` |
| `havePublicIPv4Address` | `false` |
| `havePublicIPv6Address` | `false` |
| `havePrivateIPv4Address` | `false` |
| `havePrivateIPv6Address` | `false` |
| `saveResultsInDatabase` | `false` |
| `submitResultsToContract` | `false` |
| `projectName` | `Blazing Core` |
| `rpcUrl` | `https://rpc.witnesschain.com` |

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `witnesschain/infinity-watch:1.0.0` |
| CPU | 1.0 |
| Memory | 1Gi |
| Storage | 5Gi |
| Exposed Ports | 80 |
