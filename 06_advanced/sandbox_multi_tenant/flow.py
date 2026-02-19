"""
Sandbox: Multi-Tenant Data Processing

Demonstrates safely running different tenants' code in isolated WebAssembly sandboxes.
Each tenant submits code that is signed, validated, and executed in a separate sandbox
so one tenant cannot access another's data or services.

Patterns shown:
  1. Per-invocation run_sandboxed() calls for tenant isolation
  2. Passing tenant-specific input_data to each sandbox execution
  3. Signing key reuse across tenant invocations
  4. Workflow wrapper that provides the entry point for multi-tenant dispatch
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
