import os
from blazing import Blazing


async def main():
    app = Blazing()

    @app.step
    async def read_secret(services=None):
        return os.getenv('MY_SECRET', 'unset')

    @app.workflow
    async def show_secret(services=None):
        return await read_secret(services=services)

    await app.publish()
    result = await app.show_secret().wait_result()
    print({'secret': result})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
