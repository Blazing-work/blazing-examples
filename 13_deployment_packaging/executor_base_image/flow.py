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
