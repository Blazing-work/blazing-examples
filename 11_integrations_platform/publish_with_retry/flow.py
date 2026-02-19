"""
Publish with Retry

Demonstrates wrapping app.publish() in an exponential-backoff retry loop to handle
transient 429 (rate limit) HTTP errors from the control plane.  Up to max_retries
attempts are made with doubling delays before the error is re-raised.

Patterns shown:
  1. publish_with_retry(app, max_retries, base_delay) helper function for resilient publish
  2. Catching httpx.HTTPStatusError and checking status_code == 429 for rate limiting
  3. asyncio.sleep(base_delay * 2**attempt) for exponential backoff between retries
"""
import asyncio
from blazing import Blazing


async def publish_with_retry(app, max_retries=3, base_delay=1.0):
    import httpx
    for attempt in range(max_retries):
        try:
            await app.publish()
            return
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429 and attempt < max_retries - 1:
                await asyncio.sleep(base_delay * (2 ** attempt))
            else:
                raise


async def main():
    app = Blazing()

    @app.step
    async def add_one(x: int, services=None):
        return x + 1

    @app.workflow
    async def run_add_one(x: int, services=None):
        return await add_one(x, services=services)

    await publish_with_retry(app)
    result = await app.run_add_one(x=10).wait_result()
    print({'result': result})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
