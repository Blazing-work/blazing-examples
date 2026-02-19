"""
SyncBlazing Quickstart

Demonstrates the SyncBlazing class for fully synchronous workflow execution.
Steps and workflows are defined with async def as normal, but publish() and
workflow invocation are called without await — SyncBlazing handles the event loop.

Patterns shown:
  1. SyncBlazing() — the synchronous-first Blazing API
  2. Defining async steps and workflows on SyncBlazing
  3. app.publish() and app.workflow_name(...) without await
  4. Receiving the result directly from the workflow call (no handle, no await)
"""
from blazing import SyncBlazing


def main():
    app = SyncBlazing()

    @app.step
    async def add(x: int, y: int, services=None):
        return x + y

    @app.workflow
    async def add_two_numbers(x: int, y: int, services=None):
        return await add(x, y, services=services)

    app.publish()
    result = app.add_two_numbers(x=5, y=7)
    print({'result': result})


if __name__ == '__main__':
    main()
