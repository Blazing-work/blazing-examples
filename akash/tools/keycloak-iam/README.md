# keycloak-iam

From [the official Quay image page](https://quay.io/repository/keycloak/keycloak):
Keycloak is an open source software product to allow single sign-on with Identity and Access Management aimed at modern applications and services.
Please update this manifest according to your needs.

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
| `KEYCLOAK_ADMIN` | `admin` |

### Secrets

The following values are configured as secrets and should be set securely:

- `KEYCLOAK_ADMIN_PASSWORD`

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `quay.io/keycloak/keycloak:20.0.0` |
| CPU | 1.0 |
| Memory | 1Gi |
| Storage | 512Mi |
| Exposed Ports | 8080 |
