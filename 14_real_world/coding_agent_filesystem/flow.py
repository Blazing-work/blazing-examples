"""
Coding Agent with BlazeFileSystem

A multi-phase coding agent that runs deepagents inside the Pyodide sandbox with real
filesystem operations proxied to a trusted StorageService — git commands are mocked
while file reads and writes use BlazeFileSystem backed by StorageService in-memory
storage. Demonstrates production-ready patterns for sandboxed agents that need file I/O.

Patterns shown:
  1. StorageService — trusted in-memory file storage called from sandbox
  2. BlazeFileSystem(services) — file I/O adapter proxying to StorageService
  3. create_filesystem_tools(fs) — LangChain tools (read_file, write_file, list_files)
  4. Mixed tools: mock git tools + real filesystem tools in one agent
  5. BlazeCheckpointer — persist agent state across the coding workflow phases
  6. fs.aexists() / fs.aread() — verify file was actually written to StorageService

Requires: pip install blazing langblaze deepagents langgraph langchain-core
          docker-compose up -d
"""

import asyncio
from pathlib import Path

import httpx
from blazing import Blazing
from blazing.dynamic_code import create_signing_key, execute_user_code
from blazing.wheel_builder import build_wheel, upload_wheel
from langblaze import CheckpointService, StorageService


# ── Setup helpers ─────────────────────────────────────────────────────────────

async def _build_and_publish(api_url: str, api_token: str) -> str:
    """Build langblaze wheel, create app with both services, publish. Returns signing_key."""
    langblaze_dir = Path(__file__).parent.parent.parent.parent / "langblaze"
    wheel_info = build_wheel(str(langblaze_dir))
    print(f"  Built wheel: {wheel_info.filename}")

    await asyncio.sleep(2)
    async with httpx.AsyncClient(timeout=60.0) as client:
        wheel_url = await upload_wheel(wheel_info, api_url, api_token, client)
    print(f"  Wheel URL: {wheel_url}")

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
    signing_key = create_signing_key()

    # Register both trusted services
    app.service(CheckpointService)   # LangGraph checkpoint persistence
    app.service(StorageService)      # Real file I/O backend

    await app.publish()
    print("  Services published (CheckpointService + StorageService)")
    return signing_key


# ── User code: coding agent workflow (runs in Pyodide sandbox) ─────────────────

