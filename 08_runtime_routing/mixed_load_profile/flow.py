import asyncio
from blazing import Blazing


async def main():
    app = Blazing()

    @app.step(step_type='BLOCKING')
    async def cpu_work(x: int, services=None):
        total = 0
        for i in range(x):
            total += i
        return total

    @app.step
    async def io_work(x: int, services=None):
        await asyncio.sleep(0.1)
        return x * 2

    @app.workflow
    async def mixed_profile(x: int, services=None):
        cpu, io = await asyncio.gather(
            cpu_work(x, services=services),
            io_work(x, services=services),
        )
        return {'cpu': cpu, 'io': io}

    await app.publish()
    result = await app.mixed_profile(x=1000).wait_result()
    print(result)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
