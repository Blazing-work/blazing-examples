"""
# Sandbox: Basic User-Provided Transform

The simplest sandbox example: let users write transformation logic while your infrastructure stays protected.

## Metadata
- **Product**: Blazing Flow Sandbox
- **Difficulty**: Intermediate
- **Time**: 15 min
- **Tags**: sandbox, wasm, security, user-code

## Description

The simplest sandbox example: let users write transformation logic while your infrastructure stays protected.

## What you'll learn

- How to run untrusted code in WASM sandbox
- Security guarantees of sandboxed execution
- Basic transformation patterns in sandbox
"""

from blazing import Blazing

async def main():
    app = Blazing(api_url="http://localhost:8000", api_token="your-token")
    # USER CODE (untrusted - runs in WASM sandbox)
    @app.step
    async def user_transform(data: list, services=None):
        """
        User-provided transformation logic.
        Runs in WASM sandbox - NO network, NO filesystem access.
        """
        # Pure Python computation (safe)
        return [x * 2 for x in data if x > 0]
    # YOUR CODE (trusted - orchestrates)
    @app.workflow
    async def process_data(data: list, services=None):
        """
        Your workflow that calls user code safely.
        """
        result = await user_transform(data, services=services)
        return {"transformed": result, "count": len(result)}
    await app.publish()
    # Execute
    run = await app.create_workflow_task("process_data", data=[1, -2, 3, -4, 5])
    result = await run.result()
    print(result)  # {"transformed": [2, 6, 10], "count": 3}


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
