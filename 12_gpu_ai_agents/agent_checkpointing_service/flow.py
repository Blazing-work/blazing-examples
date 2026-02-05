from blazing import Blazing, BaseService


async def main():
    app = Blazing()

    @app.service
    class CheckpointService(BaseService):
        def __init__(self, connector_instances):
            self._store = {}

        async def save(self, key: str, value):
            self._store[key] = value
            return True

        async def load(self, key: str):
            return self._store.get(key)

    @app.step
    async def step_one(value: int, services=None):
        await services['CheckpointService'].save('step_one', value)
        return value + 1

    @app.step
    async def step_two(value: int, services=None):
        await services['CheckpointService'].save('step_two', value)
        return value * 2

    @app.workflow
    async def agent_like_pipeline(value: int, services=None):
        a = await step_one(value, services=services)
        b = await step_two(a, services=services)
        return b

    await app.publish()
    result = await app.agent_like_pipeline(value=5).wait_result()
    print({'result': result})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
