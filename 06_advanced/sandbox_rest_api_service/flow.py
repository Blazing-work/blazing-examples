"""
Sandbox: Service Bridge with REST APIs

Demonstrates letting user code call external REST APIs through a service bridge while
keeping API keys hidden inside the platform.  The sandbox receives a service proxy;
actual HTTP calls and credentials are managed by the platform.

Patterns shown:
  1. Service bridge pattern: user code calls a service, platform holds API keys
  2. run_sandboxed() passing services to the sandbox execution context
  3. Signing and validating user-submitted code before execution
  4. Minimal workflow wrapper delegating to run_sandboxed()
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
