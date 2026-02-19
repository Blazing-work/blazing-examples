"""
Redis Completion Polling

Demonstrates connecting to a remote Blazing control plane via BLAZING_API_URL and
BLAZING_API_TOKEN environment variables.  The workflow is published and a result
awaited via wait_result(), polling the remote Redis-backed completion queue.

Patterns shown:
  1. Blazing(api_url=..., api_token=...) to configure a remote control plane connection
  2. Reading connection parameters from environment variables with os.getenv defaults
  3. wait_result() to poll for workflow completion from a remote runner
"""
import os
from blazing import Blazing


async def main():
    api_url = os.getenv('BLAZING_API_URL', 'http://localhost:8000')
    api_token = os.getenv('BLAZING_API_TOKEN', 'test-token')
    app = Blazing(api_url=api_url, api_token=api_token)

    @app.step
    async def add_one(x: int, services=None):
        return x + 1

    @app.workflow
    async def run_add_one(x: int, services=None):
        return await add_one(x, services=services)

    await app.publish()
    result = await app.run_add_one(x=10).wait_result()
    print({'result': result})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
