"""
Isolated Retry

Demonstrates retry logic around a sandboxed step that raises ValueError for invalid inputs.
The workflow is called in a retry loop up to 3 attempts with asyncio.sleep between
failures, showing how to handle sandbox errors gracefully.

Patterns shown:
  1. @app.step(sandboxed=True) for an isolated step that may raise ValueError
  2. Retry loop with a fixed delay (asyncio.sleep) on exception
  3. Breaking out of the retry loop on first success
"""
import asyncio
from blazing import Blazing


async def main():
    app = Blazing()

    @app.step(sandboxed=True)
    async def flaky_step(x: int, services=None):
        if x < 0:
            raise ValueError('x must be non-negative')
        return x * 2

    @app.workflow
    async def retry_workflow(x: int, services=None):
        return await flaky_step(x, services=services)

    await app.publish()

    for attempt in range(3):
        try:
            result = await app.retry_workflow(x=5).wait_result()
            print({'result': result, 'attempt': attempt + 1})
            break
        except Exception:
            await asyncio.sleep(0.2)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
