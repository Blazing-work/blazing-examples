"""
API Execution Patterns

Demonstrates the three equivalent ways to execute a Blazing workflow and retrieve its result.
All three patterns — wait_result() one-liner, handle.result(), and app.run() by name —
produce the same output.

Patterns shown:
  1. wait_result() one-liner: await app.workflow(...).wait_result()
  2. RemoteRun handle: handle = await app.workflow(...); await handle.result()
  3. run() by name: run = await app.run('name', ...); await run.result()
"""
from blazing import Blazing


async def main():
    app = Blazing()

    @app.step
    async def add(x: int, y: int, services=None):
        return x + y

    @app.step
    async def multiply(x: int, y: int, services=None):
        return x * y

    @app.workflow
    async def calculate(a: int, b: int, c: int, services=None):
        total = await add(a, b, services=services)
        return await multiply(total, c, services=services)

    await app.publish()

    # Pattern 1: wait_result() one-liner
    one_liner = await app.calculate(a=2, b=3, c=7).wait_result()

    # Pattern 2: handle.result()
    handle = await app.calculate(a=2, b=3, c=7)
    handle_result = await handle.result()

    # Pattern 3: run() by name
    run = await app.run('calculate', a=2, b=3, c=7)
    run_result = await run.result()

    print({'one_liner': one_liner, 'handle': handle_result, 'run': run_result})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
