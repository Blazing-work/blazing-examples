# presearch

1. Go to https://nodes.presearch.org to learn more about nodes and create an account.
2. Go go https://nodes.presearch.org/ to grab your registration code.
You can leverage the persistent storage for `/app/node` mount point.

## Use Cases

- Full-text search
- Privacy-respecting search
- Data indexing

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:8080/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}:8080/` in your browser.


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `REGISTRATION_CODE` | `insert your registration code here` |

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `presearch/node:1.2.32` |
| CPU | 1.0 |
| Memory | 768Mi |
| Storage | 10Gi |
| Exposed Ports | 8080 |
