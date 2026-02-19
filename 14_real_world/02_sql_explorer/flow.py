#!/usr/bin/env python3
"""
SQL Explorer Example using DuckDB

Demonstrates ad-hoc SQL analytics via HTTP endpoints backed by DuckDB.
DuckDB provides OLAP-optimized query performance with support for SQLite, CSV, Parquet,
and JSON data sources.

Key features:
- Read-only mode by default (no DDL/DML allowed)
- SQL injection protection via parameterized queries
- Query timeout protection (30 seconds max)
- Cross-format querying (SQLite, CSV, Parquet)
- HTTP endpoints for query execution and schema discovery
"""

import asyncio
import duckdb
import logging
import os
import sys
import time
from typing import Any, Dict, List, Optional

from blazing import Blazing, BaseService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# Initialize Blazing app
app = Blazing(
    api_url=os.getenv("BLAZING_API_URL", "http://localhost:9000"),
    api_token=os.getenv("BLAZING_API_TOKEN", "demo-token")
)


@app.service()  # No egress needed - DuckDB is local/embedded
class SQLExplorerService(BaseService):
    """
    SQL query service backed by DuckDB.

    Provides read-only SQL query capabilities over SQLite, CSV, Parquet, and JSON files.
    Enforces safety through DDL rejection, parameterized queries, and timeout protection.
    """

    # DDL/DML keywords that are rejected in read-only mode
    FORBIDDEN_KEYWORDS = {
        'CREATE', 'DROP', 'ALTER', 'TRUNCATE',
        'INSERT', 'UPDATE', 'DELETE', 'REPLACE',
        'GRANT', 'REVOKE', 'COMMIT', 'ROLLBACK'
    }

    def __init__(self, connector_instances=None):
        """Initialize DuckDB connection with sample database attached."""
        super().__init__(connector_instances)

        # Create in-memory DuckDB connection
        self.conn = duckdb.connect(':memory:')

        # Get database path from environment or use default
        self.db_path = os.getenv("DB_PATH", "sample.db")

        # Attach SQLite database if it exists
        if os.path.exists(self.db_path):
            try:
                # Attach the SQLite database as 'sample' schema
                self.conn.execute(f"ATTACH '{self.db_path}' AS sample (TYPE SQLITE)")
                logger.info(f"Attached SQLite database: {self.db_path}")
            except Exception as e:
                logger.error(f"Failed to attach database {self.db_path}: {e}")
                raise
        else:
            logger.warning(f"Database file not found: {self.db_path}")

    async def connect(self):
        """Log available tables on connection."""
        try:
            tables = self.conn.execute("SHOW TABLES").fetchall()
            logger.info(f"Available tables: {tables}")
        except Exception as e:
            logger.error(f"Error showing tables: {e}")

    def _validate_sql(self, sql: str) -> None:
        """
        Validate SQL query for safety in read-only mode.

        Raises:
            ValueError: If SQL contains forbidden operations
        """
        sql_upper = sql.upper()

        for keyword in self.FORBIDDEN_KEYWORDS:
            if keyword in sql_upper:
                raise ValueError(
                    f"DDL/DML statements not allowed in read-only mode: {keyword}"
                )

        # Prevent statement stacking (SQL injection protection)
        statements = [s.strip() for s in sql.split(';') if s.strip()]
        if len(statements) > 1:
            raise ValueError(
                "Multiple statements not allowed (SQL injection protection)"
            )

    async def query(
        self,
        sql: str,
        params: Optional[List[Any]] = None,
        timeout_seconds: int = 30
    ) -> Dict[str, Any]:
        """
        Execute SQL query with safety checks and timeout protection.

        Args:
            sql: SQL query string
            params: Optional list of parameters for parameterized queries
            timeout_seconds: Maximum query execution time (default 30s)

        Returns:
            Dictionary with columns, rows, row_count, and duration_ms
        """
        self._validate_sql(sql)

        start_time = time.time()

        try:
            rows, description = await asyncio.wait_for(
                asyncio.get_event_loop().run_in_executor(None, lambda: (
                    self.conn.execute(sql, params).fetchall() if params
                    else self.conn.execute(sql).fetchall(),
                    self.conn.execute(sql, params).description if params
                    else self.conn.execute(sql).description
                )),
                timeout=timeout_seconds
            )

            columns = [desc[0] for desc in description]

            rows_as_dicts = [
                {col: val for col, val in zip(columns, row)}
                for row in rows
            ]

            duration_ms = int((time.time() - start_time) * 1000)

            return {
                "columns": columns,
                "rows": rows_as_dicts,
                "row_count": len(rows),
                "duration_ms": duration_ms
            }

        except asyncio.TimeoutError:
            logger.error(f"Query timed out after {timeout_seconds}s: {sql[:100]}")
            raise asyncio.TimeoutError(
                f"Query execution exceeded {timeout_seconds} second timeout"
            )
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise

    async def get_tables(self) -> List[Dict[str, str]]:
        """Get list of available tables with basic info."""
        result = self.conn.execute("""
            SELECT table_schema, table_name, table_type
            FROM information_schema.tables
            WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
            ORDER BY table_schema, table_name
        """).fetchall()

        return [
            {"schema": row[0], "name": row[1], "type": row[2]}
            for row in result
        ]

    async def get_schema(self, table_name: str) -> List[Dict[str, str]]:
        """Get column schema for a specific table."""
        result = self.conn.execute(f"DESCRIBE {table_name}").fetchall()

        return [
            {
                "column": row[0],
                "type": row[1],
                "nullable": row[2] == 'YES',
                "key": row[3] if len(row) > 3 else None,
                "default": row[4] if len(row) > 4 else None
            }
            for row in result
        ]


