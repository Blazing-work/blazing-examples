import os
from blazing import Blazing


async def main():
    api_url = os.getenv('BLAZING_API_URL', 'http://localhost:8000')
    api_token = os.getenv('BLAZING_API_TOKEN', 'test-token')
    app = Blazing(api_url=api_url, api_token=api_token)

    @app.step
    async def echo(message: str, services=None):
        return message

    @app.workflow
    async def ping(message: str, services=None):
        return await echo(message, services=services)

    await app.publish()
    result = await app.ping(message='hello').wait_result()
    print({'result': result})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
