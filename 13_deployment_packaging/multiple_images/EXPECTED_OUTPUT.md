# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'cpu': 2.0, 'io': {'status': 0}}
```

## Notes

- `cpu_workflow([1, 2, 3])` returns `mean([1, 2, 3]) = 2.0`
- `io_workflow()` runs `curl -s https://example.com` and returns its exit code (0 = success)
- Requires a running Blazing infrastructure: `docker-compose up -d`
- Demonstrates two workflows using different custom images: `cpu_image` (numpy) and `io_image` (curl)
