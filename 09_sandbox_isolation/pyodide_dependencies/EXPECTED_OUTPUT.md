# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'mean': 2.5, 'sum': 10.0}
```

## Notes

- `mean([1,2,3,4]) = 2.5`, `sum([1,2,3,4]) = 10.0` — computed by numpy inside the sandbox
- Requires a running Blazing infrastructure: `docker-compose up -d`
- The `sandbox_dependencies=['numpy']` installs numpy into the Pyodide sandbox at startup
