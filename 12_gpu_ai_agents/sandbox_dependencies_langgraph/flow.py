from blazing import Blazing


async def main():
    app = Blazing(sandbox_dependencies=['langchain-core'])

    @app.step(sandboxed=True)
    async def agent_step(prompt: str, services=None):
        # Placeholder for agent libraries installed in the sandbox
        return {'prompt': prompt, 'status': 'ready'}

    @app.workflow
    async def run_agent(prompt: str, services=None):
        return await agent_step(prompt, services=services)

    await app.publish()
    result = await app.run_agent(prompt='summarize logs').wait_result()
    print(result)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
