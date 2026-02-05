from blazing import Blazing
from blazing.image import Image


async def main():
    app = Blazing()

    image = (
        Image.executor()
        .run_commands('mkdir -p /models', 'echo "weights" > /models/model.txt')
        .env(MODEL_PATH='/models/model.txt')
    )

    @app.step
    async def load_model(services=None):
        import os
        path = os.getenv('MODEL_PATH')
        with open(path, 'r') as f:
            return f.read().strip()

    @app.workflow(image=image)
    async def read_model(services=None):
        return await load_model(services=services)

    await app.publish()
    result = await app.read_model().wait_result()
    print({'model': result})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
