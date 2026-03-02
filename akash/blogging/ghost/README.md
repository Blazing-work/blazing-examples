# ghost

Ghost is a modern, open-source publishing platform built for professional content creators and publishers.

## Use Cases

- Professional blogs
- Newsletter publishing
- Membership and subscription sites
- Content marketing

## Getting Started

1. Navigate to `/ghost/` to set up your admin account
2. Choose a theme and configure your publication settings
3. Create and publish your first post

## Accessing the Service

Open the Ghost admin panel at `http://{SERVICE_URI}:2368/ghost/`


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `url` | `http://changeme.com` |
| `NODE_ENV` | `production` |
| `database__client` | `sqlite3` |
| `database__connection__filename` | `content/data/ghost.db` |

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `ghost:5.12.3` |
| CPU | 1.0 |
| Memory | 1Gi |
| Storage | 5Gi |
| Exposed Ports | 2368 |

## Documentation

For full documentation, visit: [https://ghost.org/docs/](https://ghost.org/docs/)
