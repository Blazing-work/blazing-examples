# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'blocking': 10, 'async': 6, 'sandboxed_blocking': 15, 'sandboxed_async': 7}
```

## Notes

- `blocking_step(5) = 5*2 = 10`, `async_step(5) = 5+1 = 6`, `sandboxed_blocking_step(5) = 5*3 = 15`, `sandboxed_async_step(5) = 5+2 = 7`
- Requires a running Blazing infrastructure: `docker-compose up -d`
- Shows all four worker type combinations: trusted+BLOCKING, trusted+NON-BLOCKING, sandboxed+BLOCKING, sandboxed+NON-BLOCKING