async def coding_agent_workflow(state, services=None) -> dict:
    """
    USER CODE: Runs inside the Pyodide sandbox.

    A coding agent that:
      1. Initializes a git repo (mock tool)
      2. Writes a Python file via BlazeFileSystem (real file I/O)
      3. Commits changes (mock tool)
      4. Reads back the file to verify it was written
      5. Saves agent state via BlazeCheckpointer

    Tool call pattern (batched in one LLM turn):
      git_init + write_file + git_commit -> read_file -> final answer
    """
    from itertools import cycle

    from deepagents import create_deep_agent
    from langblaze import BlazeCheckpointer, BlazeFileSystem, create_filesystem_tools
    from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
    from langchain_core.messages import AIMessage

    session_id = state.get("session_id")
    if not session_id:
        import uuid as uuid_mod
        session_id = str(uuid_mod.uuid4())

    # BlazeCheckpointer — state persistence via CheckpointService
    checkpointer = BlazeCheckpointer(services)

    # BlazeFileSystem — real file I/O via StorageService
    fs = BlazeFileSystem(services)
    filesystem_tools = create_filesystem_tools(fs)

    # Mock git tools (git is mocked; file operations are real)
    def git_init(path: str) -> str:
        """Initialize a git repository at the given path."""
        return f"Initialized empty Git repository in {path}"

    def git_commit(message: str) -> str:
        """Stage all changes and commit with the given message."""
        return f"Committed: {message} [abc1234]"

    # Combine mock git tools with real filesystem tools
    tools = [git_init, git_commit] + filesystem_tools

    # Track operations
    tool_calls_made = []
    files_written = []

    # Mock LLM — 3 turns: (1) batch git+file+commit, (2) read_file verify, (3) final
    mock_responses = cycle([
        # Turn 1: parallel tool calls — git init, write file, git commit
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "git_init",
                    "args": {"path": "/workspace/my-project"},
                    "id": "call_1",
                },
                {
                    "name": "write_file",
                    "args": {
                        "path": "/workspace/my-project/main.py",
                        "content": "def hello():\n    return 'Hello, World!'\n\nif __name__ == '__main__':\n    print(hello())\n",
                    },
                    "id": "call_2",
                },
                {
                    "name": "git_commit",
                    "args": {"message": "feat: add main.py with hello function"},
                    "id": "call_3",
                },
            ],
        ),
        # Turn 2: read back the file to verify it was written
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "read_file",
                    "args": {"path": "/workspace/my-project/main.py"},
                    "id": "call_4",
                }
            ],
        ),
        # Turn 3: final summary (terminates agent loop)
        AIMessage(
            content="Project initialized with main.py committed and verified."
        ),
    ])

    class MockChatModel(GenericFakeChatModel):
        """GenericFakeChatModel extended with bind_tools support."""
        def bind_tools(self, tools, **kwargs):
            return self

    mock_model = MockChatModel(messages=mock_responses)

    # Create agent with all tools (mock git + real filesystem)
    agent = create_deep_agent(
        model=mock_model,
        tools=tools,
    )

    config = {"configurable": {"thread_id": session_id}}
    input_state = {
        "messages": [
            {"role": "user", "content": "Initialize a Python project with git"}
        ],
    }

    try:
        # Run the agent
        result = await agent.ainvoke(input_state, config=config)
        messages = result.get("messages", [])

        # Extract tool calls and track files written
        for msg in messages:
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tc in msg.tool_calls:
                    tool_calls_made.append(tc["name"])
                    if tc["name"] == "write_file":
                        files_written.append(tc.get("args", {}).get("path", "unknown"))

        # Verify file was actually written to StorageService via BlazeFileSystem
        file_exists = await fs.aexists("/workspace/my-project/main.py")
        file_content = await fs.aread("/workspace/my-project/main.py")

        # Save checkpoint with workflow metadata
        await checkpointer.aput(
            config,
            checkpoint=result,
            metadata={
                "phase": "coding_workflow",
                "tool_count": len(tool_calls_made),
                "files_written": files_written,
                "file_verified": file_exists,
            },
        )

        return {
            "session_id": session_id,
            "success": True,
            "tool_calls_made": tool_calls_made,
            "files_written": files_written,
            "file_verified": file_exists,
            "file_content_preview": file_content[:100] if file_content else None,
        }

    except Exception as e:
        return {
            "session_id": session_id,
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
        }


# ── Main ──────────────────────────────────────────────────────────────────────

async def main():
    import os

    api_url = os.getenv("BLAZING_API_URL", "http://localhost:8000")
    api_token = os.getenv("BLAZING_API_TOKEN", "demo-token-placeholder")

    print("=== Coding Agent with BlazeFileSystem Demo ===")
    print()
    print("Architecture:")
    print("  Pyodide sandbox (coding_agent_workflow)")
    print("    -> BlazeFileSystem -> StorageService (trusted) -> in-memory files")
    print("    -> BlazeCheckpointer -> CheckpointService (trusted) -> in-memory state")
    print("    -> Mock git tools (git_init, git_commit)")
    print()

    print("[Setup] Building wheel and publishing services...")
    signing_key = await _build_and_publish(api_url, api_token)
    print()

    print("[Step 1] Executing coding agent workflow...")
    result = await execute_user_code(
        coding_agent_workflow,
        {"session_id": None},
        api_url=api_url,
        api_token=api_token,
        signing_key=signing_key,
        timeout=3600.0,
    )

    print(f"  Session ID: {result.get('session_id')}")
    print(f"  Success: {result.get('success')}")
    print(f"  Tool calls: {result.get('tool_calls_made')}")
    print(f"  Files written: {result.get('files_written')}")
    print(f"  File verified: {result.get('file_verified')}")
    print(f"  File preview: {result.get('file_content_preview')}")
    print()
    print("=== Demo complete ===")


if __name__ == "__main__":
    asyncio.run(main())
