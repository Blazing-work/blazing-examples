"""
# Hello World

Your first Blazing Flow application in under 5 minutes.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Beginner
- **Time**: 5 min
- **Tags**: quickstart, python

## Recommendation

We recommend using the **async `Blazing` class** for the best performance and production readiness.
A sync version (`SyncBlazing`) is provided at the bottom for learning purposes only.

## Description

This is the simplest possible Blazing Flow application. It demonstrates how to:
- Create a basic Blazing app
- Define a simple step and workflow
- Publish to the execution engine
- Execute and return a response

## What you'll learn

- How to structure a Blazing Flow application
- Basic step definition with @app.step
- Workflow definition with @app.workflow
- E2E execution with publish and wait_result
"""

from blazing import Blazing


async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    # Define a step (the unit of work)
    @app.step
    async def hello(services=None):
        """A simple hello world step."""
        return {"message": "Hello, World!"}

    @app.step
    async def hello_name(name: str, services=None):
        """A personalized greeting step."""
        return {"message": f"Hello, {name}!"}

    # Define workflows that orchestrate steps
    @app.workflow
    async def greet(services=None):
        """Workflow: say hello."""
        return await hello(services=services)

    @app.workflow
    async def greet_person(name: str, services=None):
        """Workflow: personalized greeting."""
        return await hello_name(name, services=services)

    # IMPORTANT: Publish to register steps/workflows with the execution engine
    await app.publish()

    # Execute workflows and wait for results
    result1 = await app.greet().wait_result()
    result2 = await app.greet_person(name="Blazing").wait_result()

    print(result1)  # {"message": "Hello, World!"}
    print(result2)  # {"message": "Hello, Blazing!"}


# ==============================================================================
# SYNC API - For learning and prototyping only
# NOTE: For production, we strongly recommend using the async Blazing class above
# ==============================================================================


def main_sync():
    """Synchronous version using SyncBlazing - for learning/prototyping only."""
    from blazing import SyncBlazing

    app = SyncBlazing()

    @app.step
    async def hello(services=None):
        """A simple hello world step."""
        return {"message": "Hello, World!"}

    @app.step
    async def hello_name(name: str, services=None):
        """A personalized greeting step."""
        return {"message": f"Hello, {name}!"}

    @app.workflow
    async def greet(services=None):
        """Workflow: say hello."""
        return await hello(services=services)

    @app.workflow
    async def greet_person(name: str, services=None):
        """Workflow: personalized greeting."""
        return await hello_name(name, services=services)

    # No await, no asyncio.run()!
    app.publish()
    print(app.greet())  # {"message": "Hello, World!"}
    print(app.greet_person(name="Blazing"))  # {"message": "Hello, Blazing!"}


if __name__ == "__main__":
    # Choose your preferred style:
    import asyncio

    asyncio.run(main())  # Async version (recommended)

    # Or use SyncBlazing (cleanest sync experience):
    # main_sync()
