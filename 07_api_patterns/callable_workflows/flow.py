from blazing import Blazing


async def main():
    app = Blazing()

    @app.step
    async def increment(x: int, services=None):
        return x + 1

    @app.workflow
    async def add_three(x: int, services=None):
        x = await increment(x, services=services)
        x = await increment(x, services=services)
        x = await increment(x, services=services)
        return x

    await app.publish()

    # Callable workflow
    result = await app.add_three(x=10).wait_result()
    print({'result': result})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
