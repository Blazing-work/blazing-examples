"""
Sandbox: Security Validation

Demonstrates the sandbox's security enforcement by running code samples that attempt
malicious operations and verifying they are blocked.  sandbox.py contains examples
of code that fails AST validation, bytecode validation, and WASM isolation.

Patterns shown:
  1. run_sandboxed() as the execution harness for security tests
  2. Verifying that dangerous imports and builtins are blocked by AST validation
  3. Verifying that network/filesystem access is denied in the WASM sandbox
  4. Using the same workflow wrapper for both safe and malicious code tests
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
