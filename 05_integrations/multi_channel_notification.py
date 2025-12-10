"""
# Multi-Channel Notification

Send notifications across email, SMS, and push channels simultaneously.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Intermediate
- **Time**: 25 min
- **Tags**: notifications, multi-channel, email, sms, push

## Description

Send notifications across email, SMS, and push channels simultaneously.

## What you'll learn

- Multi-channel notification patterns
- Parallel notification delivery
- Channel selection logic
"""

import asyncio

from blazing import Blazing


async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    @app.step
    async def send_email_notification(user_id: int, message: str, services=None):
        """Send email notification."""
        user = await services["UserDatabase"].get_user(user_id)
        await services["EmailService"].send(user["email"], "Notification", message)
        return {"channel": "email", "sent": True}

    @app.step
    async def send_sms_notification(user_id: int, message: str, services=None):
        """Send SMS notification."""
        user = await services["UserDatabase"].get_user(user_id)
        await services["SMSService"].send(user["phone"], message)
        return {"channel": "sms", "sent": True}

    @app.step
    async def send_push_notification(user_id: int, message: str, services=None):
        """Send push notification."""
        await services["PushService"].send(user_id, message)
        return {"channel": "push", "sent": True}

    @app.workflow
    async def notify_user(user_id: int, message: str, channels: list, services=None):
        """Send notification through multiple channels."""
        tasks = []
        if "email" in channels:
            tasks.append(send_email_notification(user_id, message, services=services))
        if "sms" in channels:
            tasks.append(send_sms_notification(user_id, message, services=services))
        if "push" in channels:
            tasks.append(send_push_notification(user_id, message, services=services))

        results = await asyncio.gather(*tasks)
        return {"user_id": user_id, "channels": results}

    await app.publish()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
