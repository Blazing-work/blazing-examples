# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'operations_scanned': 1}
```

## Notes

- `operations_scanned` reflects the number of workflow operations scanned by the depth metrics endpoint
- Requires a running Blazing infrastructure: `docker-compose up -d`
- The exact count may vary depending on prior workflow runs in the same session
- Queries `GET /v1/metrics/depth` after running one workflow execution
