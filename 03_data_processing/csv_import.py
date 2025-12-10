"""
# CSV Import Pipeline

Download, parse, validate, and import CSV files from cloud storage.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Advanced
- **Time**: 30 min
- **Tags**: csv, file-processing, import, validation

## Description

Download, parse, validate, and import CSV files from cloud storage.

## What you'll learn

- CSV parsing with Python csv module
- File validation patterns
- Bulk import strategies
"""

import csv
import io
from blazing.base import BaseService

from blazing import Blazing

async def main():
    app = Blazing(api_url="http://localhost:8000", api_token="your-token")

    @app.service
    class FileStorageService(BaseService):
        def __init__(self, connectors):
            self._s3 = connectors.get('s3')
        async def download(self, file_key: str) -> bytes:
            """Download file from S3."""
            return await self._s3.get_object(file_key)
        async def upload(self, file_key: str, data: bytes):
            """Upload file to S3."""
            await self._s3.put_object(file_key, data)
    @app.step
    async def parse_csv(file_content: bytes, services=None):
        """Parse CSV file."""
        content = file_content.decode('utf-8')
        reader = csv.DictReader(io.StringIO(content))
        rows = list(reader)
        return {"rows": rows, "count": len(rows)}
    @app.step
    async def validate_csv_rows(rows: list, services=None):
        """Validate CSV rows."""
        valid_rows = []
        errors = []
        for idx, row in enumerate(rows):
            try:
                # Validate required fields
                if not row.get('email') or not row.get('name'):
                    raise ValueError("Missing required fields")
                valid_rows.append(row)
            except ValueError as e:
                errors.append({"row": idx, "error": str(e)})
        return {"valid": valid_rows, "errors": errors}
    @app.step
    async def import_csv_rows(rows: list, services=None):
        """Import validated rows to database."""
        imported = []
        for row in rows:
            user_id = await services['UserDatabase'].create_user(row['name'], row['email'])
            imported.append(user_id)
        return {"imported": len(imported), "ids": imported}
    @app.workflow
    async def import_csv_file(file_key: str, services=None):
        """Import CSV file from S3."""
        # Download file
        file_content = await services['FileStorageService'].download(file_key)
        # Parse CSV
        parsed = await parse_csv(file_content, services=services)
        # Validate rows
        validated = await validate_csv_rows(parsed['rows'], services=services)
        # Import valid rows
        result = await import_csv_rows(validated['valid'], services=services)
        return {
            "file": file_key,
            "total_rows": parsed['count'],
            "imported": result['imported'],
            "errors": len(validated['errors'])
        }
    await app.publish()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
