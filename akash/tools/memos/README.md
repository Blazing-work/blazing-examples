# memos

An open-source, self-hosted note-taking service. Your thoughts, your data, your control — no tracking, no ads, no subscription fees.
Open URI from Leases tab to access web interface.
[Github](https://github.com/usememos/memos) | [Docs](https://usememos.com/docs)

## Use Cases

- Self-hosted utility
- Productivity tool
- System administration

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Connect to the service on port `5230`
3. Refer to the official documentation for usage instructions

## Accessing the Service

Connect to the service on port `5230`. Replace `{SERVICE_URI}` with your deployment's assigned URI.

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `neosmemo/memos:0.25.2` |
| CPU | 0.1 |
| Memory | 512Mi |
| Storage | 1Gi |
| Exposed Ports | 5230 |
