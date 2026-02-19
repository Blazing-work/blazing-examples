# Expected Output

## Running

```bash
python flow.py
```

## Output

```
[2, 4, 6]
```

## Notes

- `[1*2, 2*2, 3*2] = [2, 4, 6]` — each value in [1, 2, 3] doubled inside the sandbox
- Requires a running Blazing infrastructure: `docker-compose up -d`
- The simplest sandboxed step example: `@app.step(sandboxed=True)` with a list comprehension
