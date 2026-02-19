"""
Sandbox: Basic User-Provided Transform

The simplest sandbox integration: let users write transformation logic that runs in a
WebAssembly sandbox while the platform infrastructure stays protected.  flow.py provides
the run_sandboxed() workflow; the transform logic lives in sandbox.py.

Patterns shown:
  1. Reading sandbox source code from a companion sandbox.py file
  2. create_signing_key() for HMAC code signing
  3. run_sandboxed() with func_name pointing to the sandbox entry point
  4. Minimal workflow boilerplate for sandboxed step execution
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
