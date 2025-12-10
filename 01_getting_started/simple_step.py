"""
# Simple Step

The simplest possible Blazing Flow example - a single processing step.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Beginner
- **Time**: 5 min
- **Tags**: step, basics, quickstart

## Description

The simplest possible Blazing Flow example - a single processing step.

## What you'll learn

- How to create a Blazing app
- How to define a step with @app.step
- How to publish steps to the execution engine
"""

from blazing import Blazing

async def main():
    app = Blazing(api_url="http://localhost:8000", api_token="your-token")
    @app.step
    async def hello(name: str, services=None):
        """Basic step that returns a greeting."""
        return f"Hello, {name}!"
    await app.publish()
    result = await app.hello("World")
    print(result)  # "Hello, World!"


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
