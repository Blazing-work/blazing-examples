"""
Depth Statistics Metrics

Demonstrates running a workflow and retrieving raw depth statistics from the metrics API.
After publishing and executing a simple step/workflow, the full /v1/metrics/depth
response is printed to show all available depth tracking fields.

Patterns shown:
  1. Connecting to a remote Blazing API with env-var credentials
  2. Publishing a workflow and running it before querying metrics
  3. GET /v1/metrics/depth with Authorization header to retrieve depth stats

Requires: docker-compose up -d
"""
import os
import httpx
from blazing import Blazing


async def main():
    api_url = os.getenv('BLAZING_API_URL', 'http://localhost:8000')
    api_token = os.getenv('BLAZING_API_TOKEN', 'test-token')
    app = Blazing(api_url=api_url, api_token=api_token)

    @app.step
    async def step_one(x: int, services=None):
        return x + 1

    @app.workflow
    async def wf(x: int, services=None):
        return await step_one(x, services=services)

    await app.publish()
    await app.wf(x=1).wait_result()

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{api_url}/v1/metrics/depth",
            headers={'Authorization': f'Bearer {api_token}'},
        )
        print(resp.json())


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
