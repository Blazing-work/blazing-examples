# cjdns-pkt

Set unique values for network endpoint (line 4 and 21) and `CJDNS_PEERID` variable. Them you can create deployment.
Got to "Leases" tab and copy socket received from the provider. Them, on "Update" tab, paste socket to `CJDNS_IPV4` and press on "Update Deployment"
Check [dashboard](https://vinny.cjdns.fr/ptest/), after few minutes you can see actual status your node.

## Use Cases

- Network services
- VPN
- Network monitoring

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:3479/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}:3479/` in your browser or send HTTP requests to this address.


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `CJDNS_PEERID` | `PUB_Node_Name` |
| `CJDNS_PORT` | `3479` |
| `CJDNS_SETUSER` | `0` |
| `CJDNS_IPV6` | `false` |
| `CJDNS_IPV4` | `(empty)` |

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `declab/cjdns:0.1` |
| CPU | 1.0 |
| Memory | 1Gi |
| Storage | 1Gi |
| Exposed Ports | 3479 |
