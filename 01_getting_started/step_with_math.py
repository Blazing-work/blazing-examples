"""
# Step with Math

Basic arithmetic operations in a distributed step.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Beginner
- **Time**: 5 min
- **Tags**: step, math, basics

## Description

Basic arithmetic operations in a distributed step.

## What you'll learn

- How to pass parameters to steps
- How to return values from steps
- Basic type annotations for step parameters
"""



from blazing import Blazing

async def main():
    app = Blazing(api_url="http://localhost:8000", api_token="your-token")

    @app.step
    async def add(a: int, b: int, services=None):
        """Add two numbers."""
        return a + b

    await app.publish()
    result = await app.add(10, 20)
    print(result)  # 30


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
