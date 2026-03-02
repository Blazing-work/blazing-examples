# status

[Status](https://status.app) is an open source, decentralised crypto communication super app. This deployment manifest allows you to run a bootstrap and service node allowing your (and others) to discover peers and receive/publish messages from resource restricted devices (e.g. phones). Apart from potentially being useful to you as a user directy, it also helps harden and decentralize the communication infrastructure ([Waku](http://waku.org)) which Status leverages.
It is recommended to provide a `NODEKEY` environment variable which is the node private key used to derive a `peerId` - public identifier of the node. If you do not provide it, a random key will be generated on restart.
The node requires a public IP, so once you initially deploy, you need to find the leased IP address and provide it in `IP_ADDR` environment variable and update the deployment. This will result in node being able to advertise itself to the network.

## Use Cases

- Real-time messaging
- Team communication
- Chat platform hosting

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Connect to the service on port `60000`
3. Refer to the official documentation for usage instructions

## Accessing the Service

Connect to the service on port `60000`. Replace `{SERVICE_URI}` with your deployment's assigned URI.


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `IP_ADDR` | `(empty)` |
| `NODEKEY` | `(empty)` |

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `harbor.status.im/wakuorg/nwaku:v0.31.0` |
| CPU | 1.0 |
| Memory | 2Gi |
| Storage | 1Gi |
| Exposed Ports | 60000 |
