from blazing import Blazing


async def main():
    app = Blazing()

    @app.step(sandboxed=True)
    async def secure_compute(x: int, services=None):
        return x * 2

    @app.workflow
    async def isolated_workflow(x: int, services=None):
        return await secure_compute(x, services=services)

    await app.publish()
    result = await app.isolated_workflow(x=21).wait_result()
    print({'result': result})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
