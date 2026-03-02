# vidulum

By default, the image is setting the moniker to the container name, use `vidulumd start --help` in order to see what you can customize should you need to.
If you plan to register a validator, make sure you back-up the `priv_validator_key.json` & `node_key.json` in the `/root/.vidulum/config` directory.
- https://github.com/vidulum/mainnet

## Use Cases

- Blockchain node operation
- Validator services
- Decentralized network participation

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Connect to the service on port `26656`
3. Refer to the official documentation for usage instructions

## Accessing the Service

Connect to the service on port `26656`. Replace `{SERVICE_URI}` with your deployment's assigned URI.

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `andrey01/vidulumd:1.0.0` |
| CPU | 2.0 |
| Memory | 4Gi |
| Storage | 200Gi |
| Exposed Ports | 26656 |
