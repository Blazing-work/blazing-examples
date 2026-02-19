# SQL Explorer

Read-only SQL query API backed by DuckDB. Supports SQLite, CSV, Parquet, and JSON sources.

## Patterns

- `@app.service()` — no egress needed (DuckDB is local/embedded)
- SQL injection protection via DDL rejection + parameterized queries
- `asyncio.wait_for()` — query timeout enforcement (30s default)
- `run_in_executor()` — wraps sync DuckDB calls for async compatibility

## Setup

```bash
pip install duckdb
```

Set `DB_PATH` env var to point to a SQLite file, or queries run on in-memory DuckDB.

## Endpoints

- `POST /query` — execute SQL (read-only)
- `GET /tables` — list available tables
- `GET /schema/{table}` — get column schema
- `GET /health` — DuckDB version check
