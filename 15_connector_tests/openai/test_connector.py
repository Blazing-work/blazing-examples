"""
OpenAI connector tests — chat completion and budget enforcement.

Most tests run against OpenRouter free-tier models (zero cost) to validate
connector behaviour. One smoke test calls real OpenAI to confirm it works.

Run (free, via OpenRouter):
    OPENROUTER_API_KEY=... pytest 15_connector_tests/openai/ -v

Run (with real OpenAI smoke test):
    OPENROUTER_API_KEY=... OPENAI_API_KEY=... pytest 15_connector_tests/openai/ -v
"""

import os
import pytest
import pytest_asyncio

from blazing.base import BudgetExceededError
from blazing_service.connectors import SecretsConnector, OpenAIConnector

_FREE_MODEL = "meta-llama/llama-3.3-70b-instruct:free"

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.skipif(not os.getenv("OPENROUTER_API_KEY"), reason="OPENROUTER_API_KEY not set"),
]


@pytest_asyncio.fixture
async def openrouter_connector():
    secrets = SecretsConnector(name="secrets", values={"OPENAI_API_KEY": os.environ["OPENROUTER_API_KEY"]})
    await secrets.connect()
    connector = OpenAIConnector(
        name="openrouter",
        secrets=secrets,
        max_tokens_budget=5000,
        base_url="https://openrouter.ai/api/v1",
    )
    await connector.connect()
    yield connector
    await connector.disconnect()
    await secrets.disconnect()


@pytest.mark.timeout(60)
async def test_chat_completion(openrouter_connector):
    """Chat returns a non-empty content string with token tracking."""
    response = await openrouter_connector.chat(
        messages=[{"role": "user", "content": "Reply with exactly: pong"}],
        model=_FREE_MODEL,
        max_tokens=10,
    )
    assert isinstance(response["content"], str)
    assert len(response["content"]) > 0
    assert openrouter_connector.tokens_used > 0


@pytest.mark.timeout(60)
async def test_system_message(openrouter_connector):
    """System + user messages processed correctly."""
    response = await openrouter_connector.chat(
        messages=[
            {"role": "system", "content": "You are a calculator. Reply with only the number."},
            {"role": "user", "content": "What is 2+2?"},
        ],
        model=_FREE_MODEL,
        max_tokens=20,
    )
    assert "4" in response["content"]


@pytest.mark.timeout(30)
async def test_budget_exceeded_error():
    """BudgetExceededError raised before the API call when budget is exhausted."""
    secrets = SecretsConnector(name="secrets", values={"OPENAI_API_KEY": os.environ["OPENROUTER_API_KEY"]})
    await secrets.connect()
    connector = OpenAIConnector(
        name="budget-test", secrets=secrets, max_tokens_budget=10,
        base_url="https://openrouter.ai/api/v1",
    )
    try:
        await connector.connect()
        with pytest.raises(BudgetExceededError):
            await connector.chat(
                messages=[{"role": "user", "content": "This will exceed the 10-token budget"}],
                model=_FREE_MODEL,
                max_tokens=50,
            )
    finally:
        await connector.disconnect()
        await secrets.disconnect()


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OPENAI_API_KEY not set")
@pytest.mark.timeout(60)
async def test_real_openai_smoke(openai_connector):
    """One call to real OpenAI to confirm it works as a backend. Cost: ~$0.0002."""
    response = await openai_connector.chat(
        messages=[{"role": "user", "content": "Reply with exactly: pong"}],
        model="gpt-4o-mini",
        max_tokens=10,
    )
    assert len(response["content"]) > 0
