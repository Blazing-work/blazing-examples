# whoogle-search

Whoogle Search is a self-hosted, ad-free, privacy-respecting metasearch engine that proxies Google results.

## Use Cases

- Private web searches without tracking
- Ad-free search results
- Self-hosted search for organizations

## Getting Started

1. Navigate to the search page — no account needed
2. Configure preferences (theme, language, region) in settings
3. Optionally set it as your browser's default search engine

## Accessing the Service

Open `http://{SERVICE_URI}:5000/` and start searching.


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `WHOOGLE_USER` | `user` |
| `WHOOGLE_PASS` | `password` |

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `benbusby/whoogle-search:latest` |
| CPU | 1.0 |
| Memory | 1Gi |
| Storage | 1Gi |
| Exposed Ports | 5000 |

## Documentation

For full documentation, visit: [https://github.com/benbusby/whoogle-search](https://github.com/benbusby/whoogle-search)
