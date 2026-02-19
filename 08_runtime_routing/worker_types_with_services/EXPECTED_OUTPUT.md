# Expected Output

## Running

```bash
python flow.py
```

## Requirements

- Running Blazing infrastructure: `docker-compose up -d`
- `BLAZING_API_URL` (defaults to `http://localhost:8000`)
- `BLAZING_API_TOKEN` (defaults to `demo-token-placeholder`)

## Output

```
=== Worker Types with Services Demo ===

Four worker types, one service (MathOpsService):
  BLOCKING            (trusted sync):   value + 10
  NON_BLOCKING        (trusted async):  value *  2  via service
  NON_BLOCKING_SANDBOXED (sandboxed):   value -  5  via service
  NON_BLOCKING_SANDBOXED (sandboxed):   value /  3  via service

  start                    : 5
  after_blocking           : 15   (5 + 10)
  after_non_blocking       : 30   (15 * 2)
  after_blocking_sandboxed : 25   (30 - 5)
  after_non_blocking_sandboxed: 8    (25 / 3)
  final                    : 8

All four worker types accessed MathOpsService with identical services['Name'] API.
```

## Math Chain

| Step | Worker Type | Operation | Input | Output |
|------|-------------|-----------|-------|--------|
| 1 | BLOCKING (trusted sync) | + 10 | 5 | 15 |
| 2 | NON_BLOCKING (trusted async) | * 2 | 15 | 30 |
| 3 | NON_BLOCKING_SANDBOXED (sandboxed) | - 5 | 30 | 25 |
| 4 | NON_BLOCKING_SANDBOXED (sandboxed) | / 3 | 25 | 8 |

## Notes

- The BLOCKING step cannot call services (sync context) — only pure computation
- Steps 2, 3, and 4 all use `services['MathOpsService']` with the same dict-access pattern
- Sandboxed steps run in the Pyodide WASM sandbox; service calls cross the sandbox boundary via the JS bridge
- The final result is always 8 for start_value=5: ((5+10)*2-5)//3 = 8
