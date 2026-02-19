# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'result': 12}
```

## Notes

- `10 + 1 + 1 = 12` — the workflow increments value=10 twice
- Requires a running Blazing infrastructure: `docker-compose up -d`
- Uses synchronous blocking result retrieval: `handle.wait_result_sync()`
