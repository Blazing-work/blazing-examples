# Expected Output

## Running

```bash
python flow.py
```

## Output

```
INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

## Notes

- Server starts and listens on http://0.0.0.0:8080
- Process ID (XXXXX) will vary
- Server runs until manually stopped with CTRL+C
- Demonstrates error handling with validation and custom error messages
- Example requests:
  ```bash
  # Valid request
  curl -X POST http://localhost:8080/transaction/calculate \
    -H "Content-Type: application/json" \
    -d '{"amount": 500}'
  # Response: {"amount": 500, "fee": 15.0, "total": 515.0, "status": "success"}

  # Invalid request (negative amount)
  curl -X POST http://localhost:8080/transaction/calculate \
    -H "Content-Type: application/json" \
    -d '{"amount": -100}'
  # Response: Error status with "Amount must be positive" message
  ```
- Fee calculation tiers: <100 (5%), 100-1000 (3%), >1000 (1%)
