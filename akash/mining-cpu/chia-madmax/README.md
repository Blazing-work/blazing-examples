# chia-madmax

This is a new implementation of a chia plotter which is designed as a processing pipeline, similar to how GPUs work, only the "cores" are normal software CPU threads.  As a result this plotter is able to fully max out any storage device's bandwidth, simply by increasing the number of "cores", ie. threads.

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
| `PLOTTER` | `madmax` |
| `BUCKETS` | `256` |
| `PLOT_SIZE` | `32` |
| `PORT` | `8444` |
| `FINAL_LOCATION` | `local` |
| `CPU_UNITS` | `8` |
| `MEMORY_UNITS` | `6Gi` |
| `STORAGE_UNITS` | `815Gi` |

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `cryptoandcoffee/akash-chia:316` |
| CPU | 8.0 |
| Memory | 6Gi |
| Storage | 815Gi |
| Exposed Ports | 8080 |
