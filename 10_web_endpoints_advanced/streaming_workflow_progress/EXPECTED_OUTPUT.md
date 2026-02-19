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
- Test with streaming client: `curl -N -X POST http://localhost:8080/process -d '{"items": [1, 2, 3]}'`
- Streaming response emits progress events like `{"step": 1, "total": 3, "message": "Processed 1/3"}` then the final result `{"results": [2, 4, 6]}`
- Uses `progress()` and `log()` from `blazing.endpoints.streaming`
