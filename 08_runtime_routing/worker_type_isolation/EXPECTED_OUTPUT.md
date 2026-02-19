# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'trusted': 6, 'sandboxed': 7}
```

## Notes

- `trusted_async(5) = 5 + 1 = 6`, `sandboxed_async(5) = 5 + 2 = 7`
- Requires a running Blazing infrastructure: `docker-compose up -d`
- Demonstrates worker type isolation: trusted steps run in the main executor, sandboxed in Pyodide
