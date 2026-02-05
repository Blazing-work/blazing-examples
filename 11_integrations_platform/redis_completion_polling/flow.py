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
