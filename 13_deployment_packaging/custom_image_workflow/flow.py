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
