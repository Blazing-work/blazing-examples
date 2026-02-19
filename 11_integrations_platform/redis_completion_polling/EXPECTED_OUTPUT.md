# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'result': 11}
```

## Notes

- `10 + 1 = 11` — add_one increments x=10
- Requires a running Blazing infrastructure with Redis: `docker-compose up -d`
- Demonstrates connecting to a Blazing control plane via environment variables `BLAZING_API_URL` and `BLAZING_API_TOKEN`
