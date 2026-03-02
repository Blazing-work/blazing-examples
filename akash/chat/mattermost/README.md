# mattermost

[Mattermost](https://mattermost.com/) is an open source collaboration platform built for developers (Slack alternative).

## Use Cases

- Real-time messaging
- Team communication
- Chat platform hosting

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:8065/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}:8065/` in your browser or send HTTP requests to this address.

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `mattermost/mattermost-preview` |
| CPU | 1.0 |
| Memory | 512Mi |
| Storage | 1Gi |
| Exposed Ports | 8065 |
