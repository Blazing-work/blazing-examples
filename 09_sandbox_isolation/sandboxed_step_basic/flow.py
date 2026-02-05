from blazing import Blazing


async def main():
    app = Blazing()

    @app.step(sandboxed=True)
    async def sandboxed_transform(values: list, services=None):
        return [v * 2 for v in values]

    @app.workflow
    async def run_transform(values: list, services=None):
        return await sandboxed_transform(values, services=services)

    await app.publish()
    result = await app.run_transform(values=[1, 2, 3]).wait_result()
    print(result)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
