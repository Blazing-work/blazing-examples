"""
# Data Processing Step

Filter and transform data in a single step.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Beginner
- **Time**: 5 min
- **Tags**: step, data, filtering

## Recommendation

We recommend using the **async `Blazing` class** for the best performance and production readiness.
A sync version (`SyncBlazing`) is provided at the bottom for learning purposes only.

## Description

Filter and transform data in a single step.

## What you'll learn

- How to work with lists in steps
- How to use list comprehensions for data filtering
- Basic data transformation patterns
"""

from blazing import Blazing


async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    @app.step
    async def filter_positive(numbers: list, services=None):
        """Filter out negative numbers."""
        return [n for n in numbers if n > 0]

    await app.publish()
    result = await app.filter_positive(numbers=[1, -2, 3, -4, 5])
    print(result)  # [1, 3, 5]


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
    async def filter_positive(numbers: list, services=None):
        """Filter out negative numbers."""
        return [n for n in numbers if n > 0]

    # No await, no asyncio.run()!
    app.publish()
    result = app.filter_positive(numbers=[1, -2, 3, -4, 5])
    print(result)  # [1, 3, 5]


if __name__ == "__main__":
    # Choose your preferred style:
    import asyncio

    asyncio.run(main())  # Async version

    # Or use SyncBlazing (cleanest sync experience):
    # main_sync()
