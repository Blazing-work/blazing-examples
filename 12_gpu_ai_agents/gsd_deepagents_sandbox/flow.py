"""
GSD-Style Tool Registry in Pyodide Sandbox

Pass structured tool definitions as plain dicts into a Pyodide sandbox and
implement a data-driven tool registry with list and filter operations. The
GSD framework concept — structured tool management, phase-based orchestration,
dependency resolution — is represented as pure data to avoid importing the full
GSD framework into Pyodide.

Patterns shown:
  1. Blazing(sandbox_wheel_urls=[...], sandbox_dependencies=[...]) — custom wheel + deps
  2. build_wheel() + upload_wheel() — package local langblaze for sandbox
  3. execute_user_code(fn, state_dict, ...) — run async function in Pyodide sandbox
  4. create_signing_key() — generate key for trusted code submission
  5. Data-driven tool registry — tool defs passed as dicts in state, not imports
  6. Registry operations: "list" returns all tools; "filter_by_tag" returns subset
  7. Tool dependency graph — "requires" field models tool dependencies

Requires: pip install blazing langblaze
          docker-compose up -d
          langblaze source at ../../../../langblaze (for wheel build)
"""

import asyncio
import os
from pathlib import Path

import httpx
from blazing import Blazing
from blazing.dynamic_code import create_signing_key, execute_user_code
from blazing.wheel_builder import build_wheel, upload_wheel


# ── Step 1: Build and upload the langblaze wheel ──────────────────────────────

async def _build_and_upload_wheel(api_url: str, api_token: str) -> str:
    """Build the langblaze wheel and upload it to the Blazing wheel server."""
    langblaze_dir = Path(__file__).parent.parent.parent.parent / "langblaze"
    wheel_info = build_wheel(str(langblaze_dir))
    print(f"  Built wheel: {wheel_info.filename}")

    await asyncio.sleep(2)
    async with httpx.AsyncClient(timeout=60.0) as client:
        wheel_url = await upload_wheel(wheel_info, api_url, api_token, client)
    print(f"  Wheel URL: {wheel_url}")
    return wheel_url


# ── Create Blazing app with sandbox dependencies ──────────────────────────────

def make_app(api_url: str, api_token: str, wheel_url: str) -> Blazing:
    """
    Create Blazing app with langblaze wheel and deepagents sandbox dependencies.
    No services are needed for this example — the registry is pure data.
    """
    app = Blazing(
        api_url=api_url,
        api_token=api_token,
        sandbox_wheel_urls=[wheel_url],
        sandbox_dependencies=[
            "deepagents",
            "langgraph",
            "langchain-core",
            "typing_extensions",
        ],
    )
    return app


# ── User code: GSD-style tool registry (runs in Pyodide sandbox) ──────────────

async def use_gsd_registry(state: dict, services=None) -> dict:
    """
    USER CODE: Runs inside the Pyodide sandbox.

    Demonstrates the GSD data-driven tool registry pattern:
    - Tool definitions are passed as plain dicts in state (no GSD framework import)
    - The registry supports "list" and "filter_by_tag" operations
    - "requires" field in tool defs models the dependency graph

    State dict keys:
      tool_definitions — dict of tool_name -> {name, description, tags, requires}
      operation        — "list" or "filter_by_tag"
      tag              — tag to filter by (only for "filter_by_tag")
    """
    # Read tool definitions from state (passed as plain dicts)
    tool_definitions = state.get("tool_definitions", {})

    # Build registry: normalize each tool definition
    registry = {}
    for tool_name, tool_def in tool_definitions.items():
        registry[tool_name] = {
            "name": tool_def["name"],
            "description": tool_def["description"],
            "tags": tool_def.get("tags", []),
            "requires": tool_def.get("requires", []),
        }

    # Execute the requested registry operation
    operation = state.get("operation", "list")

    if operation == "list":
        return {
            "tool_count": len(registry),
            "tool_names": list(registry.keys()),
            "registry": registry,
        }
    elif operation == "filter_by_tag":
        tag = state.get("tag")
        filtered = {
            name: tool
            for name, tool in registry.items()
            if tag in tool.get("tags", [])
        }
        return {
            "filtered_count": len(filtered),
            "filtered_names": list(filtered.keys()),
            "filtered": filtered,
        }
    else:
        return {"error": f"Unknown operation: {operation}"}


# ── Main ───────────────────────────────────────────────────────────────────────

async def main():
    api_url = os.getenv("BLAZING_API_URL", "http://localhost:8000")
    api_token = os.getenv("BLAZING_API_TOKEN", "demo-token-placeholder")

    print("=== GSD-Style Tool Registry in Pyodide Sandbox ===")
    print()

    # Build and upload the langblaze wheel (required for sandbox use)
    print("[Setup] Building and uploading langblaze wheel...")
    wheel_url = await _build_and_upload_wheel(api_url, api_token)

    # Create app (no services — the registry is pure data)
    app = make_app(api_url, api_token, wheel_url)

    # Generate signing key for trusted code submission
    signing_key = create_signing_key()
    print(f"  Signing key: {signing_key[:16]}...")

    # Publish (no services to register for this example)
    await app.publish()
    print("  Published (no services — registry is data-driven)")
    print()

    # Tool definitions: 3 tools with tags and dependency graph
    tool_definitions = {
        "write_file": {
            "name": "write_file",
            "description": "Write content to a file",
            "tags": ["filesystem", "io"],
            "requires": [],
        },
        "read_file": {
            "name": "read_file",
            "description": "Read content from a file",
            "tags": ["filesystem", "io"],
            "requires": [],
        },
        "run_analysis": {
            "name": "run_analysis",
            "description": "Run data analysis on a file",
            "tags": ["analytics"],
            "requires": ["read_file"],
        },
    }

    # ── Operation 1: list all tools ────────────────────────────────────────────
    print("--- Operation 1: List all tools ---")
    result1 = await execute_user_code(
        use_gsd_registry,
        {
            "tool_definitions": tool_definitions,
            "operation": "list",
        },
        api_url=api_url,
        api_token=api_token,
        signing_key=signing_key,
    )
    print(f"  Tool count: {result1['tool_count']}")
    print(f"  Tool names: {result1['tool_names']}")
    print()

    # ── Operation 2: filter_by_tag "filesystem" ────────────────────────────────
    print('--- Operation 2: Filter by tag "filesystem" ---')
    result2 = await execute_user_code(
        use_gsd_registry,
        {
            "tool_definitions": tool_definitions,
            "operation": "filter_by_tag",
            "tag": "filesystem",
        },
        api_url=api_url,
        api_token=api_token,
        signing_key=signing_key,
    )
    print(f"  Filtered count: {result2['filtered_count']}")
    print(f"  Filtered names: {result2['filtered_names']}")
    print()

    print("=== Done ===")


if __name__ == "__main__":
    asyncio.run(main())
