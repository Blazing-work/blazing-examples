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
- Test: `curl -X POST http://localhost:8080/blazing/square -d '{"value": 5}'` → `{"value": 25}`
- Demonstrates mounting the Blazing ASGI app as a sub-path (`/blazing`) of a FastAPI app
