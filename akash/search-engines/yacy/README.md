# yacy

YaCy Search Engine Software
===========================
YaCy is a distributed Web Search Engine, based on a peer-to-peer network.

## Use Cases

- Full-text search
- Privacy-respecting search
- Data indexing

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:8090/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}:8090/` in your browser or send HTTP requests to this address.

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `yacy/yacy_search_server:latest` |
| CPU | 0.1 |
| Memory | 256Mi |
| Exposed Ports | 8090 |
