"""
Local Multiple Services

Demonstrates registering two services (MathService and StringService) in a single
Blazing app and consuming both from one step.  The step multiplies a value via
MathService and uppercases a label via StringService, returning both results together.

Patterns shown:
  1. Multiple @app.service classes registered on the same Blazing instance
  2. Accessing two services in one step via services['MathService'] and services['StringService']
  3. Combining results from multiple services in a single step return value
"""
from blazing import Blazing, BaseService


async def main():
    app = Blazing()

    @app.service
    class MathService(BaseService):
        async def multiply(self, x: float, y: float) -> float:
            return x * y

    @app.service
    class StringService(BaseService):
        async def uppercase(self, value: str) -> str:
            return value.upper()

    @app.step
    async def process(value: float, label: str, services=None):
        doubled = await services['MathService'].multiply(value, 2.0)
        upper = await services['StringService'].uppercase(label)
        return {'doubled': doubled, 'label': upper}

    @app.workflow
    async def pipeline(value: float, label: str, services=None):
        return await process(value, label, services=services)

    await app.publish()
    result = await app.pipeline(value=21.0, label='answer').wait_result()
    print(result)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
