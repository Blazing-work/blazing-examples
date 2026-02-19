"""
Trading Strategy Sandbox

Demonstrates a two-sided platform where the platform owner defines services (market data)
and a Blazing workflow that uses run_sandboxed(), while end users submit trading strategy
code as strings that run safely inside a five-layer security sandbox.

Patterns shown:
  1. Platform-side: run_sandboxed() workflow with MarketDataService injected as a service bridge
  2. User-side: strategy functions accessing market data without seeing credentials
  3. Five security layers: AST validation, HMAC signing, signature verification, bytecode
     validation, and Pyodide WASM isolation (all handled by run_sandboxed())
  4. create_signing_key() for per-deployment HMAC key management
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
