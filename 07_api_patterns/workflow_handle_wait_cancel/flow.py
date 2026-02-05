from blazing import Blazing


async def main():
    app = Blazing()

    @app.step
    async def multiply(x: int, services=None):
        return x * 2

    @app.workflow
    async def run_multiply(value: int, services=None):
        return await multiply(value, services=services)

    await app.publish()

    handle = app.run_multiply(value=5)
    await handle.wait()
    result = await handle.wait_result()
    print({'result': result})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
