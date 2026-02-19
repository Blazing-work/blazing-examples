# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'result': 12}
```

## Notes

- `step_one(5) = 5 + 1 = 6`, `step_two(6) = 6 * 2 = 12`
- Requires a running Blazing infrastructure: `docker-compose up -d`
- CheckpointService saves intermediate results at each step for agent-style fault tolerance
