"""
Worker Types with Services

Demonstrates all four executor worker types in a single workflow where each step calls
a trusted MathOpsService — showing that trusted sync (BLOCKING), trusted async
(NON_BLOCKING), and both sandboxed async variants all access services the same way.

Patterns shown:
  1. @app.service with BaseService — define trusted service callable from all workers
  2. @app.step (sync) — BLOCKING trusted step: pure computation, no service needed
  3. @app.step (async) — NON_BLOCKING trusted step: await services['Name'].method()
  4. @app.step(sandboxed=True) — sandboxed async steps: same services['Name'] pattern
  5. services['MathOpsService'] dict access — identical API across all worker types
"""

import asyncio
import os

from blazing import Blazing
from blazing.base import BaseService


app = Blazing(
    api_url=os.getenv("BLAZING_API_URL", "http://localhost:8000"),
    api_token=os.getenv("BLAZING_API_TOKEN", "demo-token-placeholder"),
)


# ── MathOpsService (trusted service — accessible from all worker types) ───────

@app.service
class MathOpsService(BaseService):
    """Service with basic math operations, callable from all four worker types."""

    def __init__(self, connectors):
        self._connectors = connectors

    async def add(self, x: int, y: int) -> int:
        """Add two numbers."""
        return x + y

    async def multiply(self, x: int, y: int) -> int:
        """Multiply two numbers."""
        return x * y

    async def subtract(self, x: int, y: int) -> int:
        """Subtract two numbers."""
        return x - y

    async def divide(self, x: int, y: int) -> int:
        """Integer divide two numbers."""
        return x // y


# ── Step 1: BLOCKING — trusted sync step (pure computation) ───────────────────
# Worker type: BLOCKING (synchronous trusted executor)
# Note: BLOCKING steps cannot await services — pure computation only.

@app.step
def trusted_sync_compute_step(value: int, services=None) -> int:
    """Trusted sync step (BLOCKING worker). Adds 10 — pure computation."""
    # BLOCKING: trusted sync — no service call possible here (sync context)
    return value + 10


# ── Step 2: NON_BLOCKING — trusted async step ─────────────────────────────────
# Worker type: NON_BLOCKING (asynchronous trusted executor)

@app.step
async def trusted_async_compute_step(value: int, services=None) -> int:
    """Trusted async step (NON_BLOCKING worker). Multiplies by 2 via MathOpsService."""
    # NON_BLOCKING: trusted async — can await services
    result = await services["MathOpsService"].multiply(value, 2)
    return result


# ── Step 3: NON_BLOCKING_SANDBOXED — sandboxed async step (first) ─────────────
# Worker type: NON_BLOCKING_SANDBOXED (Pyodide async executor)

@app.step(sandboxed=True)
async def sandboxed_sync_compute_step(value: int, services=None) -> int:
    """Sandboxed async step (NON_BLOCKING_SANDBOXED worker). Subtracts 5 via MathOpsService."""
    # NON_BLOCKING_SANDBOXED: sandboxed async — same services['Name'] pattern
    result = await services["MathOpsService"].subtract(value, 5)
    return result


# ── Step 4: NON_BLOCKING_SANDBOXED — sandboxed async step (second) ────────────
# Worker type: NON_BLOCKING_SANDBOXED (Pyodide async executor)

@app.step(sandboxed=True)
async def sandboxed_async_compute_step(value: int, services=None) -> int:
    """Sandboxed async step (NON_BLOCKING_SANDBOXED worker). Divides by 3 via MathOpsService."""
    # NON_BLOCKING_SANDBOXED: sandboxed async — same services['Name'] pattern
    result = await services["MathOpsService"].divide(value, 3)
    return result


# ── Workflow — orchestrates all four worker types ─────────────────────────────

@app.workflow
async def four_worker_orchestration_workflow(start_value: int, services=None):
    """
    Workflow orchestrating all four worker types through MathOpsService:

    start_value=5
      -> BLOCKING (trusted sync):              5 + 10 = 15   (after_blocking)
      -> NON_BLOCKING (trusted async):        15 *  2 = 30   (after_non_blocking)
      -> NON_BLOCKING_SANDBOXED (sandboxed):  30 -  5 = 25   (after_blocking_sandboxed)
      -> NON_BLOCKING_SANDBOXED (sandboxed):  25 /  3 =  8   (after_non_blocking_sandboxed)
    """
    # Step 1: BLOCKING worker — pure computation
    step1 = await trusted_sync_compute_step(start_value)

    # Step 2: NON_BLOCKING worker — trusted async + MathOpsService
    step2 = await trusted_async_compute_step(step1, services=services)

    # Step 3: NON_BLOCKING_SANDBOXED worker — sandboxed async + MathOpsService
    step3 = await sandboxed_sync_compute_step(step2, services=services)

    # Step 4: NON_BLOCKING_SANDBOXED worker — sandboxed async + MathOpsService
    step4 = await sandboxed_async_compute_step(step3, services=services)

    return {
        "start": start_value,
        "after_blocking": step1,
        "after_non_blocking": step2,
        "after_blocking_sandboxed": step3,
        "after_non_blocking_sandboxed": step4,
        "final": step4,
    }


# ── Main ──────────────────────────────────────────────────────────────────────

async def main():
    print("=== Worker Types with Services Demo ===")
    print()
    print("Four worker types, one service (MathOpsService):")
    print("  BLOCKING            (trusted sync):   value + 10")
    print("  NON_BLOCKING        (trusted async):  value *  2  via service")
    print("  NON_BLOCKING_SANDBOXED (sandboxed):   value -  5  via service")
    print("  NON_BLOCKING_SANDBOXED (sandboxed):   value /  3  via service")
    print()

    await app.publish()

    # Expected: ((5 + 10) * 2 - 5) / 3 = (15 * 2 - 5) / 3 = (30 - 5) / 3 = 25 / 3 = 8
    unit = await app.four_worker_orchestration_workflow(start_value=5)
    result = await unit.result()

    print(f"  start                    : {result['start']}")
    print(f"  after_blocking           : {result['after_blocking']}   (5 + 10)")
    print(f"  after_non_blocking       : {result['after_non_blocking']}   (15 * 2)")
    print(f"  after_blocking_sandboxed : {result['after_blocking_sandboxed']}   (30 - 5)")
    print(f"  after_non_blocking_sandboxed: {result['after_non_blocking_sandboxed']}    (25 / 3)")
    print(f"  final                    : {result['final']}")
    print()
    print("All four worker types accessed MathOpsService with identical services['Name'] API.")


if __name__ == "__main__":
    asyncio.run(main())
