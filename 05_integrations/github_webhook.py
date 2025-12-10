"""
# GitHub Webhook Handler

Process GitHub webhooks with signature validation and event handling.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Advanced
- **Time**: 30 min
- **Tags**: webhook, github, security, events

## Description

Process GitHub webhooks with signature validation and event handling.

## What you'll learn

- How to validate webhook signatures
- Processing GitHub pull request events
- Secure webhook handling patterns
"""

    import hmac
    import hashlib

from blazing import Blazing

async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    @app.step
    async def validate_github_signature(payload: dict, signature: str, services=None):
        """Validate GitHub webhook signature."""
        secret = await services['ConfigService'].get('github_webhook_secret')
        expected = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(f"sha256={expected}", signature):
            raise ValueError("Invalid signature")
        return payload

    @app.step
    async def process_pull_request(pr_data: dict, services=None):
        """Process pull request event."""
        if pr_data['action'] == 'opened':
            # Notify team
            await services['SlackService'].notify(
                f"New PR: {pr_data['title']} by {pr_data['user']}"
            )
        return {"processed": True, "action": pr_data['action']}

    @app.workflow
    async def handle_github_webhook(payload: dict, signature: str, services=None):
        """Handle GitHub webhook."""
        validated = await validate_github_signature(payload, signature, services=services)
        if validated['event_type'] == 'pull_request':
            result = await process_pull_request(validated['data'], services=services)
        return result

    await app.publish()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
