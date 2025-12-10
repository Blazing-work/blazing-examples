"""
# Step with Math

Basic arithmetic operations in a distributed step.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Beginner
- **Time**: 5 min
- **Tags**: step, math, basics

## Recommendation

We recommend using the **async `Blazing` class** for the best performance and production readiness.
A sync version (`SyncBlazing`) is provided at the bottom for learning purposes only.

## Description

Basic arithmetic operations in a distributed step.

## What you'll learn

- How to pass parameters to steps
- How to return values from steps
- Basic type annotations for step parameters
"""

from blazing import Blazing


async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    @app.step
    async def add(a: int, b: int, services=None):
        """Add two numbers."""
        return a + b

    await app.publish()
    result = await app.add(a=10, b=20)
    print(result)  # 30


# ==============================================================================
# SYNC API - For learning and prototyping only
# NOTE: For production, we strongly recommend using the async Blazing class above
# ==============================================================================


def main_sync():
    """Synchronous version using SyncBlazing - for learning/prototyping only."""
    from blazing import SyncBlazing

    # SyncBlazing is great for learning, but use async Blazing for production
    app = SyncBlazing()

    @app.step
    async def add(a: int, b: int, services=None):
        """Add two numbers."""
        return a + b

    # No await, no asyncio.run()!
    app.publish()
    result = app.add(a=10, b=20)
    print(result)  # 30


if __name__ == "__main__":
    # Choose your preferred style:
    import asyncio

    asyncio.run(main())  # Async version

    # Or use SyncBlazing (cleanest sync experience):
    # main_sync()
