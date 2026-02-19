"""
Anthropic connector tests — chat completion and streaming.

Validates real Anthropic API connectivity using claude-3-haiku-20240307
for cost efficiency (~$0.00025 per 1K input tokens, ~$0.01 per full run).

Run:
    ANTHROPIC_API_KEY=sk-ant-... pytest 15_connector_tests/anthropic/ -v
"""

import os
import pytest

from blazing.local.llm import ChatResponse, StreamChunk

_MODEL = "claude-3-haiku-20240307"

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.skipif(not os.getenv("ANTHROPIC_API_KEY"), reason="ANTHROPIC_API_KEY not set"),
]


@pytest.mark.timeout(60)
async def test_chat_completion(anthropic_connector):
    """Chat returns a non-empty ChatResponse."""
    response = await anthropic_connector.chat(
        messages=[{"role": "user", "content": "Reply with exactly: pong"}],
        max_tokens=10,
    )
    assert isinstance(response, ChatResponse)
    assert response.content


@pytest.mark.timeout(60)
async def test_system_message(anthropic_connector):
    """System + user messages handled correctly."""
    response = await anthropic_connector.chat(
        messages=[
            {"role": "system", "content": "You are a calculator. Reply with only the number."},
            {"role": "user", "content": "What is 2+2?"},
        ],
        max_tokens=20,
    )
    assert "4" in response.content


@pytest.mark.timeout(60)
async def test_multi_turn_conversation(anthropic_connector):
    """Multi-turn conversation maintains context across messages."""
    response = await anthropic_connector.chat(
        messages=[
            {"role": "user", "content": "My favourite colour is blue."},
            {"role": "assistant", "content": "Got it, blue is your favourite colour."},
            {"role": "user", "content": "What is my favourite colour?"},
        ],
        max_tokens=20,
    )
    assert "blue" in response.content.lower()


@pytest.mark.timeout(60)
async def test_streaming(anthropic_connector):
    """Streaming yields StreamChunks and assembles into full text."""
    chunks = []
    async for chunk in anthropic_connector.stream(
        messages=[{"role": "user", "content": "Count to 3, one number per word."}],
        max_tokens=30,
    ):
        assert isinstance(chunk, StreamChunk)
        chunks.append(chunk)

    assert len(chunks) > 0
    full_text = "".join(c.content for c in chunks if c.content)
    assert len(full_text) > 0


@pytest.mark.timeout(60)
async def test_token_usage(anthropic_connector):
    """Token usage is tracked after a chat call."""
    response = await anthropic_connector.chat(
        messages=[{"role": "user", "content": "Say hello."}],
        max_tokens=20,
    )
    assert response.input_tokens is not None and response.input_tokens > 0
    assert response.output_tokens is not None and response.output_tokens > 0
