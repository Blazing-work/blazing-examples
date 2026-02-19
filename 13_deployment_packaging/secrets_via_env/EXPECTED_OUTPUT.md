# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'secret': 'unset'}
```

## Notes

- The step reads `MY_SECRET` from the environment; defaults to `'unset'` if not set
- To test with a real secret: `MY_SECRET=my-value python flow.py` → `{'secret': 'my-value'}`
- Requires a running Blazing infrastructure: `docker-compose up -d`
- Demonstrates injecting secrets via environment variables rather than hardcoding them
