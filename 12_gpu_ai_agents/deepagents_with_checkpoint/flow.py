"""
DeepAgents with BlazeCheckpointer

Run a deepagents LangGraph-based agent loop entirely inside the Pyodide sandbox with
multi-turn state persistence via BlazeCheckpointer — a LangGraph-compatible checkpointer
that serializes state through a trusted CheckpointService. Supports resumable sessions
across independent invocations using thread_id.

Patterns shown:
  1. Blazing(sandbox_dependencies=[...], sandbox_wheel_urls=[...]) — install packages + custom wheel
  2. build_wheel() + upload_wheel() — package local langblaze for sandbox use
  3. CheckpointService with LangGraph protocol — aget/aput/alist/aput_writes
  4. BlazeCheckpointer(services) — LangGraph checkpointer backed by CheckpointService
  5. create_deep_agent() + agent.ainvoke(state, config={"configurable": {"thread_id": id}})
  6. Multi-turn resumable sessions — Invocation 1 creates session; Invocation 2 resumes

Requires: pip install blazing langblaze deepagents langgraph langchain-core
          docker-compose up -d
"""

import asyncio
import uuid
from pathlib import Path

import httpx
from blazing import Blazing
from blazing.base import BaseService
from blazing.dynamic_code import create_signing_key, execute_user_code
from blazing.wheel_builder import build_wheel, upload_wheel


# ── Module-level checkpoint storage (persists across service calls) ───────────
# Not class-level — must survive across separate CheckpointService.aget/aput calls
_checkpoint_storage: dict = {}


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
# Done in main() after the wheel is uploaded so we can pass the wheel_url.


# ── CheckpointService (trusted worker — persists LangGraph checkpoint state) ──

def make_app(api_url: str, api_token: str, wheel_url: str) -> Blazing:
    """Create Blazing app with sandbox dependencies including the langblaze wheel."""
    app = Blazing(
        api_url=api_url,
        api_token=api_token,
        sandbox_wheel_urls=[wheel_url],
        # deepagents requires langgraph, langchain-core
        sandbox_dependencies=[
            "deepagents",
            "langgraph",
            "langchain-core",
            "typing_extensions",
        ],
    )

    @app.service
    class CheckpointService(BaseService):
        """
        Checkpoint service compatible with LangGraph BaseCheckpointSaver protocol.

        Backed by module-level _checkpoint_storage dict so state persists
        across multiple execute_user_code invocations within the same process.
        """

        def __init__(self, connectors):
            self._connectors = connectors

        async def aget(self, thread_id: str):
            """Load the latest checkpoint for thread_id."""
            if thread_id not in _checkpoint_storage:
                return None
            data = _checkpoint_storage[thread_id]
            return {
                "checkpoint": data["checkpoint"],
                "metadata": data.get("metadata", {}),
                "parent_config": data.get("parent_config"),
            }

        async def aput(self, thread_id: str, checkpoint: dict, metadata: dict = None):
            """Save a checkpoint for thread_id. Returns a checkpoint_id."""
            checkpoint_id = str(uuid.uuid4())
            _checkpoint_storage[thread_id] = {
                "checkpoint": checkpoint,
                "metadata": metadata or {},
                "checkpoint_id": checkpoint_id,
                "parent_config": _checkpoint_storage.get(thread_id, {}).get("checkpoint_id"),
            }
            return checkpoint_id

        async def alist(self, thread_id=None, filter=None, before=None, limit=None):
            """List checkpoints, optionally filtered by thread_id."""
            results = []
            for tid, data in _checkpoint_storage.items():
                if thread_id is None or tid == thread_id:
                    results.append({
                        "checkpoint": data["checkpoint"],
                        "metadata": data.get("metadata", {}),
                        "parent_config": data.get("parent_config"),
                    })
            return results[:limit] if limit else results

        async def aput_writes(self, thread_id, checkpoint_id, writes, task_id):
            """Write intermediate channel values (no-op for simple implementations)."""
            pass

    return app


# ── User code: deepagents agent with BlazeCheckpointer (runs in Pyodide) ──────

