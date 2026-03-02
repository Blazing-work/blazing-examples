# swagger-ui

This template deploys the official [Swagger UI](https://github.com/swagger-api/swagger-ui) container and lets you point it to your own OpenAPI specification.
3. Open the URI in the "Leases" tab to access the Swagger UI. On some providers, you will need to manually open the URI in the "Leases" tab with HTTPS instead of HTTP.

## Use Cases

- Self-hosted utility
- Productivity tool
- System administration

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:8080/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}:8080/` in your browser.


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `SWAGGER_JSON_URL` | `https://petstore3.swagger.io/api/v3/openapi.json` |

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `swaggerapi/swagger-ui:v5.29.3` |
| CPU | 1.0 |
| Memory | 1Gi |
| Storage | 1Gi |
| Exposed Ports | 8080 |
