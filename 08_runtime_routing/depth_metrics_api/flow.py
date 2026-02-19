"""
Depth Metrics API

Demonstrates querying the Blazing depth metrics endpoint after running a workflow.
After publishing and executing a workflow, the /v1/metrics/depth API is called
directly with httpx to retrieve the operations_scanned metric.

Patterns shown:
  1. Connecting to a remote Blazing instance via BLAZING_API_URL and BLAZING_API_TOKEN
  2. Running a workflow and then querying the metrics API with httpx
  3. Reading operations_scanned from the depth metrics response

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
    async def increment(x: int, services=None):
        return x + 1

    @app.workflow
    async def run_increment(x: int, services=None):
        return await increment(x, services=services)

    await app.publish()
    await app.run_increment(x=5).wait_result()

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{api_url}/v1/metrics/depth",
            headers={'Authorization': f'Bearer {api_token}'},
        )
        data = resp.json()

    print({'operations_scanned': data.get('operations_scanned')})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
