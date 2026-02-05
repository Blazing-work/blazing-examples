from blazing import Blazing


async def main():
    app = Blazing()

    @app.step
    async def child_step(x: int, services=None):
        return x + 1

    @app.workflow
    async def parent_workflow(x: int, services=None):
        return await child_step(x, services=services)

    await app.publish()
    result = await app.parent_workflow(x=5).wait_result()
    print({'result': result})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
