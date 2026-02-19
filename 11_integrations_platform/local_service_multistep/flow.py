"""
Local Service Multi-Step

Demonstrates a two-step pipeline where both steps share the same MathService.
compute_sum iterates through a list calling MathService.add, then compute_product
scales the result, and the workflow collects both outputs into a summary dict.

Patterns shown:
  1. A single service shared across multiple steps via services['MathService']
  2. Sequential step pipeline: compute_sum feeds its result into compute_product
  3. Workflow returning a structured dict combining both step outputs
"""
from blazing import Blazing, BaseService


async def main():
    app = Blazing()

    @app.service
    class MathService(BaseService):
        async def add(self, x: float, y: float) -> float:
            return x + y

        async def multiply(self, x: float, y: float) -> float:
            return x * y

    @app.step
    async def compute_sum(values: list, services=None):
        total = 0.0
        for v in values:
            total = await services['MathService'].add(total, float(v))
        return total

    @app.step
    async def compute_product(base: float, factor: float, services=None):
        return await services['MathService'].multiply(base, factor)

    @app.workflow
    async def aggregate_and_scale(values: list, scale_factor: float, services=None):
        total = await compute_sum(values, services=services)
        scaled = await compute_product(total, scale_factor, services=services)
        return {'sum': total, 'scaled': scaled}

    await app.publish()
    result = await app.aggregate_and_scale(values=[1, 2, 3, 4, 5], scale_factor=10.0).wait_result()
    print(result)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
