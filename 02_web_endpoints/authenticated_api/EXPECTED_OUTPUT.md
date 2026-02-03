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
- Three endpoints are available:
  - Public: `GET /health` (no auth required)
  - JWT-protected: `POST /secure/data` (requires JWT token)
  - API-key-protected: `GET /admin/stats` (requires API key)
- Example requests:
  ```bash
  # Public endpoint
  curl http://localhost:8080/health
  # Response: {"status": "healthy", "version": "1.0.0"}

  # Protected endpoint (requires Bearer token)
  curl -H "Authorization: Bearer secret-api-key" http://localhost:8080/admin/stats
  # Response: {"total_users": 1000, "active_jobs": 42}
  ```
