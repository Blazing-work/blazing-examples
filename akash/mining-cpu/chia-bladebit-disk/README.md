# chia-bladebit-disk

Chia is releasing new plotting software called Bladebit Disk, utilizing the high-performance code from the in-memory plotter Bladebit, with a new architecture optimized for mainstream storage devices (solid state drives, and hard disk drives). Major new features include DRAM caching to reduce writes and improve performance and brand new architecture for disk io that improves SSD endurance and takes advantage of high bandwidth SSDs, like PCIe 4.0. The plotter has broad compatibility across device types and operating systems as well as low minimum requirements for embedded and entry-level systems.
[Announcing Bladebit 2.0 Full Blog](https://www.chia.net/2022/08/08/announcing-bladebit-2.en.html)

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
| `PLOTTER` | `bladebit-disk` |
| `BLADEBIT_VERSION` | `v2.0.0-beta1` |
| `BUCKETS` | `128` |
| `PLOT_SIZE` | `32` |
| `FINAL_LOCATION` | `local` |
| `CPU_UNITS` | `16` |
| `MEMORY_UNITS` | `124Gi` |
| `STORAGE_UNITS` | `815Gi` |
| `RAMCACHE` | `100G` |

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `cryptoandcoffee/akash-chia:316` |
| CPU | 16.0 |
| Memory | 124Gi |
| Storage | 815Gi |
| Exposed Ports | 8080 |
