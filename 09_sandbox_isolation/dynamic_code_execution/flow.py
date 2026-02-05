from blazing import Blazing


async def main():
    app = Blazing()

    @app.step(sandboxed=True)
    async def eval_expression(expression: str, services=None):
        allowed = {'__builtins__': {}}
        return eval(expression, allowed, {})

    @app.workflow
    async def run_expression(expression: str, services=None):
        return await eval_expression(expression, services=services)

    await app.publish()
    result = await app.run_expression(expression='(2 + 3) * 4').wait_result()
    print({'result': result})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
