# Docsearch Crawler

BFS web crawler that indexes documentation sites to Algolia.

## Patterns

- Breadth-first search with `collections.deque`
- robots.txt compliance via `urllib.robotparser`
- URL normalization (trailing slash, fragments, sorted query params)
- SHA256 objectID generation for idempotent indexing
- Batch indexing (1000 docs/batch) for Algolia rate limits

## Setup

```bash
pip install httpx trafilatura beautifulsoup4 lxml
```

Requires `algolia` connector configured with API key and app ID.

## Usage

```bash
POST /crawl
{"start_url": "https://docs.example.com", "index_name": "my_docs", "max_depth": 3, "max_pages": 100}
```

Add the target domain to `@app.service(egress=[...])` before crawling.
