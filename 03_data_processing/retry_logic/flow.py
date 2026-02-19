"""
Retry Logic

Demonstrates implementing retry with exponential backoff inside a Blazing workflow.
An unreliable step with a 30% failure rate is retried up to max_retries times, with
each retry waiting 2^attempt seconds before the next try.

Patterns shown:
  1. An unreliable step that fails randomly to simulate transient errors
  2. Retry loop in a workflow with configurable max_retries
  3. Exponential backoff via asyncio.sleep(2**attempt)
  4. Returning attempt count alongside the result or error
"""
import asyncio
import random

from blazing import Blazing


async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    @app.step
    async def unreliable_operation(data: str, services=None):
        """Operation that might fail."""
        # Simulate occasional failure
        if random.random() < 0.3:  # 30% failure rate
            raise ValueError("Transient error")
        return f"processed: {data}"

    @app.workflow
    async def with_retry(data: str, max_retries: int = 3, services=None):
        """Workflow with retry logic."""
        for attempt in range(max_retries):
            try:
                result = await unreliable_operation(data, services=services)
                return {"success": True, "result": result, "attempts": attempt + 1}
            except ValueError as e:
                if attempt == max_retries - 1:
                    return {"success": False, "error": str(e), "attempts": attempt + 1}
                await asyncio.sleep(2**attempt)  # Exponential backoff

    await app.publish()

    # Execute the retry workflow
    print("Running workflow with retry logic (30% failure rate)...")
    result = await app.with_retry(data="test data", max_retries=3).wait_result()

    print(f"Result: {result}")
    print(f"Attempts made: {result['attempts']}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
