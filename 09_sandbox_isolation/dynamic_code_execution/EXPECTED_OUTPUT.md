# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'result': 20}
```

## Notes

- `(2 + 3) * 4 = 20` — the sandboxed step evaluates the expression string safely
- Requires a running Blazing infrastructure: `docker-compose up -d`
- The sandbox restricts builtins to prevent unsafe code execution
