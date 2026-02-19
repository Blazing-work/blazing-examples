"""
Image Environment Variables

Demonstrates baking an environment variable into the executor image spec using .env().
The step reads the variable with os.getenv() at runtime, confirming that image-level
environment variables are visible to code running inside the container.

Patterns shown:
  1. Image.executor().env(FOO='bar') to inject an env var into the image spec
  2. @app.workflow(image=image) to run the workflow inside the configured image
  3. os.getenv('FOO') inside a step to verify the image-level env var is accessible
"""
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
