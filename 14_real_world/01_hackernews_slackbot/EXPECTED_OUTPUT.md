# Expected Output

## Running

```bash
python flow.py
```

## Requirements

This example requires external services configured:
- `BLAZING_API_URL` and `BLAZING_API_TOKEN` for Blazing infrastructure
- `SLACK_WEBHOOK_URL` for posting to Slack
- Running Blazing infrastructure: `docker-compose up -d`

Start infrastructure: `docker-compose up -d`

## Output

```
2026-02-19 09:00:00,000 - HackerNewsBot - INFO - Fetching top 30 HN stories
2026-02-19 09:00:01,200 - HackerNewsBot - INFO - Found 12 stories with score >= 100
2026-02-19 09:00:01,500 - HackerNewsBot - INFO - Posted digest to Slack: 12 stories
```

## Notes

- The workflow runs on a `Period(hours=1)` schedule — it fires hourly when published
- Actual story count and scores depend on live Hacker News data at runtime
- Output timestamps and story counts will vary with each execution
- Requires a valid Slack webhook URL; without it the workflow will fail on the post step
