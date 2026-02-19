# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'result': 81}
```

## Notes

- `9 * 9 = 81` — the square step computes x*x for value=9
- Requires a running Blazing infrastructure: `docker-compose up -d`
- Uses synchronous API: `app.publish_sync()` and `app.run_sync('compute', value=9)`
