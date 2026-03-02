# chia-bladebit

A fast RAM-only, k32-only, Chia plotter.
416 GiB of RAM are required to run it, plus a few more megabytes for stack space and small allocations.

## Use Cases

- CPU mining
- Cryptocurrency mining
- Compute resource monetization

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:8080/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}:8080/` in your browser.


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `VERSION` | `1.6.0` |
| `CONTRACT` | `(empty)` |
| `FARMERKEY` | `(empty)` |
| `PLOTTER` | `bladebit` |
| `BUCKETS` | `256` |
| `PLOT_SIZE` | `32` |
| `FINAL_LOCATION` | `local` |
| `CPU_UNITS` | `32` |
| `MEMORY_UNITS` | `420Gi` |
| `STORAGE_UNITS` | `1200Gi` |

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `cryptoandcoffee/akash-chia:316` |
| CPU | 32.0 |
| Memory | 420Gi |
| Storage | 1200Gi |
| Exposed Ports | 8080 |
