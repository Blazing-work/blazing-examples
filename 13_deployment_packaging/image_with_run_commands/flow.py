"""
Image with Run Commands

Demonstrates using .run_commands() to execute shell commands during image build,
creating directories and writing seed files into the image layer.  The step then reads
the seed file at runtime to confirm the build-time commands executed correctly.

Patterns shown:
  1. Image.executor().run_commands('mkdir -p /app/data', 'echo ... > file') for build-time setup
  2. @app.workflow(image=image) to deploy into the image with pre-created filesystem artifacts
  3. Reading a build-time file (open('/app/data/seed.txt')) at step runtime
"""
from blazing import Blazing
from blazing.image import Image


async def main():
    app = Blazing()

    image = (
        Image.executor()
        .run_commands('mkdir -p /app/data', 'echo "seed" > /app/data/seed.txt')
    )

    @app.step
    async def read_seed(services=None):
        with open('/app/data/seed.txt', 'r') as f:
            return f.read().strip()

    @app.workflow(image=image)
    async def get_seed(services=None):
        return await read_seed(services=services)

    await app.publish()
    result = await app.get_seed().wait_result()
    print({'seed': result})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
