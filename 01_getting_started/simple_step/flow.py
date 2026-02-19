"""
Simple Step

The simplest possible Blazing Flow example — a single step wrapped in a workflow.
Shows the minimal boilerplate: one @app.step, one @app.workflow, publish, and
wait_result().

Patterns shown:
  1. Defining a single @app.step
  2. Wrapping a step in a @app.workflow
  3. app.publish() then wait_result() for a synchronous result
  4. SyncBlazing variant with no async/await at the call site
"""
from blazing import Blazing


async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    # Define a step (the unit of work)
    @app.step
    async def hello(name: str, services=None):
        """Basic step that returns a greeting."""
        return f"Hello, {name}!"

    # Define a workflow that orchestrates steps
    @app.workflow
    async def greet(name: str, services=None):
        """Workflow: greet someone by name."""
        return await hello(name, services=services)

    # IMPORTANT: Publish to register steps/workflows with the execution engine
    await app.publish()

    # Execute workflow and wait for result
    result = await app.greet(name="World").wait_result()
    print(result)  # "Hello, World!"


# ==============================================================================
# SYNC API - For learning and prototyping only
# NOTE: For production, we strongly recommend using the async Blazing class above
# ==============================================================================


def main_sync():
    """Synchronous version using SyncBlazing - for learning/prototyping only."""
    from blazing import SyncBlazing

    app = SyncBlazing()

    @app.step
    async def hello(name: str, services=None):
        """Basic step that returns a greeting."""
        return f"Hello, {name}!"

    @app.workflow
    async def greet(name: str, services=None):
        """Workflow: greet someone by name."""
        return await hello(name, services=services)

    # No await, no asyncio.run()!
    app.publish()
    print(app.greet(name="World"))  # "Hello, World!"


if __name__ == "__main__":
    # Choose your preferred style:
    import asyncio

    asyncio.run(main())  # Async version

    # Or use SyncBlazing (cleanest sync experience):
    # main_sync()
