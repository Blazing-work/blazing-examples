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
- Test the Blazing endpoint: `curl -X POST http://localhost:8080/blazing/double -d '{"value": 5}'` → `{"value": 10}`
- Test the sidecar SSE stream: `curl -N http://localhost:8080/stream` → emits `data: tick 0` through `data: tick 4` at 0.5s intervals
- Demonstrates running a Blazing ASGI app alongside a custom FastAPI SSE streaming route
