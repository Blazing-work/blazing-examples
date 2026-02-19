"""
Dynamic Code Execution

Demonstrates evaluating a user-provided Python expression inside a sandboxed step.
The step uses a restricted execution environment so only safe math operations
are permitted, showing a minimal dynamic code execution pattern.

Patterns shown:
  1. @app.step(sandboxed=True) to run expression evaluation in a WebAssembly sandbox
  2. Restricting builtins to an empty dict to block dangerous calls
  3. Passing an expression string as a workflow parameter and returning the result
"""
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
