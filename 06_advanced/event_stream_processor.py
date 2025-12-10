"""
# Event Stream Processor

Process event streams from Kafka in batches with aggregation.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Expert
- **Time**: 40 min
- **Tags**: streaming, kafka, events, real-time

## Description

Process event streams from Kafka in batches with aggregation.

## What you'll learn

- Kafka consumer patterns
- Stream processing in batches
- Real-time event aggregation
"""

from blazing.base import BaseService
    from collections import Counter

from blazing import Blazing

async def main():
    app = Blazing(api_url="http://localhost:8000", api_token="your-token")

    @app.service
    class EventStreamService(BaseService):
        def __init__(self, connectors):
            self._kafka = connectors.get('kafka')
        async def consume_batch(self, topic: str, batch_size: int = 100) -> list:
            """Consume batch of events from Kafka."""
            events = []
            async for message in self._kafka.consume(topic, max_messages=batch_size):
                events.append(message.value)
            return events
        async def produce(self, topic: str, event: dict):
            """Produce event to Kafka."""
            await self._kafka.produce(topic, event)
    @app.step
    async def process_event_batch(events: list, services=None):
        """Process batch of events."""
        processed = []
        for event in events:
            # Transform event
            transformed = {
                **event,
                'processed_at': datetime.now().isoformat(),
                'enriched': True
            }
            processed.append(transformed)
        return processed
    @app.step
    async def aggregate_events(events: list, services=None):
        """Aggregate events by type."""
        event_types = Counter(e['event_type'] for e in events)
        return {
            "total_events": len(events),
            "by_type": dict(event_types)
        }
    @app.workflow
    async def stream_processing_job(topic: str, batch_size: int = 100, services=None):
        """Process event stream in batches."""
        # Consume batch
        events = await services['EventStreamService'].consume_batch(topic, batch_size)
        if not events:
            return {"processed": 0, "message": "No events"}
        # Process batch
        processed = await process_event_batch(events, services=services)
        # Aggregate
        stats = await aggregate_events(processed, services=services)
        # Store processed events
        for event in processed:
            await services['EventDatabase'].insert(event)
        return {
            "topic": topic,
            "processed": len(processed),
            "stats": stats
        }
    await app.publish()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
