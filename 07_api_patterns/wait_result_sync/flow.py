"""
Wait Result Sync

Demonstrates using the sync helper methods on the async Blazing class.
publish_sync() and wait_result_sync() allow using the standard async Blazing app
from a synchronous context without asyncio.run().

Patterns shown:
  1. app.publish_sync() — synchronous publish from a regular def function
  2. handle.wait_result_sync() — synchronous result retrieval from a RemoteRun handle
  3. No asyncio.run() required at the call site
"""
from blazing import Blazing


def main():
    app = Blazing()

    @app.step
    async def increment(x: int, services=None):
        return x + 1

    @app.workflow
    async def inc_twice(value: int, services=None):
        value = await increment(value, services=services)
        value = await increment(value, services=services)
        return value

    app.publish_sync()
    result = app.inc_twice(value=10).wait_result_sync()
    print({'result': result})


if __name__ == '__main__':
    main()
