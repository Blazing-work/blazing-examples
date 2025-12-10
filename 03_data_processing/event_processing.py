"""
# Event Processing Pipeline

Validate, enrich, and store incoming events with multi-step processing.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Intermediate
- **Time**: 25 min
- **Tags**: events, pipeline, enrichment, validation

## Description

Validate, enrich, and store incoming events with multi-step processing.

## What you'll learn

- Event processing architecture
- Data enrichment patterns
- Event storage strategies
"""



from blazing import Blazing

async def main():
    app = Blazing(api_url="http://localhost:8000", api_token="your-token")

    @app.step
    async def validate_event(event: dict, services=None):
        """Validate event structure."""
        required = ['event_type', 'user_id', 'timestamp']
        if not all(k in event for k in required):
            raise ValueError("Invalid event structure")
        return event

    @app.step
    async def enrich_event(event: dict, services=None):
        """Enrich event with user data."""
        user = await services['UserDatabase'].get_user(event['user_id'])
        return {**event, 'user_name': user['name'], 'user_email': user['email']}

    @app.step
    async def store_event(event: dict, services=None):
        """Store event in analytics database."""
        await services['EventDatabase'].insert(event)
        return {"stored": True, "event_id": event.get('id')}

    @app.workflow
    async def process_event(event: dict, services=None):
        """Process incoming event."""
        validated = await validate_event(event, services=services)
        enriched = await enrich_event(validated, services=services)
        result = await store_event(enriched, services=services)
        return result

    await app.publish()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
