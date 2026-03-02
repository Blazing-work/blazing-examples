# kanboard

From the official Docker image:
https://docs.kanboard.org/en/latest/admin_guide/docker.html
Kanboard is a free and open source Kanban project management software.

## Use Cases

- Task tracking
- Team collaboration
- Project planning

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:80/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}/` in your browser.

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `kanboard/kanboard:v1.2.8` |
| CPU | 1.0 |
| Memory | 512Mi |
| Storage | 512Mi |
| Exposed Ports | 80 |
