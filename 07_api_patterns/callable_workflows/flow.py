"""
Callable Workflows

Demonstrates calling a workflow by attribute on the Blazing app instance.
After publishing, workflows are accessible as callables on the app object —
app.workflow_name(...) returns a RemoteRun handle with wait_result().

Patterns shown:
  1. Registering a step that is called multiple times inside a workflow
  2. Calling a workflow via app.add_three(x=10) attribute access
  3. Chaining the same step call three times within a single workflow
"""
from blazing import Blazing


async def main():
    app = Blazing()

    @app.step
    async def increment(x: int, services=None):
        return x + 1

    @app.workflow
    async def add_three(x: int, services=None):
        x = await increment(x, services=services)
        x = await increment(x, services=services)
        x = await increment(x, services=services)
        return x

    await app.publish()

    # Callable workflow
    result = await app.add_three(x=10).wait_result()
    print({'result': result})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
