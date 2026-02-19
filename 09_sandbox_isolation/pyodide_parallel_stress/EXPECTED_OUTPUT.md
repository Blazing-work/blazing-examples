# Expected Output

## Running

```bash
python flow.py
```

## Output

```
[1, 4, 9, 16, 25]
```

## Notes

- `[1^2, 2^2, 3^2, 4^2, 5^2] = [1, 4, 9, 16, 25]` — squares of [1, 2, 3, 4, 5] computed in parallel
- Requires a running Blazing infrastructure: `docker-compose up -d`
- Uses `asyncio.gather` to fire all 5 sandboxed compute calls simultaneously
