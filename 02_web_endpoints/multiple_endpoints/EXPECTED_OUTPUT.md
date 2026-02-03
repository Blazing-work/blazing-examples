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
- Multiple API versions and endpoints available:
  - V1: `/v1/users/create`, `/v1/users/list`
  - V2: `/v2/users/create`, `/v2/users/list` (with enhanced features)
  - Admin: `/admin/stats`
- Example requests:
  ```bash
  # V1 endpoint
  curl -X POST "http://localhost:8080/v1/users/create?name=John&email=john@example.com"
  # Response: {"id": 1, "name": "John", "email": "john@example.com", "version": "v1"}

  # V2 endpoint with pagination
  curl "http://localhost:8080/v2/users/list?limit=20&offset=0"
  # Response: {"users": [], "count": 0, "limit": 20, "offset": 0, "version": "v2"}
  ```
