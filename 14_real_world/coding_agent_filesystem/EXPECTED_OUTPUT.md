# Expected Output

## Running

```bash
python flow.py
```

## Requirements

- Running Blazing infrastructure: `docker-compose up -d`
- `BLAZING_API_URL` (defaults to `http://localhost:8000`)
- `BLAZING_API_TOKEN` (defaults to `demo-token-placeholder`)
- langblaze source tree at `../../../../langblaze` (for wheel build)

## Output

```
=== Coding Agent with BlazeFileSystem Demo ===

Architecture:
  Pyodide sandbox (coding_agent_workflow)
    -> BlazeFileSystem -> StorageService (trusted) -> in-memory files
    -> BlazeCheckpointer -> CheckpointService (trusted) -> in-memory state
    -> Mock git tools (git_init, git_commit)

[Setup] Building wheel and publishing services...
  Built wheel: langblaze-0.1.0-py3-none-any.whl
  Wheel URL: http://localhost:8000/v1/wheels/langblaze-0.1.0-py3-none-any.whl
  Services published (CheckpointService + StorageService)

[Step 1] Executing coding agent workflow...
  Session ID: b7e3a2f1-c4d5-6e7f-8901-234567890abc
  Success: True
  Tool calls: ['git_init', 'write_file', 'git_commit', 'read_file']
  Files written: ['/workspace/my-project/main.py']
  File verified: True
  File preview: def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    print(hello())

=== Demo complete ===
```

## Tool Call Sequence

| Turn | Tool Calls | Type |
|------|------------|------|
| 1 | `git_init`, `write_file`, `git_commit` | Parallel batch (mock + real + mock) |
| 2 | `read_file` | File verification (real) |
| 3 | (final answer) | Agent terminates |

## File Written

Path: `/workspace/my-project/main.py`

```python
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    print(hello())
```

## Notes

- Session IDs are random UUIDs — actual values will differ each run
- `git_init` and `git_commit` are mock functions — no real git binary is invoked
- `write_file` and `read_file` are real operations via `BlazeFileSystem` + `StorageService`
- `file_verified: True` confirms the file was actually written and is readable from StorageService
- The agent loop runs entirely in the Pyodide sandbox; StorageService and CheckpointService run on trusted workers
