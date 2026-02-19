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
- Test the happy path: `curl -X POST http://localhost:8080/blazing/divide -d '{"x": 10, "y": 2}'` → `{"result": 5.0}`
- Test the error path: `curl -X POST http://localhost:8080/blazing/divide -d '{"x": 10, "y": 0}'` → `{"detail": "y must be non-zero"}` with status 400
