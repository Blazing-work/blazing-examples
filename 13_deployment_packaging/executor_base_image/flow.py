"""
Executor Base Image

Demonstrates extending the standard Blazing executor base image with additional system
packages, Python packages, and environment variables.  The built image is attached to a
workflow so all its steps run with curl, numpy, and APP_ENV pre-configured.

Patterns shown:
  1. Image.executor() to start from the official Blazing executor base image
  2. .apt_install('curl').pip_install('numpy') to layer system and Python packages
  3. .env(APP_ENV='prod') to bake environment variables into the image spec
"""
from blazing import Blazing
from blazing.image import Image


async def main():
    app = Blazing()

    image = (
        Image.executor()
        .apt_install('curl')
        .pip_install('numpy')
        .env(APP_ENV='prod')
    )

    @app.step
    async def compute(values: list, services=None):
        import numpy as np
        return float(np.mean(values))

    @app.workflow(image=image)
    async def mean(values: list, services=None):
        return await compute(values, services=services)

    await app.publish()
    result = await app.mean(values=[1, 2, 3, 4]).wait_result()
    print({'mean': result})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
