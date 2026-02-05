from blazing import Blazing
from blazing.image import Image


async def main():
    app = Blazing()

    cpu_image = Image.executor().pip_install('numpy')
    io_image = Image.executor().apt_install('curl')

    @app.step
    async def compute_mean(values: list, services=None):
        import numpy as np
        return float(np.mean(values))

    @app.step
    async def fetch_example(services=None):
        import subprocess
        result = subprocess.run(['curl', '-s', 'https://example.com'], capture_output=True, text=True)
        return {'status': result.returncode}

    @app.workflow(image=cpu_image)
    async def cpu_workflow(values: list, services=None):
        return await compute_mean(values, services=services)

    @app.workflow(image=io_image)
    async def io_workflow(services=None):
        return await fetch_example(services=services)

    await app.publish()
    cpu = await app.cpu_workflow(values=[1, 2, 3]).wait_result()
    io = await app.io_workflow().wait_result()
    print({'cpu': cpu, 'io': io})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
