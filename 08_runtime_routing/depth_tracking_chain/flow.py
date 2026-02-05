from blazing import Blazing


async def main():
    app = Blazing()

    @app.step
    async def step_a(x: int, services=None):
        return x + 1

    @app.step
    async def step_b(x: int, services=None):
        return await step_a(x, services=services) + 1

    @app.step
    async def step_c(x: int, services=None):
        return await step_b(x, services=services) + 1

    @app.workflow
    async def chain_workflow(x: int, services=None):
        return await step_c(x, services=services) + 1

    await app.publish()
    result = await app.chain_workflow(x=1).wait_result()
    print({'result': result})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
