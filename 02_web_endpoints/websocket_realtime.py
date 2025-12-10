"""
# WebSocket Real-Time Updates

Enable WebSocket for real-time progress updates from long-running workflows.

## Metadata
- **Product**: Blazing Flow Endpoints
- **Difficulty**: Advanced
- **Time**: 25 min
- **Tags**: endpoint, websocket, real-time, streaming

## Description

Enable WebSocket for real-time progress updates from long-running workflows.

## What you'll learn

- How to enable WebSocket on endpoints
- How to receive real-time progress updates
- WebSocket client implementation patterns
"""

import asyncio

from blazing import Blazing
from blazing.web import create_asgi_app


async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    @app.step
    async def process_batch(batch_id: int, services=None):
        """Simulate processing a batch."""
        await asyncio.sleep(2)  # Simulate work
        return {"batch_id": batch_id, "status": "completed"}

    # Enable WebSocket with enable_websocket=True
    @app.endpoint(path="/process", enable_websocket=True)
    @app.workflow
    async def process_data(num_batches: int, services=None):
        """
        Long-running workflow with progress updates.
        WebSocket endpoint: ws://localhost:8080/process/ws
        """
        results = []
        for i in range(num_batches):
            result = await process_batch(i, services=services)
            results.append(result)
        return {"processed": len(results), "results": results}

    await app.publish()
    await create_asgi_app(app)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
