"""
Executor Routing Mixed

Demonstrates mixing trusted and sandboxed NON-BLOCKING steps in a single workflow.
Both a trusted step and a sandboxed step are called sequentially; the workflow
collects both results to show how routing differs between the two.

Patterns shown:
  1. @app.step(step_type='NON-BLOCKING') for trusted async execution
  2. @app.step(sandboxed=True, step_type='NON-BLOCKING') for isolated async execution
  3. Calling both step types from one workflow and returning results together
"""
from blazing import Blazing


async def main():
    app = Blazing()

    @app.step(step_type='NON-BLOCKING')
    async def trusted_step(x: int, services=None):
        return x + 1

    @app.step(sandboxed=True, step_type='NON-BLOCKING')
    async def sandboxed_step(x: int, services=None):
        return x + 2

    @app.workflow
    async def mixed_workflow(x: int, services=None):
        return {
            'trusted': await trusted_step(x, services=services),
            'sandboxed': await sandboxed_step(x, services=services),
        }

    await app.publish()
    result = await app.mixed_workflow(x=10).wait_result()
    print(result)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
