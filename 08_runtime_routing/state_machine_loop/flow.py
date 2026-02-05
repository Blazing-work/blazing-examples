from blazing import Blazing


async def main():
    app = Blazing()

    @app.step
    async def next_state(value: int, services=None):
        return value + 1

    @app.workflow
    async def run_state_machine(limit: int, services=None):
        state = 0
        while state < limit:
            state = await next_state(state, services=services)
        return state

    await app.publish()
    result = await app.run_state_machine(limit=5).wait_result()
    print({'final_state': result})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
