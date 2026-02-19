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
=== DeepAgents with BlazeCheckpointer Demo ===

[Setup] Building and uploading langblaze wheel...
  Built wheel: langblaze-0.1.0-py3-none-any.whl
  Wheel URL: http://localhost:8000/v1/wheels/langblaze-0.1.0-py3-none-any.whl
  Signing key: a3f2c1d4e5b6f7a8...
  Services published (CheckpointService)

--- Invocation 1: First query ---
  Success: True
  Session ID: a3f2c1d4-e5b6-f7a8-9012-3456789abcde
  Agent type: CompiledStateGraph
  Messages: 2

--- Invocation 2: Resume session ---
  Success: True
  Session ID: a3f2c1d4-e5b6-f7a8-9012-3456789abcde (same session)
  Messages: 4

--- Invocation 3: Verify accumulated state ---
  has_state: True

=== Demo complete ===
  Session a3f2c1d4-e5b6-f7a8-9012-3456789abcde persisted across 3 invocations
```

## Invocation Pattern

| Invocation | Input | Output |
|------------|-------|--------|
| 1 | `session_id=None`, `query="Research LangGraph architecture"` | New UUID session created, 2 messages |
| 2 | `session_id=<uuid>`, `query="Analyze checkpoint patterns"` | Session resumed, 4 messages |
| 3 | `session_id=<uuid>`, `operation="get_state"` | `has_state=True`, checkpoint verified |

## Notes

- Session IDs are random UUIDs — actual values will differ each run
- Message count grows across invocations as prior context is loaded via BlazeCheckpointer
- The langblaze wheel must be built from the local source tree before the first run
- `_checkpoint_storage` is a module-level dict — it persists within the process but resets on restart
- For production, replace the in-memory storage with Redis-backed persistence
