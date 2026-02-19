"""
Sandbox: Async Service Calls

Demonstrates how to execute user-provided code that makes concurrent async service calls
from inside a Blazing sandbox.  The flow.py hosts the run_sandboxed() wrapper workflow;
the actual concurrent service call logic lives in sandbox.py.

Patterns shown:
  1. create_signing_key() to generate a per-deployment HMAC signing key
  2. run_sandboxed() wrapping an external sandbox.py entry point
  3. Passing input_data and services into the sandboxed execution context
  4. Returning the sandbox result from a Blazing workflow
"""
from blazing import Blazing, run_sandboxed, create_signing_key

app = Blazing()

# Read the sandbox code
with open("sandbox.py", "r") as f:
    sandbox_code = f.read()

signing_key = create_signing_key()


@app.workflow
async def run_sandbox(input_data: dict, services=None) -> dict:
    """Execute the sandbox code securely."""
    result = await run_sandboxed(
        sandbox_code,
        input_data,
        signing_key=signing_key,
        func_name="main",  # Entry point in sandbox.py
        services=services
    )
    return result


if __name__ == "__main__":
    import asyncio

    async def main():
        await app.publish()
        result = await app.run_sandbox(input_data={"test": True}).wait_result()
        print(result)

    asyncio.run(main())
