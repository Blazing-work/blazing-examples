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
