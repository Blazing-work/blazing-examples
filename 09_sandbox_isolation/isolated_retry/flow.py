import asyncio
from blazing import Blazing


async def main():
    app = Blazing()

    @app.step(sandboxed=True)
    async def flaky_step(x: int, services=None):
        if x < 0:
            raise ValueError('x must be non-negative')
        return x * 2

    @app.workflow
    async def retry_workflow(x: int, services=None):
        return await flaky_step(x, services=services)

    await app.publish()

    for attempt in range(3):
        try:
            result = await app.retry_workflow(x=5).wait_result()
            print({'result': result, 'attempt': attempt + 1})
            break
        except Exception:
            await asyncio.sleep(0.2)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
