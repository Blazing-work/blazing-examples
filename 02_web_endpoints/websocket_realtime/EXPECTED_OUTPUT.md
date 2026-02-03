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
- Demonstrates WebSocket support for real-time progress updates
- WebSocket endpoint: `ws://localhost:8080/process/ws`
- Example usage:
  ```bash
  # Start the workflow via WebSocket and receive real-time updates
  # Use a WebSocket client to connect to ws://localhost:8080/process/ws
  # Send: {"num_batches": 3}
  # Receive: Real-time progress updates as each batch completes
  ```
- Each batch simulates 2 seconds of processing
- Progress updates are streamed as the workflow executes
- Final response includes all batch results
