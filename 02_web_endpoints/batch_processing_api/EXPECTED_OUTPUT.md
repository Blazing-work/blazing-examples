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
- Demonstrates concurrent batch processing using asyncio.gather
- Example request:
  ```bash
  curl -X POST http://localhost:8080/batch/users \
    -H "Content-Type: application/json" \
    -d '{"user_ids": [1, 2, 3], "multiplier": 1.5}'
  # Response: {"processed_count": 3, "results": [{"user_id": 1, "name": "User 1", "original_score": 10, "final_score": 15}, ...]}
  ```
- Each user fetch simulates 0.5s database query
- All users are fetched and processed in parallel
