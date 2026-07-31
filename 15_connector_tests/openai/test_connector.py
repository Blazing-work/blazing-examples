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

_FREE_MODEL = "openrouter/free"

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.skipif(not os.getenv("OPENROUTER_API_KEY"), reason="OPENROUTER_API_KEY not set"),
]


async def chat_with_fallback(connector, messages, **kwargs):
    """Call via OpenRouter free model router (zero cost)."""
    return await connector.chat(messages=messages, model=_FREE_MODEL, **kwargs)


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
    response = await chat_with_fallback(
        openrouter_connector,
        messages=[{"role": "user", "content": "Reply with exactly: pong"}],
        # 512: enough headroom for a reasoning model to finish its reasoning
        # tokens AND emit content. The openrouter/free router may resolve to a
        # reasoning model; a tiny cap truncates it mid-reasoning -> null content.
        max_tokens=512,
    )
    assert response["content"] is not None, "model returned null content"
    assert isinstance(response["content"], str)
    assert len(response["content"]) > 0
    assert openrouter_connector.tokens_used > 0


@pytest.mark.timeout(60)
async def test_system_message(openrouter_connector):
    """A system+user conversation is accepted and answered.

    ⚠️ DELIBERATELY DOES NOT ASSERT THE MODEL'S ANSWER.

    This used to send "You are a calculator" / "What is 2+2?" and assert `"4" in
    content`. `_FREE_MODEL` is `openrouter/free`, a ROUTER that resolves to whatever
    free model is available at that moment — so the assertion tested that minute's
    model, not this connector. It failed in CI with:

        AssertionError: assert '4' in 'User Safety: safe'

    i.e. the router landed on something that answered with a moderation verdict. Same
    branch, two commits, opposite results, with nothing changed that the test touches.
    (blazing#461.)

    The guarantee worth having — that a system message is transmitted with role
    "system" ahead of the user turn — IS tested, deterministically and without a
    network call, in the blazing repo:

        tests/test_llm_connector.py::TestOpenAIConnector::test_chat_with_system_message
            body = mock_connector._client.post.call_args.kwargs["json"]
            assert body["messages"][0]["role"] == "system"
            assert body["messages"][1]["role"] == "user"

    So asserting model semantics here added no coverage and one flaky check. What is
    left is the live-path contract, matching the other tests in this file:
    test_chat_completion prompts "Reply with exactly: pong" and likewise never asserts
    "pong".
    """
    response = await chat_with_fallback(
        openrouter_connector,
        messages=[
            {"role": "system", "content": "You are a calculator. Reply with only the number."},
            {"role": "user", "content": "What is 2+2?"},
        ],
        # 512: see note in test_chat_completion — reasoning models need room
        # to finish reasoning before emitting the answer.
        max_tokens=512,
    )
    assert response["content"] is not None, "model returned null content"
    assert isinstance(response["content"], str)
    assert len(response["content"]) > 0, "a system+user conversation produced no completion"
    assert openrouter_connector.tokens_used > 0, "the call was not accounted for"


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
