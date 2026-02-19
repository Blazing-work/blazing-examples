# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'result': 6}
```

## Notes

- `5 + 1 = 6` — the child_step increments x=5 by 1
- Requires a running Blazing infrastructure: `docker-compose up -d`
- Demonstrates basic depth tracking: workflow calls one step at depth=1
