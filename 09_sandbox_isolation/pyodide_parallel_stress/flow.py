"""
Pyodide Parallel Stress

Demonstrates running multiple sandboxed step instances concurrently with asyncio.gather.
Five square-compute tasks are launched in parallel inside sandboxed steps to stress-test
the Pyodide WASM runtime's ability to handle concurrent sandboxed executions.

Patterns shown:
  1. @app.step(sandboxed=True) for sandboxed compute (x*x)
  2. Building a list of sandboxed step coroutines for each value
  3. asyncio.gather to run all sandboxed steps concurrently
"""
import asyncio
from blazing import Blazing


async def main():
    app = Blazing()

    @app.step(sandboxed=True)
    async def compute(x: int, services=None):
        return x * x

    @app.workflow
    async def run_many(values: list, services=None):
        tasks = [compute(v, services=services) for v in values]
        return await asyncio.gather(*tasks)

    await app.publish()
    result = await app.run_many(values=[1, 2, 3, 4, 5]).wait_result()
    print(result)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
