# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'one_liner': 35, 'handle': 35, 'run': 35}
```

## Notes

- `(2 + 3) * 7 = 35` — all three execution patterns return the same result
- Requires a running Blazing infrastructure: `docker-compose up -d`
- Demonstrates three equivalent patterns: `wait_result()`, `handle.result()`, and `run()` by name
