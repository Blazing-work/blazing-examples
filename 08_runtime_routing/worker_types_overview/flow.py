from blazing import Blazing


async def main():
    app = Blazing()

    @app.step(step_type='BLOCKING')
    async def blocking_step(x: int, services=None):
        return x * 2

    @app.step(step_type='NON-BLOCKING')
    async def async_step(x: int, services=None):
        return x + 1

    @app.step(sandboxed=True, step_type='BLOCKING')
    async def sandboxed_blocking_step(x: int, services=None):
        return x * 3

    @app.step(sandboxed=True, step_type='NON-BLOCKING')
    async def sandboxed_async_step(x: int, services=None):
        return x + 2

    @app.workflow
    async def run_all(x: int, services=None):
        return {
            'blocking': await blocking_step(x, services=services),
            'async': await async_step(x, services=services),
            'sandboxed_blocking': await sandboxed_blocking_step(x, services=services),
            'sandboxed_async': await sandboxed_async_step(x, services=services),
        }

    await app.publish()
    result = await app.run_all(x=5).wait_result()
    print(result)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
