# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'result': 13}
```

## Notes

- `10 + 3 increments = 13` — the workflow calls `increment` three times starting from x=10
- Requires a running Blazing infrastructure: `docker-compose up -d`
- Demonstrates callable workflow syntax: `app.add_three(x=10).wait_result()`
