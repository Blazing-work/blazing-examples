# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'result': 14}
```

## Notes

- `(3 + 4) * 2 = 14` — MathService.add(3, 4) returns 7, then double() multiplies by 2
- Requires a running Blazing infrastructure: `docker-compose up -d`
- Uses `async with app:` context manager to manage service lifecycle alongside workflow execution
