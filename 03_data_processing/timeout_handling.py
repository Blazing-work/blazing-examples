"""
# Timeout Handling

Prevent workflows from hanging with asyncio.wait_for timeouts.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Intermediate
- **Time**: 15 min
- **Tags**: timeout, error-handling, asyncio

## Description

Prevent workflows from hanging with asyncio.wait_for timeouts.

## What you'll learn

- How to implement timeouts with asyncio.wait_for
- Handling TimeoutError exceptions
- When to use timeouts in workflows
"""

import asyncio

from blazing import Blazing

async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    @app.step
    async def slow_operation(data: str, services=None):
        """Operation that might take too long."""
        await asyncio.sleep(10)  # Simulate slow operation
        return f"processed: {data}"
    @app.workflow
    async def with_timeout(data: str, timeout_seconds: int = 5, services=None):
        """Workflow with timeout."""
        try:
            result = await asyncio.wait_for(
                slow_operation(data, services=services),
                timeout=timeout_seconds
            )
            return {"success": True, "result": result}
        except asyncio.TimeoutError:
            return {"success": False, "error": "Operation timed out"}
    await app.publish()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
