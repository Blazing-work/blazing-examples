"""
Workflow Handle Wait and Cancel

Demonstrates working with a RemoteRun handle to wait for workflow completion.
The handle is obtained without await, then handle.wait() blocks until the job finishes,
and handle.wait_result() retrieves the returned value.

Patterns shown:
  1. Obtaining a RemoteRun handle from an un-awaited workflow call
  2. handle.wait() to block asynchronously until the workflow is done
  3. handle.wait_result() to retrieve the result after waiting
"""
from blazing import Blazing


async def main():
    app = Blazing()

    @app.step
    async def multiply(x: int, services=None):
        return x * 2

    @app.workflow
    async def run_multiply(value: int, services=None):
        return await multiply(value, services=services)

    await app.publish()

    handle = app.run_multiply(value=5)
    await handle.wait()
    result = await handle.wait_result()
    print({'result': result})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
