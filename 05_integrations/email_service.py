"""
# Email Service

Send emails via SMTP service integration.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Intermediate
- **Time**: 20 min
- **Tags**: service, email, smtp, notifications

## Description

Send emails via SMTP service integration.

## What you'll learn

- How to configure SMTP connectors
- Sending emails from workflows
- Template-based email composition
"""

from blazing.base import BaseService

from blazing import Blazing

async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    @app.service
    class EmailService(BaseService):
        def __init__(self, connectors):
            self._smtp = connectors.get('smtp')
        async def send(self, to: str, subject: str, body: str):
            """Send email."""
            message = {
                "to": to,
                "subject": subject,
                "body": body
            }
            await self._smtp.send(message)
            return {"sent": True, "to": to}
    @app.workflow
    async def send_welcome_email(user_email: str, user_name: str, services=None):
        """Send welcome email to new user."""
        subject = f"Welcome, {user_name}!"
        body = f"Hello {user_name},\n\nWelcome to our platform!"
        result = await services['EmailService'].send(user_email, subject, body)
        return result
    await app.publish()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
