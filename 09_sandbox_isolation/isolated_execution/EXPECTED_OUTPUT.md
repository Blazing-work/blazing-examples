# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'result': 42}
```

## Notes

- `21 * 2 = 42` — the sandboxed secure_compute step doubles x=21
- Requires a running Blazing infrastructure: `docker-compose up -d`
- The step runs inside the Pyodide sandbox, isolated from the main executor environment
