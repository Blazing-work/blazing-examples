# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'result': 10, 'attempt': 1}
```

## Notes

- `5 * 2 = 10` — the flaky_step succeeds on the first attempt since x=5 >= 0
- Requires a running Blazing infrastructure: `docker-compose up -d`
- The retry loop only retries on exceptions; with x=5 there is no exception so attempt is always 1
