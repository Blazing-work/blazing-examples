# Expected Output

## Running

```bash
python flow.py
```

## Requirements

This example requires external services configured:
- `BLAZING_API_URL` and `BLAZING_API_TOKEN` for Blazing infrastructure
- A DuckDB-compatible data file (SQLite, CSV, Parquet, or JSON) to query

Start infrastructure: `docker-compose up -d`

## Output

```
INFO:     Started server process [{pid}]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## Notes

- This example starts a long-running uvicorn server — it does not exit on its own
- Press CTRL+C to stop the server
- Test a query: `curl -X POST http://localhost:8000/query -d '{"sql": "SELECT 42 AS answer"}'` → `{"columns": ["answer"], "rows": [[42]], "elapsed_ms": 1.2}`
- Read-only mode: DDL/DML queries (CREATE, INSERT, UPDATE, DROP) are rejected with status 400
