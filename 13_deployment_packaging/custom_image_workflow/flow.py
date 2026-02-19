"""
Custom Image Workflow

Demonstrates attaching a custom container image to a workflow using the Image builder API.
A Debian Slim image is configured with numpy pre-installed, then the workflow decorator
receives the image so all steps in that workflow run in the specified container.

Patterns shown:
  1. Image.debian_slim(python_version='3.11').pip_install('numpy') to build an image spec
  2. @app.workflow(image=image) to bind the custom image to a specific workflow
  3. numpy imported inside the step body, available because the image pre-installs it
"""
from blazing import Blazing
from blazing.image import Image


async def main():
    app = Blazing()

    image = Image.debian_slim(python_version='3.11').pip_install('numpy')

    @app.step
    async def mean(values: list, services=None):
        import numpy as np
        return float(np.mean(values))

    @app.workflow(image=image)
    async def compute_mean(values: list, services=None):
        return await mean(values, services=services)

    await app.publish()
    result = await app.compute_mean(values=[1, 2, 3, 4]).wait_result()
    print({'mean': result})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
