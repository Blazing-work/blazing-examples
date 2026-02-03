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
- Demonstrates multi-step workflow pipeline: validate → compute → format
- Example request:
  ```bash
  curl -X POST http://localhost:8080/analyze \
    -H "Content-Type: application/json" \
    -d '{"data": {"values": [1, 2, 3, 4, 5]}}'
  # Response: {
  #   "summary": "Analyzed 5 values",
  #   "statistics": {"count": 5, "sum": 15, "average": 3.0, "min": 1, "max": 5},
  #   "status": "completed"
  # }
  ```
- Each step in the pipeline is independently testable and reusable
