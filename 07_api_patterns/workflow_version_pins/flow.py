from blazing import Blazing


async def main():
    app = Blazing()

    @app.step
    async def multiply(x: int, services=None):
        return x * 3

    version_pins = {
        'MathService': '1.0.0',
    }

    @app.workflow(version_pins=version_pins)
    async def pinned_workflow(x: int, services=None):
        return await multiply(x, services=services)

    await app.publish()
    result = await app.pinned_workflow(x=7).wait_result()
    print({'result': result})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
