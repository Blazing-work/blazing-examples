"""
# Basic Workflow

Multi-step orchestration - the foundation of distributed workflows.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Beginner
- **Time**: 10 min
- **Tags**: workflow, orchestration, multi-step

## Description

Multi-step orchestration - the foundation of distributed workflows.

## What you'll learn

- How to define workflows with @app.workflow
- How to chain multiple steps together
- How workflows pass data between steps
"""



from blazing import Blazing

async def main():
    app = Blazing(api_url="http://localhost:8000", api_token="your-token")

    @app.step
    async def double(x: int, services=None):
        """Double a number."""
        return x * 2

    @app.step
    async def add_ten(x: int, services=None):
        """Add 10 to a number."""
        return x + 10

    @app.workflow
    async def process_number(x: int, services=None):
        """Workflow: double then add 10."""
        doubled = await double(x, services=services)
        result = await add_ten(doubled, services=services)
        return result

    await app.publish()
    result = await app.process_number(5)
    print(result)  # 20 ((5 * 2) + 10)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
