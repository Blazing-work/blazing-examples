"""
Model Cache in Image

Demonstrates caching model weights inside the executor image using .run_commands() and
.env() to set the MODEL_PATH.  The step reads the weights file at startup using the
path from the environment variable, simulating model loading from an image-baked cache.

Patterns shown:
  1. run_commands to create /models and write placeholder weights during image build
  2. .env(MODEL_PATH='/models/model.txt') to make the path available at runtime
  3. os.getenv('MODEL_PATH') inside the step to locate and load the cached model file
"""
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
