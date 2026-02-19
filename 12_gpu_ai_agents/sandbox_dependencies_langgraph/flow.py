"""
Sandbox Dependencies LangGraph

Demonstrates pre-installing langchain-core into the Pyodide WebAssembly sandbox via
the sandbox_dependencies parameter.  A sandboxed step can then import LangChain
primitives to run agent logic in complete isolation from the host environment.

Patterns shown:
  1. Blazing(sandbox_dependencies=['langchain-core']) to pre-install packages in Pyodide
  2. @app.step(sandboxed=True) as the execution boundary for agent logic
  3. A workflow that invokes the sandboxed agent step and returns its result
"""
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
