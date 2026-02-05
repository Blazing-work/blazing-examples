import asyncio
from blazing import Blazing


async def main():
    app = Blazing()

    @app.step(sandboxed=True)
    async def compute(x: int, services=None):
        return x * x

    @app.workflow
    async def run_many(values: list, services=None):
        tasks = [compute(v, services=services) for v in values]
        return await asyncio.gather(*tasks)

    await app.publish()
    result = await app.run_many(values=[1, 2, 3, 4, 5]).wait_result()
    print(result)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
