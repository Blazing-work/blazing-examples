"""
ReAct Agent as Dynamic Code

Run a complete LangGraph-style ReAct agent loop as user-submitted dynamic code in the
Pyodide sandbox. LLMService, ToolService, and StateService execute on trusted workers;
the agent loop and state machine run as sandboxed user code signed with a signing key.
Agent state persists across invocations via DictConnector (Redis cache API).

Patterns shown:
  1. execute_user_code() — submit Python function as signed sandboxed code
  2. create_signing_key() — generate key for trusted code submission
  3. LLMService + ToolService as trusted-worker services called from sandbox
  4. DictConnector pattern — state persistence via /v1/data/cache API

Requires: pip install blazing langblaze
          docker-compose up -d
          OPENAI_API_KEY environment variable (for production; mock used here)
"""

import asyncio
import os

from blazing import Blazing
from blazing.base import BaseService
from blazing.dynamic_code import create_signing_key, execute_user_code


app = Blazing(
    api_url=os.getenv("BLAZING_API_URL", "http://localhost:8000"),
    api_token=os.getenv("BLAZING_API_TOKEN", "demo-token-placeholder"),
)


# ── LLMService (trusted worker — holds API credentials) ──────────────────────

@app.service
class LLMService(BaseService):
    """
    LLM service running on trusted workers with API credentials.
    Uses mock responses for demo purposes — replace with real connector for production.

    In production, swap the mock logic for:
        from blazing.local.llm import OpenAIConnector
    """

    def __init__(self, connectors):
        self._connectors = connectors
        self._call_count = 0

    async def chat(self, messages: list, tools: list = None) -> dict:
        """
        Chat completion. Returns OpenAI-style response dict.
        Mock implementation: first call returns tool call, second call returns final answer.
        """
        self._call_count += 1
        last_user_content = ""
        for msg in messages:
            if msg.get("role") == "user":
                last_user_content = msg.get("content", "")

        # First call: decide to use a tool
        if self._call_count == 1:
            return {
                "role": "assistant",
                "content": None,
                "tool_calls": [{
                    "id": "call_001",
                    "function": {
                        "name": "search",
                        "arguments": {"query": last_user_content},
                    },
                }],
            }

        # Subsequent calls: return final answer
        return {
            "role": "assistant",
            "content": f"Based on my research, here is the answer to: {last_user_content}",
            "tool_calls": None,
        }


# ── ToolService (trusted worker — executes tools securely) ───────────────────

@app.service
class ToolService(BaseService):
    """
    Tool execution service on trusted workers.
    Exposes tools that the sandbox agent can call safely.
    """

    def __init__(self, connectors):
        self._connectors = connectors

    async def execute(self, tool_name: str, args: dict) -> str:
        """Execute a named tool and return a string result."""
        if tool_name == "search":
            query = args.get("query", "")
            return f"Search result for '{query}': Found 3 relevant documents about this topic."
        elif tool_name == "calculator":
            # Safe fixed-response demo for calculator tool
            return "Calculator result: 42"
        return f"Unknown tool: {tool_name}"


# ── StateService (trusted worker — persists agent state) ─────────────────────

@app.service
class StateService(BaseService):
    """
    State persistence service. Backed by an in-memory dict for demo;
    replace with DictConnector-backed Redis for production multi-turn sessions.
    """

    def __init__(self, connectors):
        self._connectors = connectors
        self._storage: dict = {}

    async def get_state(self, session_id: str) -> dict | None:
        """Load agent state for a session."""
        return self._storage.get(session_id)

    async def put_state(self, session_id: str, state: dict) -> bool:
        """Persist agent state for a session."""
        self._storage[session_id] = state
        return True


# ── User code: ReAct agent loop (runs in Pyodide sandbox) ────────────────────

async def react_agent_loop(state: dict, services) -> dict:
    """
    USER CODE: Runs inside the Pyodide sandbox as signed dynamic code.

    Implements a ReAct (Reason + Act) loop:
      LOAD_STATE -> CALL_LLM -> EXECUTE_TOOLS -> SAVE_STATE -> repeat until final answer

    Services are called through the trusted-worker bridge — the sandbox never
    holds API keys or direct database connections.
    """
    import uuid as uuid_mod

    session_id = state.get("session_id") or str(uuid_mod.uuid4())
    query = state.get("query", "What can you help me with?")
    max_steps = state.get("max_steps", 5)

    # Load prior context from StateService
    prior_state = await services["StateService"].get_state(session_id)
    messages = prior_state.get("messages", []) if prior_state else []

    # Add the new user query
    messages.append({"role": "user", "content": query})

    steps = 0
    final_answer = None

    # ReAct loop
    while steps < max_steps:
        steps += 1

        # Reason: call LLM to decide next action
        llm_response = await services["LLMService"].chat(messages)
        tool_calls = llm_response.get("tool_calls")

        if not tool_calls:
            # Final answer reached
            final_answer = llm_response.get("content", "")
            messages.append({"role": "assistant", "content": final_answer})
            break

        # Act: execute each tool call
        messages.append({
            "role": "assistant",
            "content": None,
            "tool_calls": tool_calls,
        })

        for tc in tool_calls:
            tool_name = tc["function"]["name"]
            tool_args = tc["function"]["arguments"]
            tool_result = await services["ToolService"].execute(tool_name, tool_args)
            messages.append({
                "role": "tool",
                "tool_call_id": tc["id"],
                "content": tool_result,
            })

    # Save updated state via StateService
    updated_state = {"messages": messages, "session_id": session_id}
    await services["StateService"].put_state(session_id, updated_state)

    return {
        "session_id": session_id,
        "response": final_answer or "Agent loop completed without final answer.",
        "steps": steps,
        "message_count": len(messages),
    }


# ── Main ──────────────────────────────────────────────────────────────────────

async def main():
    print("=== ReAct Agent as Dynamic Code Demo ===")
    print()
    print("Architecture:")
    print("  Pyodide sandbox (react_agent_loop) -> LLMService (trusted) -> mock LLM")
    print("  Pyodide sandbox (react_agent_loop) -> ToolService (trusted) -> mock tools")
    print("  Pyodide sandbox (react_agent_loop) -> StateService (trusted) -> in-memory store")
    print()

    signing_key = create_signing_key()
    print(f"Signing key generated: {signing_key[:16]}...")
    print()

    await app.publish()

    api_url = os.getenv("BLAZING_API_URL", "http://localhost:8000")
    api_token = os.getenv("BLAZING_API_TOKEN", "demo-token-placeholder")

    # Invocation 1: New session
    print("--- Invocation 1: New session ---")
    result1 = await execute_user_code(
        react_agent_loop,
        {"session_id": None, "query": "Research the LangGraph architecture"},
        api_url=api_url,
        api_token=api_token,
        signing_key=signing_key,
    )
    session_id = result1["session_id"]
    print(f"  Session ID: {session_id}")
    print(f"  Steps taken: {result1['steps']}")
    print(f"  Response: {result1['response']}")
    print()

    # Invocation 2: Resume session
    print("--- Invocation 2: Resume session ---")
    result2 = await execute_user_code(
        react_agent_loop,
        {"session_id": session_id, "query": "Summarize your findings"},
        api_url=api_url,
        api_token=api_token,
        signing_key=signing_key,
    )
    print(f"  Session ID: {result2['session_id']} (same session)")
    print(f"  Total messages: {result2['message_count']}")
    print(f"  Response: {result2['response']}")
    print()


if __name__ == "__main__":
    asyncio.run(main())
