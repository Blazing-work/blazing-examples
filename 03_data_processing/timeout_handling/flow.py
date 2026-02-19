"""
Timeout Handling

Demonstrates wrapping a slow step call with asyncio.wait_for to enforce a timeout.
A step that takes 10 seconds is called with a 5-second timeout, showing how the
workflow gracefully handles TimeoutError and returns an error response.

Patterns shown:
  1. asyncio.wait_for() to impose a per-step deadline
  2. Catching asyncio.TimeoutError and returning a structured error dict
  3. Configurable timeout_seconds parameter passed at workflow invocation time
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
                slow_operation(data, services=services), timeout=timeout_seconds
            )
            return {"success": True, "result": result}
        except asyncio.TimeoutError:
            return {"success": False, "error": "Operation timed out"}

    await app.publish()

    # Execute the workflow - will timeout since slow_operation takes 10s but timeout is 5s
    print("Running workflow with 5 second timeout (operation takes 10 seconds)...")
    result = await app.with_timeout(data="test data", timeout_seconds=5).wait_result()

    print(f"Result: {result}")
    # Expected: {"success": False, "error": "Operation timed out"}


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
