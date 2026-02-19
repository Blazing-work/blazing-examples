# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'trusted': 11, 'sandboxed': 12}
```

## Notes

- `trusted_step(10) = 10 + 1 = 11`, `sandboxed_step(10) = 10 + 2 = 12`
- Requires a running Blazing infrastructure: `docker-compose up -d`
- Demonstrates mixing trusted NON-BLOCKING and sandboxed NON-BLOCKING steps in one workflow
