"""
Sandboxed Step Execution

Demonstrates the core sandboxed execution pattern: run_sandboxed() executes
user-provided code in a WebAssembly sandbox with complete isolation from the host
infrastructure (no network, filesystem, or service access beyond what is explicitly bridged).

Patterns shown:
  1. run_sandboxed() with signing_key for HMAC code authentication
  2. Specifying func_name to select the entry point in sandbox.py
  3. Passing input_data and services into the sandboxed context
  4. A minimal Blazing workflow wrapper for sandboxed step execution
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
