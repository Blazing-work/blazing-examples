# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'result': 5}
```

## Notes

- `x=1: step_a(1)=2, step_b calls step_a: 2+1=3, step_c calls step_b: 3+1=4, chain_workflow adds 1: 4+1=5`
- Requires a running Blazing infrastructure: `docker-compose up -d`
- Demonstrates chained step depth: step_c calls step_b which calls step_a — depth tracking across 3 levels
