"""
Slack connector tests — real Slack API integration.

Validates message posting, Block Kit formatting, HMAC signature
verification, and replay-attack protection.

Run:
    SLACK_BOT_TOKEN=xoxb-... pytest 15_connector_tests/slack/ -v
    # Optional: SLACK_TEST_CHANNEL=#my-channel  SLACK_SIGNING_SECRET=...
"""

import hashlib
import hmac
import os
import time
import pytest
from async_timeout import timeout

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.skipif(not os.getenv("SLACK_BOT_TOKEN"), reason="SLACK_BOT_TOKEN not set"),
]

_CHANNEL = os.getenv("SLACK_TEST_CHANNEL", "#e2e-tests")


@pytest.mark.timeout(30)
async def test_post_simple_message(slack_connector):
    """Post a plain text message to Slack."""
    async with timeout(30):
        result = await slack_connector.post_message(text="E2E test from Blazing", channel=_CHANNEL)
        assert result.get("ok") is True
        assert "ts" in result


@pytest.mark.timeout(30)
async def test_post_block_kit(slack_connector):
    """Post a Block Kit message with sections and dividers."""
    async with timeout(30):
        blocks = [
            {"type": "section", "text": {"type": "mrkdwn", "text": "*E2E Blazing Test*\nBlock Kit"}},
            {"type": "divider"},
            {"type": "section", "text": {"type": "mrkdwn", "text": "Status: :white_check_mark: Passed"}},
        ]
        result = await slack_connector.post_blocks(text="E2E Block Kit", channel=_CHANNEL, blocks=blocks)
        assert result.get("ok") is True
        assert "ts" in result


@pytest.mark.skipif(not os.getenv("SLACK_SIGNING_SECRET"), reason="SLACK_SIGNING_SECRET not set")
@pytest.mark.timeout(10)
async def test_signature_verification_valid(slack_connector):
    """HMAC-SHA256 verification accepts a correctly signed webhook."""
    async with timeout(10):
        body = '{"type":"event_callback"}'
        ts = str(int(time.time()))
        secret = os.environ["SLACK_SIGNING_SECRET"]
        sig = "v0=" + hmac.new(secret.encode(), f"v0:{ts}:{body}".encode(), hashlib.sha256).hexdigest()
        assert slack_connector.verify_signature(body=body, timestamp=ts, signature=sig) is True


@pytest.mark.skipif(not os.getenv("SLACK_SIGNING_SECRET"), reason="SLACK_SIGNING_SECRET not set")
@pytest.mark.timeout(10)
async def test_signature_verification_invalid(slack_connector):
    """HMAC-SHA256 verification rejects a tampered signature."""
    async with timeout(10):
        assert slack_connector.verify_signature(
            body='{"type":"event_callback"}',
            timestamp=str(int(time.time())),
            signature="v0=invalid_signature",
        ) is False


@pytest.mark.skipif(not os.getenv("SLACK_SIGNING_SECRET"), reason="SLACK_SIGNING_SECRET not set")
@pytest.mark.timeout(10)
async def test_replay_attack_rejected(slack_connector):
    """HMAC verification rejects requests with timestamps older than 5 minutes."""
    async with timeout(10):
        old_ts = str(int(time.time()) - 360)
        secret = os.environ["SLACK_SIGNING_SECRET"]
        body = '{"type":"event_callback"}'
        sig = "v0=" + hmac.new(secret.encode(), f"v0:{old_ts}:{body}".encode(), hashlib.sha256).hexdigest()
        assert slack_connector.verify_signature(body=body, timestamp=old_ts, signature=sig) is False
