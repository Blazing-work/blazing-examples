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
