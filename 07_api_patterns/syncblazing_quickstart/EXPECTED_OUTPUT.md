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

- `5 + 7 = 12` — the add step sums x=5 and y=7
- Requires a running Blazing infrastructure: `docker-compose up -d`
- Uses `SyncBlazing` for fully synchronous workflow execution — no async/await needed in calling code
