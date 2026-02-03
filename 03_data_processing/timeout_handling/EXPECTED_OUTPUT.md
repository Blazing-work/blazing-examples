# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Running workflow with 5 second timeout (operation takes 10 seconds)...
Result: {'success': False, 'error': 'Operation timed out'}
```

## Notes

- Operation intentionally takes 10 seconds (simulated slow operation)
- Workflow timeout is set to 5 seconds
- Result is deterministic: operation will always timeout
- Demonstrates asyncio.wait_for() timeout handling
- In production, would be used to prevent long-running operations from blocking system
- Timeout errors are caught and returned as workflow result (not raised as exceptions)
