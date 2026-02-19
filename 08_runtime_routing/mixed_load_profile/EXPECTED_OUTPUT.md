# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'cpu': 499500, 'io': 2000}
```

## Notes

- `cpu_work(1000)` computes sum(range(1000)) = 499500; `io_work(1000)` returns 1000 * 2 = 2000
- Requires a running Blazing infrastructure: `docker-compose up -d`
- Demonstrates concurrent execution of a BLOCKING CPU step and an async I/O step via `asyncio.gather`
