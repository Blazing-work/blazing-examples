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