async def run_deepagents_with_mock_llm(state: dict, services) -> dict:
    """
    USER CODE: Runs inside the Pyodide sandbox.

    Uses REAL deepagents.create_deep_agent() with a mock LLM (GenericFakeChatModel)
    and BlazeCheckpointer for state persistence across invocations.

    State dict keys:
      session_id     — UUID for the agent session (None to create a new session)
      query          — User query to send to the agent
      operation      — "run" (default) or "get_state" (verify state)
      response_content — Mock LLM response content for this invocation
    """
    from itertools import cycle

    from deepagents import create_deep_agent
    from langblaze import BlazeCheckpointer
    from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
    from langchain_core.messages import AIMessage

    session_id = state.get("session_id")
    query = state.get("query", "Hello")
    operation = state.get("operation", "run")
    response_content = state.get("response_content", "I have completed the task.")

    # Create BlazeCheckpointer — proxies LangGraph checkpoint calls to CheckpointService
    checkpointer = BlazeCheckpointer(services)

    # Operation: verify state for an existing session
    if operation == "get_state":
        config = {"configurable": {"thread_id": session_id}}
        result = await checkpointer.aget(config)
        if result:
            checkpoint, metadata, _ = result
            return {
                "session_id": session_id,
                "operation": "get_state",
                "has_state": True,
                "checkpoint": checkpoint,
            }
        return {
            "session_id": session_id,
            "operation": "get_state",
            "has_state": False,
        }

    # Generate session_id for new sessions
    if not session_id:
        import uuid as uuid_mod
        session_id = str(uuid_mod.uuid4())

    # Create a mock LLM that avoids real API calls
    mock_responses = cycle([
        AIMessage(content=response_content),
    ])

    class MockChatModel(GenericFakeChatModel):
        """GenericFakeChatModel extended with bind_tools support."""
        def bind_tools(self, tools, **kwargs):
            return self

    mock_model = MockChatModel(messages=mock_responses)

    # Create the REAL deepagents agent with the mock LLM
    agent = create_deep_agent(
        model=mock_model,
        tools=[],
    )

    config = {
        "configurable": {
            "thread_id": session_id,
        }
    }

    input_state = {
        "messages": [{"role": "user", "content": query}],
    }

    try:
        result = await agent.ainvoke(input_state, config=config)
        messages = result.get("messages", [])
        message_count = len(messages)

        # Persist state via BlazeCheckpointer
        await checkpointer.aput(
            config,
            checkpoint=result,
            metadata={"query": query, "message_count": message_count},
        )

        return {
            "session_id": session_id,
            "operation": "run",
            "message_count": message_count,
            "success": True,
            "agent_type": type(agent).__name__,
            "last_message": str(messages[-1]) if messages else None,
        }

    except Exception as e:
        return {
            "session_id": session_id,
            "operation": "run",
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
        }


# ── Main ──────────────────────────────────────────────────────────────────────

async def main():
    import os

    api_url = os.getenv("BLAZING_API_URL", "http://localhost:8000")
    api_token = os.getenv("BLAZING_API_TOKEN", "demo-token-placeholder")

    print("=== DeepAgents with BlazeCheckpointer Demo ===")
    print()

    # Build and upload the langblaze wheel (required for sandbox use)
    print("[Setup] Building and uploading langblaze wheel...")
    wheel_url = await _build_and_upload_wheel(api_url, api_token)

    # Create app with wheel and sandbox dependencies
    app = make_app(api_url, api_token, wheel_url)

    # Generate signing key
    signing_key = create_signing_key()
    print(f"  Signing key: {signing_key[:16]}...")

    # Publish services
    await app.publish()
    print("  Services published (CheckpointService)")
    print()

    # ── Invocation 1: First query (creates new session) ────────────────────────
    print("--- Invocation 1: First query ---")
    result1 = await execute_user_code(
        run_deepagents_with_mock_llm,
        {
            "session_id": None,
            "query": "Research the LangGraph architecture",
            "operation": "run",
            "response_content": "I'll research LangGraph architecture for you.",
        },
        api_url=api_url,
        api_token=api_token,
        signing_key=signing_key,
    )
    print(f"  Success: {result1.get('success')}")
    session_id = result1["session_id"]
    print(f"  Session ID: {session_id}")
    print(f"  Agent type: {result1.get('agent_type')}")
    print(f"  Messages: {result1.get('message_count')}")
    print()

    # ── Invocation 2: Second query (resumes existing session) ──────────────────
    print("--- Invocation 2: Resume session ---")
    result2 = await execute_user_code(
        run_deepagents_with_mock_llm,
        {
            "session_id": session_id,
            "query": "Now analyze the checkpoint patterns",
            "operation": "run",
            "response_content": "Based on my research, here are the checkpoint patterns.",
        },
        api_url=api_url,
        api_token=api_token,
        signing_key=signing_key,
    )
    print(f"  Success: {result2.get('success')}")
    print(f"  Session ID: {result2['session_id']} (same session)")
    print(f"  Messages: {result2.get('message_count')}")
    print()

    # ── Invocation 3: Verify accumulated state ─────────────────────────────────
    print("--- Invocation 3: Verify accumulated state ---")
    result3 = await execute_user_code(
        run_deepagents_with_mock_llm,
        {
            "session_id": session_id,
            "operation": "get_state",
        },
        api_url=api_url,
        api_token=api_token,
        signing_key=signing_key,
    )
    print(f"  has_state: {result3.get('has_state')}")
    print()

    print("=== Demo complete ===")
    print(f"  Session {session_id} persisted across 3 invocations")


if __name__ == "__main__":
    asyncio.run(main())
