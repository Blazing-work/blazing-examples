"""
Worker Type Isolation

Demonstrates the routing difference between trusted NON-BLOCKING and sandboxed
NON-BLOCKING steps.  Both types are called in the same workflow and results returned
side by side to show that isolation affects routing but not the async execution model.

Patterns shown:
  1. @app.step(step_type='NON-BLOCKING') for trusted async execution
  2. @app.step(sandboxed=True, step_type='NON-BLOCKING') for sandboxed async execution
  3. Comparing trusted vs sandboxed output in a single workflow dict
"""
from blazing import Blazing


async def main():
    app = Blazing()

    @app.step(step_type='NON-BLOCKING')
    async def trusted_async(x: int, services=None):
        return x + 1

    @app.step(sandboxed=True, step_type='NON-BLOCKING')
    async def sandboxed_async(x: int, services=None):
        return x + 2

    @app.workflow
    async def compare(x: int, services=None):
        a = await trusted_async(x, services=services)
        b = await sandboxed_async(x, services=services)
        return {'trusted': a, 'sandboxed': b}

    await app.publish()
    result = await app.compare(x=5).wait_result()
    print(result)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
