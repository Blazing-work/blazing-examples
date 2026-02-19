# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'result': 10}
```

## Notes

- `5 * 2 = 10` — the multiply step doubles value=5
- Requires a running Blazing infrastructure: `docker-compose up -d`
- Demonstrates using `handle.wait()` to poll completion before calling `handle.wait_result()`
