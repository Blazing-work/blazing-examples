"""
# Email Queue Processor

Process email queues in batches with Redis.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Intermediate
- **Time**: 25 min
- **Tags**: queue, email, batch, redis

## Description

Process email queues in batches with Redis.

## What you'll learn

- Queue-based email processing
- Batch processing patterns
- Redis as a message queue
"""

from blazing.base import BaseService
        import json
        import json
    import asyncio

from blazing import Blazing

async def main():
    app = Blazing(api_url="http://localhost:8000", api_token="your-token")

    @app.service
    class EmailQueueService(BaseService):
        def __init__(self, connectors):
            self._queue = connectors.get('redis')
            self._smtp = connectors.get('smtp')
        async def enqueue(self, to: str, subject: str, body: str):
            """Add email to queue."""
            email = json.dumps({"to": to, "subject": subject, "body": body})
            await self._queue.lpush('email_queue', email)
        async def dequeue(self) -> dict:
            """Get next email from queue."""
            email = await self._queue.rpop('email_queue')
            return json.loads(email) if email else None
    @app.step
    async def send_queued_email(services=None):
        """Process one email from queue."""
        email = await services['EmailQueueService'].dequeue()
        if email:
            await services['EmailQueueService']._smtp.send(email)
            return {"sent": True, "to": email['to']}
        return {"sent": False, "reason": "queue_empty"}
    @app.workflow
    async def process_email_queue(batch_size: int = 10, services=None):
        """Process email queue in batches."""
        results = await asyncio.gather(*[
            send_queued_email(services=services)
            for _ in range(batch_size)
        ])
        sent_count = sum(1 for r in results if r['sent'])
        return {"processed": batch_size, "sent": sent_count}
    await app.publish()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
