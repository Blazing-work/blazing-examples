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
    app = Blazing()  # Uses Blazing SaaS by default

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

    # ASYNC: Three equivalent ways to execute a workflow:

    # 1. One-liner with wait_result() - SIMPLEST! ⭐
    result = await app.process_number(5).wait_result()

    # 2. Using RemoteRun handle (more explicit)
    # run = await app.process_number(5)
    # result = await run.result()

    # 3. Using run() method (by name)
    # run = await app.run("process_number", 5)
    # result = await run.wait_result()

    print(result)  # 20 ((5 * 2) + 10)


# ==============================================================================
# SYNC API - For users who don't want async/await
# ==============================================================================


# Option 1: Use SyncBlazing class (cleanest sync experience)
def main_sync_blazing():
    """Fully synchronous version using SyncBlazing - no async/await at all!"""
    from blazing import SyncBlazing

    app = SyncBlazing()  # Uses Blazing SaaS by default

    @app.step
    async def double(x: int, services=None):
        return x * 2

    @app.step
    async def add_ten(x: int, services=None):
        return x + 10

    @app.workflow
    async def process_number(x: int, services=None):
        doubled = await double(x, services=services)
        result = await add_ten(doubled, services=services)
        return result

    # Everything is sync - no await, no asyncio.run()!
    app.publish()
    result = app.process_number(5)  # Returns result directly!
    # Or: result = app.run("process_number", 5)

    print(result)  # 20


# Option 2: Use sync helper methods on async Blazing
def main_sync():
    """Synchronous version using helper methods - compatible with existing code."""
    app = Blazing()  # Uses Blazing SaaS by default

    @app.step
    async def double(x: int, services=None):
        return x * 2

    @app.step
    async def add_ten(x: int, services=None):
        return x + 10

    @app.workflow
    async def process_number(x: int, services=None):
        doubled = await double(x, services=services)
        result = await add_ten(doubled, services=services)
        return result

    # Sync publish and run - no async/await!
    app.publish_sync()
    result = app.process_number(5).wait_result_sync()
    # Or: result = app.run_sync("process_number", 5)

    print(result)  # 20


if __name__ == "__main__":
    # Choose your preferred style:
    import asyncio

    asyncio.run(main())  # Async version (recommended for async codebases)

    # Or use SyncBlazing (cleanest sync experience):
    # main_sync_blazing()

    # Or use sync helpers on async Blazing:
    # main_sync()
