# quai-gpu-miner

GPU Mining Implementation of Quai's ProgPow Algorithm.
- STRATUM_IP: The IP address to your running stratum instance, or pool.
- STRATUM_PORT: The port that stratum is listening on for that IP. Ensure that it is open/forwarded.

## Use Cases

- GPU mining
- Cryptocurrency mining
- High-performance hashing

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:80/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}/` in your browser.


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `STRATUM_IP` | `(empty)` |
| `STRATUM_PORT` | `(empty)` |
| `PLATFORM` | `U` |

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `quainetwork/quai-gpu-miner-run:v0.5.0` |
| CPU | 0.1 |
| Memory | 512Mi |
| Storage | 1Gi |
| Exposed Ports | 80 |
