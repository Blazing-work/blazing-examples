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
