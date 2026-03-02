# ipfs

The InterPlanetary File System (IPFS) is a protocol and peer-to-peer network for storing and sharing data in a distributed file system. IPFS uses content-addressing to uniquely identify each file in a global namespace connecting all computing devices.
(Source: [Wikipedia](https://en.wikipedia.org/wiki/InterPlanetary_File_System))
After deploying the IPFS WebUI will be available at assigned provider ingress URL. For the WebUI to work, you will need to update the deployment and set this URL in `IPFS_EXTERNAL_ADDR` (without trailing slash).

## Use Cases

- Distributed file storage
- Content-addressed storage
- Data redundancy

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Connect to the service on port `5001`
3. Refer to the official documentation for usage instructions

## Accessing the Service

Connect to the service on port `5001`. Replace `{SERVICE_URI}` with your deployment's assigned URI.


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `IPFS_EXTERNAL_ADDR` | `(empty)` |
| `IPFS_LOGGING` | `info` |
| `BASIC_AUTH_USER` | `ipfs` |
| `BASIC_AUTH_PASS` | `secretpass` |


## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `ipfs/kubo:v0.30.0` |
| CPU | 2.0 |
| Memory | 4Gi |
| Storage | 1Gi |
| Exposed Ports | 5001 |


## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `nginx:1.27` |
| CPU | 1.0 |
| Memory | 1Gi |
| Storage | 200Mi |
| Exposed Ports | 80 |
