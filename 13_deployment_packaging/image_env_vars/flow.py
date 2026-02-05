from blazing import Blazing
from blazing.image import Image


async def main():
    app = Blazing()

    image = Image.executor().env(FOO='bar')

    @app.step
    async def read_env(services=None):
        import os
        return os.getenv('FOO')

    @app.workflow(image=image)
    async def get_env(services=None):
        return await read_env(services=services)

    await app.publish()
    result = await app.get_env().wait_result()
    print({'FOO': result})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
