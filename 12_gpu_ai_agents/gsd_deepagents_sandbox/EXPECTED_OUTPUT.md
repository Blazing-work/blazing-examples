# Expected Output

## Running

```bash
python flow.py
```

## Requirements

- `pip install blazing langblaze`
- Running Blazing infrastructure: `docker-compose up -d`
- `BLAZING_API_URL` (defaults to `http://localhost:8000`)
- `BLAZING_API_TOKEN` (defaults to `demo-token-placeholder`)
- langblaze source tree at `../../../../langblaze` (relative to this file, for wheel build)

## Output

```
=== GSD-Style Tool Registry in Pyodide Sandbox ===

[Setup] Building and uploading langblaze wheel...
  Built wheel: langblaze-0.1.0-py3-none-any.whl
  Wheel URL: http://localhost:8000/v1/wheels/langblaze-0.1.0-py3-none-any.whl
  Signing key: a3f2c1d4e5b6f7a8...
  Published (no services — registry is data-driven)

--- Operation 1: List all tools ---
  Tool count: 3
  Tool names: ['write_file', 'read_file', 'run_analysis']

--- Operation 2: Filter by tag "filesystem" ---
  Filtered count: 2
  Filtered names: ['write_file', 'read_file']

=== Done ===
```

## Registry Operations

| Operation | Input | Output |
|-----------|-------|--------|
| `"list"` | `tool_definitions` dict | `tool_count=3`, `tool_names=[...]`, `registry={...}` |
| `"filter_by_tag"` | `tool_definitions` + `tag="filesystem"` | `filtered_count=2`, `filtered_names=["write_file","read_file"]` |

## Tool Definitions

| Tool | Tags | Requires |
|------|------|----------|
| `write_file` | `["filesystem", "io"]` | `[]` |
| `read_file` | `["filesystem", "io"]` | `[]` |
| `run_analysis` | `["analytics"]` | `["read_file"]` |

## Notes

- Tool definitions are passed as plain Python dicts in the `state` dict — no GSD framework is imported into Pyodide
- The `requires` field models the dependency graph; your orchestrator can use it to determine execution order
- Wheel URL will differ each run based on the local server; signing key prefix will also vary
- This example does not register any services (`app.publish()` with no `@app.service` decorators) because the registry is pure data
- Compare with `deepagents_with_checkpoint/` which focuses on `BlazeCheckpointer` and multi-turn session persistence
