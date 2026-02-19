"""
Isolated Execution

Demonstrates the simplest sandboxed step: a compute step decorated with sandboxed=True
runs in a WebAssembly sandbox with complete isolation from the host system.
This is the minimal pattern for isolated execution in Blazing.

Patterns shown:
  1. @app.step(sandboxed=True) to run code in a WebAssembly sandbox
  2. A workflow that delegates entirely to a sandboxed step
  3. Retrieving the sandboxed step result via wait_result()
"""
from blazing import Blazing


async def main():
    app = Blazing()

    @app.step(sandboxed=True)
    async def secure_compute(x: int, services=None):
        return x * 2

    @app.workflow
    async def isolated_workflow(x: int, services=None):
        return await secure_compute(x, services=services)

    await app.publish()
    result = await app.isolated_workflow(x=21).wait_result()
    print({'result': result})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
