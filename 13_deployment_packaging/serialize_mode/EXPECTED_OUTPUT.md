# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Loading Strategy: serialize

Strategies comparison:
  'wheel'      — build & upload wheel (default, best for production)
  'serialize'  — serialize functions at runtime (fastest to iterate)
  'dockerfile' — bundle code in custom image (full control)

Published with loading_strategy='serialize'

Result: Report for 'monthly sales': sum=15, mean=3.0, n=5
```

## Notes

- Requires a running Blazing infrastructure: `docker-compose up -d`
- `analysis_pipeline('monthly sales')`: fetch returns rows=[1,2,3,4,5], sum=15, mean=3.0, n=5
- The `serialize` loading strategy sends dill-serialized functions to workers — no wheel build step needed
