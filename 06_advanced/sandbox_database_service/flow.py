"""
Sandbox: Service Bridge with Database

Demonstrates running user code that processes data through a database service bridge,
keeping database credentials safe inside the platform while exposing only a scoped
service interface to the sandbox.

Patterns shown:
  1. run_sandboxed() forwarding the services dict to user code
  2. User code accessing a database service without seeing credentials
  3. Signing key creation and code signing via create_signing_key()
  4. Workflow wrapper that delegates entirely to run_sandboxed()
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
