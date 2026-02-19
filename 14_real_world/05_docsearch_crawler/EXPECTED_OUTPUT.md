# Expected Output

## Running

```bash
python flow.py
```

## Requirements

This example requires external services configured:
- `ALGOLIA_APP_ID` and `ALGOLIA_API_KEY` for Algolia indexing
- Network access to crawl the target documentation site

Start infrastructure: `docker-compose up -d`

## Output

```
INFO - DocsCrawlerService - Starting BFS crawl of https://docs.example.com
INFO - DocsCrawlerService - Crawled 1/50 pages: /getting-started
INFO - DocsCrawlerService - Crawled 2/50 pages: /api-reference
...
INFO - DocsCrawlerService - Indexed batch of 10 documents to Algolia
INFO - DocsCrawlerService - Crawl complete: 50 pages indexed in 12.3s
{"pages_crawled": 50, "pages_indexed": 50, "skipped": 3}
```

## Notes

- Page count and timing depend on the target site structure and network speed
- The crawler respects `robots.txt` — some pages may be skipped
- URL normalization deduplicates pages with trailing slashes or fragments
- Algolia objectIDs are SHA256 hashes of normalized URLs — re-crawling is idempotent
