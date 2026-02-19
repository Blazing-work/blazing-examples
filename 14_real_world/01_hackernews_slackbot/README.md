# Hacker News Slackbot

Automated digest bot that fetches top HN stories and posts them to Slack on a schedule.

## Patterns

- `@app.workflow(schedule=Period(hours=1))` — runs automatically every hour
- `@app.endpoint.post("/digest")` — manual trigger endpoint
- `asyncio.Semaphore(10)` — concurrent API rate limiting
- `connector_instances=None` — optional Slack connector injection

## Setup

```bash
pip install httpx
```

Configure a `slack` connector with a webhook URL, or the bot will log without posting.

## Run

```bash
python flow.py  # fetches and prints stories (no Slack required)
```
