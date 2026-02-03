# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Running system health check...

Health Check Results:
  Overall Status: HEALTHY
  Timestamp: [current timestamp in ISO format]

  Service Status:
    [OK] database: healthy
    [OK] cache: healthy
    [OK] external_api: healthy
```

## Notes

- Runs health checks for 3 services concurrently (database, cache, external_api)
- All services are simulated and return healthy status
- Overall status is "healthy" when all individual checks pass
- Timestamp shows when the health check was performed
- If any service fails, overall status would be "degraded" and error details would appear
- Uses simulated services for demonstration
- Demonstrates health check pattern with parallel service verification
