"""
Depth Cross-Boundary

Demonstrates a step that crosses the sandbox boundary while calling a trusted service.
A sandboxed NON-BLOCKING step calls a CalculationService via the services dict,
showing that service bridges work across the sandbox/host boundary.

Patterns shown:
  1. @app.step(sandboxed=True, step_type='NON-BLOCKING') for cross-boundary execution
  2. Accessing a trusted CalculationService from within a sandboxed step
  3. Workflow calling a sandboxed step transparently
"""
from blazing import Blazing, BaseService


async def main():
    app = Blazing()

    @app.service
    class CalculationService(BaseService):
        async def multiply(self, x: int, y: int) -> int:
            return x * y

    @app.step(sandboxed=True, step_type='NON-BLOCKING')
    async def sandboxed_processor(x: int, y: int, services=None):
        result = await services['CalculationService'].multiply(x, y)
        return result + 100

    @app.workflow
    async def cross_boundary_workflow(a: int, b: int, services=None):
        return await sandboxed_processor(a, b, services=services)

    await app.publish()
    result = await app.cross_boundary_workflow(a=5, b=3).wait_result()
    print({'result': result})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