@app.endpoint.post("/query")
async def query_endpoint(request, services=None):
    """
    Execute SQL query and return results.

    Request body:
        {"sql": "SELECT * FROM sample.users WHERE id = ?", "params": [1]}

    Response:
        {"columns": [...], "rows": [...], "row_count": 5, "duration_ms": 12}
    """
    try:
        body = await request.json()
        sql = body.get("sql")
        params = body.get("params", None)

        if not sql:
            return {"error": "Missing 'sql' field in request body"}, 400

        explorer = services['SQLExplorerService']
        result = await explorer.query(sql, params)
        return result, 200

    except ValueError as e:
        return {"error": str(e)}, 400
    except asyncio.TimeoutError as e:
        return {"error": str(e)}, 408
    except Exception as e:
        logger.error(f"Query endpoint error: {e}")
        return {"error": f"Query execution failed: {str(e)}"}, 500


@app.endpoint.get("/tables")
async def tables_endpoint(request, services=None):
    """List all available tables."""
    try:
        explorer = services['SQLExplorerService']
        tables = await explorer.get_tables()
        return {"tables": tables}, 200
    except Exception as e:
        logger.error(f"Tables endpoint error: {e}")
        return {"error": f"Failed to list tables: {str(e)}"}, 500


@app.endpoint.get("/schema/{table_name}")
async def schema_endpoint(request, services=None):
    """Get column schema for a table."""
    try:
        table_name = request.path_params.get("table_name")
        if not table_name:
            return {"error": "Missing table_name in path"}, 400

        explorer = services['SQLExplorerService']
        schema = await explorer.get_schema(table_name)
        return {"table": table_name, "columns": schema}, 200
    except Exception as e:
        logger.error(f"Schema endpoint error: {e}")
        return {"error": f"Failed to get schema: {str(e)}"}, 500


@app.endpoint.get("/health")
async def health_endpoint(request, services=None):
    """Health check endpoint with DuckDB version info."""
    try:
        explorer = services['SQLExplorerService']
        version = explorer.conn.execute("SELECT version()").fetchone()[0]
        return {"status": "healthy", "duckdb_version": version}, 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "error": str(e)}, 503


if __name__ == "__main__":
    logger.info("Starting SQL Explorer service...")
    logger.info(f"Database path: {os.getenv('DB_PATH', 'sample.db')}")
    print("Available endpoints:", file=sys.stderr)
    print("  POST /query - Execute SQL queries", file=sys.stderr)
    print("  GET /tables - List available tables", file=sys.stderr)
    print("  GET /schema/{table} - Get table schema", file=sys.stderr)
    print("  GET /health - Health check", file=sys.stderr)
