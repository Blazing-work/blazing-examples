# azure-devops-agent

This template is to deploy an azure devops agent .
An azure devops agent can be used in azure devops pipelines to build and deploy applications.
Here is the docker image used by the template:

## Use Cases

- Continuous integration
- Continuous deployment
- Developer tooling

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:3000/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}:3000/` in your browser.


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `AZP_URL` | `<Your_Azure_URL>` |
| `AZP_AGENT_NAME` | `<Agent_Name>` |

### Secrets

The following values are configured as secrets and should be set securely:

- `AZP_TOKEN`

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `odiovock/akash-azure-devops-agent:0.1.1` |
| CPU | 1.0 |
| Memory | 1Gi |
| Storage | 5Gi |
| Exposed Ports | 3000 |
