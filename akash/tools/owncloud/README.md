# owncloud

ownCloud is a self-hosted file sync and share server. It provides access to your data through a web interface, sync clients or WebDAV while providing a platform to view, sync and share across devices easily—all under your control. ownCloud’s open architecture is extensible via a simple but powerful API for applications and plugins and it works with any storage.

## Use Cases

- Self-hosted utility
- Productivity tool
- System administration

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:80/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}/` in your browser.

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `owncloud` |
| CPU | 1.0 |
| Memory | 1Gi |
| Storage | 2Gi |
| Exposed Ports | 80 |
