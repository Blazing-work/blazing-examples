"""
Service Composition Pipeline

Demonstrates composing two services (MathService and StringService) in a single step
to build a pipeline that multiplies a value and then labels the result.  Both services
are called sequentially within one step to produce a formatted string output.

Patterns shown:
  1. Two @app.service classes with different domain operations (math and string formatting)
  2. Composing multiple service calls inside a single @app.step
  3. Chaining MathService.multiply output into StringService.label for a formatted result
"""
from blazing import Blazing, BaseService


async def main():
    app = Blazing()

    @app.service
    class MathService(BaseService):
        async def multiply(self, x: int, y: int) -> int:
            return x * y

    @app.service
    class StringService(BaseService):
        async def label(self, value: int) -> str:
            return f"value={value}"

    @app.step
    async def compute(x: int, services=None):
        product = await services['MathService'].multiply(x, 5)
        return await services['StringService'].label(product)

    @app.workflow
    async def pipeline(x: int, services=None):
        return await compute(x, services=services)

    await app.publish()
    result = await app.pipeline(x=7).wait_result()
    print({'result': result})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
