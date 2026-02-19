"""
Decorators and Context

Demonstrates using the Blazing app as an async context manager alongside @app.service,
@app.step, and @app.workflow decorators.  The async with app: block ensures resources
are cleaned up after the workflow completes.

Patterns shown:
  1. @app.service decorator for a simple helper service
  2. Using services["MathService"] inside a step
  3. async with app: context manager for automatic resource cleanup
  4. Publishing and running a workflow inside the context block
"""
from blazing import Blazing, BaseService


async def main():
    app = Blazing()

    @app.service
    class MathService(BaseService):
        async def add(self, x: int, y: int) -> int:
            return x + y

    @app.step
    async def double(x: int, services=None):
        return x * 2

    @app.workflow
    async def calculate(x: int, y: int, services=None):
        total = await services['MathService'].add(x, y)
        return await double(total, services=services)

    async with app:
        await app.publish()
        result = await app.calculate(x=3, y=4).wait_result()

    print({'result': result})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
