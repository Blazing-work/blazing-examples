from blazing import Blazing


async def main():
    app = Blazing(sandbox_dependencies=['numpy'])

    @app.step(sandboxed=True)
    async def sandboxed_stats(values: list, services=None):
        import numpy as np

        arr = np.array(values)
        return {'mean': float(arr.mean()), 'sum': float(arr.sum())}

    @app.workflow
    async def run_stats(values: list, services=None):
        return await sandboxed_stats(values, services=services)

    await app.publish()
    result = await app.run_stats(values=[1, 2, 3, 4]).wait_result()
    print(result)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
