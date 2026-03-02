# wikijs

From [the project site](https://github.com/Requarks/wiki):
A modern, lightweight and powerful wiki app built on NodeJS.

## Use Cases

- Content publishing
- Blog hosting
- Content management

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:3000/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}:3000/` in your browser.


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `DB_TYPE` | `sqlite` |
| `DB_FILEPATH` | `/wiki/app.db` |

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `requarks/wiki:2` |
| CPU | 1.0 |
| Memory | 512Mi |
| Storage | 1Gi |
| Exposed Ports | 3000 |
