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
- To test the endpoint:
  ```bash
  curl "http://localhost:8080/calculate?x=10&y=20"
  # Expected response: 30
  ```
- The `/calculate` endpoint adds two numbers (x + y)
