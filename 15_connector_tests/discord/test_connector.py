"""
Discord connector tests — real webhook message delivery.

Validates message posting, rich embeds, username overrides, and
Ed25519 interaction signature verification.

Run:
    DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/... pytest 15_connector_tests/discord/ -v
"""

import os
import pytest
from async_timeout import timeout
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.skipif(not os.getenv("DISCORD_WEBHOOK_URL"), reason="DISCORD_WEBHOOK_URL not set"),
]


@pytest.mark.timeout(30)
async def test_send_simple_message(discord_connector):
    """Post a plain text message to a Discord webhook."""
    async with timeout(30):
        result = await discord_connector.send_message(content="E2E test message from Blazing")
        assert result.get("ok") is True
        assert "status_code" in result


@pytest.mark.timeout(30)
async def test_send_embed(discord_connector):
    """Post a rich embed with fields and colour to Discord."""
    async with timeout(30):
        result = await discord_connector.send_embed(
            title="E2E Test Embed",
            description="Integration test from Blazing",
            color="00FF00",
            fields=[
                {"name": "Status", "value": "Passed", "inline": True},
                {"name": "Suite", "value": "E2E", "inline": True},
            ],
        )
        assert result.get("ok") is True


@pytest.mark.timeout(30)
async def test_username_override(discord_connector):
    """Post with a custom username override."""
    async with timeout(30):
        result = await discord_connector.send_message(
            content="Custom username test", username="Blazing E2E Bot"
        )
        assert result.get("ok") is True


@pytest.mark.skipif(not os.getenv("DISCORD_PUBLIC_KEY"), reason="DISCORD_PUBLIC_KEY not set")
@pytest.mark.timeout(10)
async def test_ed25519_valid_signature(discord_connector):
    """Ed25519 signature verification accepts a valid signature."""
    async with timeout(10):
        private_key = Ed25519PrivateKey.generate()
        public_key = private_key.public_key()
        body = '{"type":1}'
        timestamp = "1234567890"
        sig = private_key.sign((timestamp + body).encode())
        original = discord_connector._public_key
        discord_connector._public_key = public_key.public_bytes_raw().hex()
        try:
            assert discord_connector.verify_interaction(body=body, signature=sig.hex(), timestamp=timestamp) is True
        finally:
            discord_connector._public_key = original


@pytest.mark.skipif(not os.getenv("DISCORD_PUBLIC_KEY"), reason="DISCORD_PUBLIC_KEY not set")
@pytest.mark.timeout(10)
async def test_ed25519_invalid_signature(discord_connector):
    """Ed25519 signature verification rejects a tampered signature."""
    async with timeout(10):
        private_key = Ed25519PrivateKey.generate()
        public_key = private_key.public_key()
        sig = private_key.sign(b"wrong data")
        original = discord_connector._public_key
        discord_connector._public_key = public_key.public_bytes_raw().hex()
        try:
            assert discord_connector.verify_interaction(body='{"type":1}', signature=sig.hex(), timestamp="1234567890") is False
        finally:
            discord_connector._public_key = original
