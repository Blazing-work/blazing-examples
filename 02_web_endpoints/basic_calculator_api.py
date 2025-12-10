"""
# Basic Calculator API

The simplest possible endpoint: expose a workflow as a public HTTP API.

## Metadata
- **Product**: Blazing Flow Endpoints
- **Difficulty**: Beginner
- **Time**: 10 min
- **Tags**: endpoint, api, rest, basic

## Description

The simplest possible endpoint: expose a workflow as a public HTTP API.

## What you'll learn

- How to expose workflows as HTTP endpoints
- How to use @app.endpoint decorator
- How to create and run a FastAPI app with Blazing
"""

import uvicorn

from blazing import Blazing
from blazing.web import create_asgi_app


async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    @app.endpoint(path="/calculate")
    @app.workflow
    async def calculate(x: int, y: int, services=None):
        """Add two numbers together."""
        return x + y

    # Publish and create FastAPI app
    await app.publish()
    fastapi_app = await create_asgi_app(app)
    # Run server
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
