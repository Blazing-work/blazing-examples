# Connector Tests

Live integration tests for every Blazing connector. Each subdirectory
tests one connector against a real external service using credentials
supplied via environment variables.

## Connectors

| Directory | Service | Required env vars |
|-----------|---------|-------------------|
| `algolia/` | Algolia search | `ALGOLIA_APP_ID`, `ALGOLIA_API_KEY` |
| `discord/` | Discord webhook | `DISCORD_WEBHOOK_URL` |
| `google_sheets/` | Google Sheets API | `GOOGLE_SHEETS_CREDENTIALS`, `GOOGLE_SHEETS_TEST_SPREADSHEET_ID` |
| `slack/` | Slack Web API | `SLACK_BOT_TOKEN` (+ optional `SLACK_SIGNING_SECRET`) |
| `mongodb/` | MongoDB (Atlas or local) | `MONGODB_TEST_URI` |
| `s3/` | S3 / MinIO | `S3_ENDPOINT_URL` (+ optional `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`) |
| `openai/` | OpenAI / OpenRouter | `OPENROUTER_API_KEY` (+ optional `OPENAI_API_KEY`) |
| `anthropic/` | Anthropic Claude | `ANTHROPIC_API_KEY` |

## Run a single connector

```bash
# Algolia
ALGOLIA_APP_ID=... ALGOLIA_API_KEY=... pytest 15_connector_tests/algolia/ -v

# Slack
SLACK_BOT_TOKEN=xoxb-... pytest 15_connector_tests/slack/ -v

# All connectors you have credentials for (others auto-skip)
pytest 15_connector_tests/ -v
```

## How tests skip gracefully

Every test file has a module-level `pytest.mark.skipif` that checks for
the required environment variable. Tests that don't find credentials are
skipped, not failed — so running the full suite only executes tests for
the services you have configured.

## MinIO (S3 local)

```bash
docker run -p 9000:9000 -e MINIO_ROOT_USER=admin -e MINIO_ROOT_PASSWORD=admin \
  minio/minio server /data

S3_ENDPOINT_URL=http://localhost:9000 pytest 15_connector_tests/s3/ -v
```

## MongoDB (local Docker)

```bash
docker run -p 27017:27017 mongo:7

MONGODB_TEST_URI=mongodb://localhost:27017 pytest 15_connector_tests/mongodb/ -v
```

## Cost estimates

| Connector | Cost per run |
|-----------|-------------|
| Algolia | Free (within M0 quota) |
| Discord | Free |
| Google Sheets | Free |
| Slack | Free |
| MongoDB Atlas M0 | Free |
| S3 / MinIO | Free (local) / negligible (AWS) |
| OpenAI (via OpenRouter free model) | $0 |
| OpenAI smoke test (gpt-4o-mini) | ~$0.0002 |
| Anthropic (claude-3-haiku) | ~$0.01 |
