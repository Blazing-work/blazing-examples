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
- Test with streaming client: `curl -N -X POST http://localhost:8080/sum -d '{"values": [1, 2, 3]}'`
- Streaming response emits progress events like `{"partial_sum": 1}`, `{"partial_sum": 3}`, `{"partial_sum": 6}` then the final result `{"sum": 6}`
- Uses `progress_bar()` and `send_data()` from `blazing.endpoints.streaming`
