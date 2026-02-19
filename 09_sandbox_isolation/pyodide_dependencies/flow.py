"""
Pyodide Dependencies

Demonstrates installing Python packages into the Pyodide WebAssembly sandbox
via the sandbox_dependencies parameter.  numpy is imported inside a sandboxed step
to compute mean and sum on a list of values.

Patterns shown:
  1. Blazing(sandbox_dependencies=['numpy']) to pre-install packages in the sandbox
  2. import numpy as np inside a @app.step(sandboxed=True) body
  3. Returning computed statistics dict from the sandboxed step
"""
from blazing import Blazing


async def main():
    app = Blazing(sandbox_dependencies=['numpy'])

    @app.step(sandboxed=True)
    async def sandboxed_stats(values: list, services=None):
        import numpy as np

        arr = np.array(values)
        return {'mean': float(arr.mean()), 'sum': float(arr.sum())}

    @app.workflow
    async def run_stats(values: list, services=None):
        return await sandboxed_stats(values, services=services)

    await app.publish()
    result = await app.run_stats(values=[1, 2, 3, 4]).wait_result()
    print(result)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
