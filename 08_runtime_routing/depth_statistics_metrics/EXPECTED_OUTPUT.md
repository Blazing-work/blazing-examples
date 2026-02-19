# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'operations_scanned': 1, 'max_depth': 1, 'avg_depth': 1.0, 'depth_distribution': {1: 1}}
```

## Notes

- The depth metrics reflect the depth of step nesting in the workflow graph
- Requires a running Blazing infrastructure: `docker-compose up -d`
- The exact values may vary depending on the server state and prior workflow runs
- Queries `GET /v1/metrics/depth` and prints the full response JSON
