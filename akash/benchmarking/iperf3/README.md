# iperf3

iPerf3 is a tool for active measurements of the maximum achievable bandwidth on IP networks. It supports tuning of various parameters related to timing, buffers and protocols (TCP, UDP, SCTP with IPv4 and IPv6). For each test it reports the bandwidth, loss, and other parameters.
iperf3 -s -p 5201
iperf3 -c 127.0.0.1 -p 5201

## Use Cases

- Performance testing
- System benchmarking
- Network testing

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Connect to the service on port `5201`
3. Refer to the official documentation for usage instructions

## Accessing the Service

Run network tests with:
```bash
iperf3 -c {SERVICE_URI} -p 5201
```

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `networkstatic/iperf3` |
| CPU | 1.0 |
| Memory | 16Mi |
| Storage | 128Mi |
| Exposed Ports | 5201 |
