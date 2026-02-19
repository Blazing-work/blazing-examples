"""
Shared pytest fixtures for Blazing connector E2E tests.

Each fixture creates a real connector instance using credentials from
environment variables, yields it for the test, then disconnects cleanly.

Required environment variables per connector:
  Algolia:       ALGOLIA_APP_ID, ALGOLIA_API_KEY
  Discord:       DISCORD_WEBHOOK_URL
  Google Sheets: GOOGLE_SHEETS_CREDENTIALS, GOOGLE_SHEETS_TEST_SPREADSHEET_ID
  Slack:         SLACK_BOT_TOKEN  (+ optional SLACK_SIGNING_SECRET)
  MongoDB:       MONGODB_TEST_URI
  S3/MinIO:      S3_ENDPOINT_URL  (+ optional AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY)
  OpenAI:        OPENAI_API_KEY
  Anthropic:     ANTHROPIC_API_KEY

Run a single connector's tests:
  pytest 15_connector_tests/algolia/ -v
"""

import os
import uuid

import pytest
import pytest_asyncio

from blazing_service.connectors import (
    AlgoliaConnector,
    DiscordConnector,
    GoogleSheetsConnector,
    MongoDBConnector,
    OpenAIConnector,
    PrometheusConnector,
    S3Connector,
    SecretsConnector,
    SlackConnector,
)
from blazing.local.llm import AnthropicConnector


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

@pytest.fixture
def unique_id():
    """Short unique string for test resource names (parallel-safe)."""
    return uuid.uuid4().hex[:12]


@pytest.fixture(scope="session")
def s3_test_bucket():
    return os.getenv("S3_TEST_BUCKET", "test-bucket")


# ---------------------------------------------------------------------------
# Connector fixtures
# ---------------------------------------------------------------------------

@pytest_asyncio.fixture
async def algolia_connector():
    secrets = SecretsConnector(name="secrets", values={
        "ALGOLIA_APP_ID": os.environ["ALGOLIA_APP_ID"],
        "ALGOLIA_API_KEY": os.environ["ALGOLIA_API_KEY"],
    })
    await secrets.connect()
    connector = AlgoliaConnector(name="algolia", secrets=secrets)
    await connector.connect()
    yield connector
    await connector.disconnect()
    await secrets.disconnect()


@pytest_asyncio.fixture
async def discord_connector():
    secrets = SecretsConnector(name="secrets", values={
        "DISCORD_WEBHOOK_URL": os.environ["DISCORD_WEBHOOK_URL"],
    })
    await secrets.connect()
    connector = DiscordConnector(name="discord", secrets=secrets)
    await connector.connect()
    yield connector
    await connector.disconnect()
    await secrets.disconnect()


@pytest_asyncio.fixture
async def google_sheets_connector():
    secrets = SecretsConnector(name="secrets", values={
        "GOOGLE_SERVICE_ACCOUNT_JSON": os.environ["GOOGLE_SHEETS_CREDENTIALS"],
    })
    await secrets.connect()
    connector = GoogleSheetsConnector(name="gsheets", secrets=secrets)
    await connector.connect()
    yield connector
    await connector.disconnect()
    await secrets.disconnect()


@pytest_asyncio.fixture
async def slack_connector():
    secret_values = {"SLACK_BOT_TOKEN": os.environ["SLACK_BOT_TOKEN"]}
    if "SLACK_SIGNING_SECRET" in os.environ:
        secret_values["SLACK_SIGNING_SECRET"] = os.environ["SLACK_SIGNING_SECRET"]
    secrets = SecretsConnector(name="secrets", values=secret_values)
    await secrets.connect()
    connector = SlackConnector(name="slack", secrets=secrets)
    await connector.connect()
    yield connector
    await connector.disconnect()
    await secrets.disconnect()


@pytest_asyncio.fixture
async def mongodb_connector():
    secrets = SecretsConnector(name="secrets", values={
        "MONGODB_URI": os.environ["MONGODB_TEST_URI"],
    })
    await secrets.connect()
    connector = MongoDBConnector(name="mongodb", secrets=secrets, database="blazing_e2e_test")
    await connector.connect()
    yield connector
    await connector.disconnect()
    await secrets.disconnect()


@pytest_asyncio.fixture
async def s3_connector():
    secrets = SecretsConnector(name="secrets", values={
        "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID", "admin"),
        "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY", "admin"),
    })
    connector = S3Connector(
        name="s3",
        secrets=secrets,
        endpoint_url=os.getenv("S3_ENDPOINT_URL"),
    )
    await connector.connect()
    yield connector
    await connector.disconnect()


@pytest_asyncio.fixture
async def openai_connector():
    secrets = SecretsConnector(name="secrets", values={
        "OPENAI_API_KEY": os.environ["OPENAI_API_KEY"],
    })
    await secrets.connect()
    connector = OpenAIConnector(name="openai", secrets=secrets, max_tokens_budget=5000)
    await connector.connect()
    yield connector
    await connector.disconnect()
    await secrets.disconnect()


@pytest_asyncio.fixture
async def anthropic_connector():
    connector = AnthropicConnector(
        api_key=os.environ["ANTHROPIC_API_KEY"],
        model="claude-3-haiku-20240307",
        max_retries=2,
    )
    await connector.connect()
    yield connector
    await connector.disconnect()


@pytest_asyncio.fixture
async def prometheus_connector():
    connector = PrometheusConnector(name="prometheus")
    await connector.connect()
    yield connector
    await connector.disconnect()
