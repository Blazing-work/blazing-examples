# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'result': 'hello'}
```

## Notes

- The echo step returns the message as-is: `ping(message='hello') = 'hello'`
- Requires a running Blazing infrastructure: `docker-compose up -d`
- Demonstrates connecting to a remote control plane via `BLAZING_API_URL` and `BLAZING_API_TOKEN` env vars
