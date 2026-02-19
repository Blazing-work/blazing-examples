"""
Dynamic Code Security Example for Blazing

Shows how to use Blazing's dynamic code execution API to safely run
user-submitted functions with multi-layer protection.

Security layers applied by serialize_user_function / execute_signed_function:

    1. AST Validation   (client)   — reject dangerous imports before signing
    2. HMAC Signing     (client)   — cryptographically sign the serialized blob
    3. Signature Check  (executor) — verify authenticity before deserialization
    4. Bytecode Check   (executor) — inspect opcodes after deserialization
    5. Sandbox          (executor) — Pyodide isolation in production workers

No Docker or infrastructure required — all layers run in-process.
"""

import asyncio

from blazing.dynamic_code import (
    create_signing_key,
    execute_signed_function,
    serialize_user_function,
)
from blazing.security import SecurityError


# ── Setup ────────────────────────────────────────────────────────────────────

# In production, load this from a secrets manager and share the same key
# between the client platform and the executor workers.
SIGNING_KEY = create_signing_key()  # 32-byte random key


# ── Happy path: safe function through all 5 layers ───────────────────────────

async def run_safe_function():
    """Execute a user-submitted function through the full security pipeline."""

    # USER submits this function (untrusted input)
    def calculate_total(items):
        """Sum prices with 10% tax."""
        return sum(item["price"] * 1.1 for item in items)

    # PLATFORM: validate AST and sign
    serialized, signature = serialize_user_function(
        calculate_total,
        signing_key=SIGNING_KEY,
        validate=True,  # Layer 1: AST check before signing
    )
    assert len(signature) == 64  # 64-char hex HMAC-SHA256

    # EXECUTOR: verify signature, validate bytecode, execute
    items = [{"price": 10}, {"price": 20}, {"price": 30}]
    result = await execute_signed_function(
        serialized,
        signature,
        args=(items,),
        signing_key=SIGNING_KEY,
        validate_bytecode=True,
    )

    expected = 10 * 1.1 + 20 * 1.1 + 30 * 1.1  # 66.0
    assert result == expected
    print(f"calculate_total([10, 20, 30]) = {result}")


# ── Layer 1: AST validation blocks dangerous imports ─────────────────────────

async def demo_layer1_blocks_os_import():
    """Layer 1 rejects 'import os' and other dangerous module imports."""

    def read_directory(path):
        import os          # blocked by Layer 1
        return os.listdir(path)

    try:
        serialize_user_function(read_directory, signing_key=SIGNING_KEY, validate=True)
        assert False, "Should have raised SecurityError"
    except SecurityError as e:
        print(f"Layer 1 blocked 'import os': {e}")


async def demo_layer1_allows_safe_math():
    """Layer 1 permits standard math operations."""

    def process_numbers(numbers):
        import math
        return [math.sqrt(x) for x in numbers if x > 0]

    serialized, signature = serialize_user_function(
        process_numbers, signing_key=SIGNING_KEY, validate=True
    )
    result = await execute_signed_function(
        serialized, signature,
        args=([1, 4, 9, 16, 25],),
        signing_key=SIGNING_KEY,
        validate_bytecode=True,
    )
    assert result == [1.0, 2.0, 3.0, 4.0, 5.0]
    print(f"process_numbers([1,4,9,16,25]) = {result}")


# ── Layer 3: Tampered code rejected before deserialization ───────────────────

async def demo_layer3_blocks_tampering():
    """Signature check runs before deserialization — tampered blobs are rejected."""

    def safe_func(x):
        return x * 2

    serialized, signature = serialize_user_function(safe_func, SIGNING_KEY)

    # Attacker corrupts the serialized blob in transit
    tampered = serialized[:-10] + "X" * 10

    try:
        await execute_signed_function(
            tampered, signature, args=(42,), signing_key=SIGNING_KEY
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"Layer 3 blocked tampered blob: {e}")


async def demo_layer3_blocks_wrong_key():
    """A signature produced with a different key is rejected."""

    def safe_func(x):
        return x * 2

    serialized, _ = serialize_user_function(safe_func, SIGNING_KEY)

    attacker_key = create_signing_key()
    _, forged_signature = serialize_user_function(safe_func, attacker_key)

    try:
        await execute_signed_function(
            serialized, forged_signature, args=(42,), signing_key=SIGNING_KEY
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"Layer 3 blocked forged signature: {e}")


# ── Async functions and closures ──────────────────────────────────────────────

async def demo_async_function():
    """Async user functions are serialized and executed correctly."""

    async def async_sum(numbers):
        await asyncio.sleep(0)
        return sum(numbers)

    serialized, signature = serialize_user_function(async_sum, SIGNING_KEY)
    result = await execute_signed_function(
        serialized, signature, args=([1, 2, 3, 4, 5],), signing_key=SIGNING_KEY
    )
    assert result == 15
    print(f"async_sum([1..5]) = {result}")


async def demo_closure():
    """Functions that close over safe variables work correctly."""

    tax_rate = 0.15

    def apply_tax(price):
        return price * (1 + tax_rate)

    serialized, signature = serialize_user_function(apply_tax, SIGNING_KEY)
    result = await execute_signed_function(
        serialized, signature, args=(100.0,), signing_key=SIGNING_KEY
    )
    assert result == 115.0
    print(f"apply_tax(100.0) with tax_rate=0.15 = {result}")


# ── Development mode: no signing ─────────────────────────────────────────────

async def demo_dev_mode():
    """In local development, signing can be disabled (signing_key=None)."""

    def simple(x):
        return x * 2

    serialized, signature = serialize_user_function(
        simple,
        signing_key=None,  # no signing key → empty signature
        validate=True,     # AST validation still runs
    )
    assert signature == ""

    result = await execute_signed_function(
        serialized, "",
        args=(21,),
        signing_key=None,
        validate_bytecode=True,
    )
    assert result == 42
    print(f"Dev mode (unsigned): simple(21) = {result}")


# ── Main ─────────────────────────────────────────────────────────────────────

async def main():
    print("=== Dynamic Code Security: 5-Layer Model ===")
    print()

    print("Happy path — all 5 layers:")
    await run_safe_function()
    print()

    print("Layer 1 — AST validation:")
    await demo_layer1_blocks_os_import()
    await demo_layer1_allows_safe_math()
    print()

    print("Layer 3 — Signature verification:")
    await demo_layer3_blocks_tampering()
    await demo_layer3_blocks_wrong_key()
    print()

    print("Async functions and closures:")
    await demo_async_function()
    await demo_closure()
    print()

    print("Development mode (signing disabled):")
    await demo_dev_mode()
    print()

    print("All security layers verified.")


if __name__ == "__main__":
    asyncio.run(main())
