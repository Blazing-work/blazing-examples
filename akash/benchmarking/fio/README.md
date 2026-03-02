# fio

Flexible IO Tester (Fio) is a benchmarking and workload simulation tool for Linux/Unix created by Jens Axboe, who also maintains the block layer of the Linux kernel. Fio is highly tunable and widely used for storage performance benchmarking. It is also used in the official performance benchmarking tool created by Nutanix that is called X-Ray. X-Ray automates the deployment of VMs on which it runs Fio and then provides the results in a user-friendly way with graphs and reports.
There are also ways to run Fio on Windows, but generally other tools that are better suited for Windows OS, such as IOmeter or CrystalDiskMark are recommended.
More documentation : https://fio.readthedocs.io/en/latest/

## Use Cases

- Performance testing
- System benchmarking
- Network testing

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:80/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}/` in your browser.


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `TEST` | `standard` |

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `cryptoandcoffee/akash-fio:4` |
| CPU | 4.0 |
| Memory | 2Gi |
| Storage | 32Gi |
| Exposed Ports | 80 |
