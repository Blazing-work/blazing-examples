"""
Depth Tracking Basic

Demonstrates the basic depth-tracking model: a workflow (parent) calling a step (child).
This one-level call tree establishes the baseline for understanding how Blazing tracks
workflow-to-step call depth.

Patterns shown:
  1. A single parent workflow calling a single child step
  2. One level of call depth: workflow → step
  3. Retrieving the result from a one-step workflow
"""
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
