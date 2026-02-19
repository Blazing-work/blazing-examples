"""
Step with Math

Demonstrates basic arithmetic operations in a distributed step.
An addition step is registered and called through a workflow, illustrating
the minimal pattern for numeric computation in Blazing.

Patterns shown:
  1. A step that accepts typed numeric arguments (int)
  2. A workflow that delegates directly to a single step
  3. Passing keyword arguments when calling a workflow
  4. SyncBlazing variant without async/await
"""
from blazing import Blazing


async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    # Define a step (the unit of work)
    @app.step
    async def add(a: int, b: int, services=None):
        """Add two numbers."""
        return a + b

    # Define a workflow that orchestrates steps
    @app.workflow
    async def compute_sum(a: int, b: int, services=None):
        """Workflow: compute sum of two numbers."""
        return await add(a, b, services=services)

    # IMPORTANT: Publish to register steps/workflows with the execution engine
    await app.publish()

    # Execute workflow and wait for result
    result = await app.compute_sum(a=10, b=20).wait_result()
    print(result)  # 30


# ==============================================================================
# SYNC API - For learning and prototyping only
# NOTE: For production, we strongly recommend using the async Blazing class above
# ==============================================================================


def main_sync():
    """Synchronous version using SyncBlazing - for learning/prototyping only."""
    from blazing import SyncBlazing

    app = SyncBlazing()

    @app.step
    async def add(a: int, b: int, services=None):
        """Add two numbers."""
        return a + b

    @app.workflow
    async def compute_sum(a: int, b: int, services=None):
        """Workflow: compute sum of two numbers."""
        return await add(a, b, services=services)

    # No await, no asyncio.run()!
    app.publish()
    print(app.compute_sum(a=10, b=20))  # 30


if __name__ == "__main__":
    # Choose your preferred style:
    import asyncio

    asyncio.run(main())  # Async version

    # Or use SyncBlazing (cleanest sync experience):
    # main_sync()
