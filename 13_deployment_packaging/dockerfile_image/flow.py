"""
Dockerfile Image

Demonstrates building a Blazing image spec from an existing Dockerfile using
Image.from_dockerfile().  The workflow is bound to the image so that executor
workers build and run steps inside the custom Docker image.

Patterns shown:
  1. Image.from_dockerfile(path=..., context=...) to reference an existing Dockerfile
  2. @app.workflow(image=image) to deploy the workflow into the custom image environment
  3. Path('.') as the Docker build context, resolved relative to the script location
"""
from pathlib import Path
from blazing import Blazing
from blazing.image import Image


async def main():
    app = Blazing()

    # Example Dockerfile (inline for demo; usually a real file)
    dockerfile_dir = Path('.')
    image = Image.from_dockerfile(path=str(dockerfile_dir / 'Dockerfile'), context=str(dockerfile_dir))

    @app.step
    async def echo(message: str, services=None):
        return message

    @app.workflow(image=image)
    async def run(message: str, services=None):
        return await echo(message, services=services)

    await app.publish()
    result = await app.run(message='hello').wait_result()
    print({'result': result})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
