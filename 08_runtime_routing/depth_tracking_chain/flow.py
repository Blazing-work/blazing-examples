"""
Depth Tracking Chain

Demonstrates a deep call chain where steps call other steps, creating multiple levels
of depth.  step_c calls step_b, which calls step_a, creating a four-level depth from
the workflow — workflow → step_c → step_b → step_a.

Patterns shown:
  1. Steps calling other steps to create multi-level depth
  2. Each step in the chain increments the value by 1
  3. The workflow adds a final increment at the top level
"""
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
