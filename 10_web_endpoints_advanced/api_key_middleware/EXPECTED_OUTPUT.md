# Expected Output

## Running

```bash
python flow.py
```

## Output

```
INFO:     Started server process [{pid}]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

## Notes

- This example starts a long-running uvicorn server — it does not exit on its own
- Press CTRL+C to stop the server
- After startup, test the protected endpoint:
  - `curl -X POST http://localhost:8080/blazing/square -H "x-api-key: dev-key" -d '{"value": 4}'`
  - Without the API key header, the server returns `{"detail": "unauthorized"}` with status 401
- The API key defaults to `dev-key` (set `BLAZING_API_KEY` env var to override)
