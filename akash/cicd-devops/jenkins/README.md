# jenkins

Jenkins – an open source automation server which enables developers around the world to reliably build, test, and deploy their software.

## Use Cases

- Continuous integration
- Continuous deployment
- Developer tooling

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:8080/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}:8080/` in your browser.

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `jenkins/jenkins:lts` |
| CPU | 1.0 |
| Memory | 1Gi |
| Storage | 5Gi |
| Exposed Ports | 8080 |
