# libretranslate

Deploy an open-source translation API using LibreTranslate .
- Translate text between multiple languages
- No external API dependencies

## Use Cases

- Self-hosted utility
- Productivity tool
- System administration

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Connect to the service on port `5000`
3. Refer to the official documentation for usage instructions

## Accessing the Service

Connect to the service on port `5000`. Replace `{SERVICE_URI}` with your deployment's assigned URI.


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `LT_FRONTEND` | `true` |

### Secrets

The following values are configured as secrets and should be set securely:

- `LT_API_KEY`

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `libretranslate/libretranslate:v1.7.3` |
| CPU | 1.0 |
| Memory | 1Gi |
| Storage | 2Gi |
| Exposed Ports | 5000 |
