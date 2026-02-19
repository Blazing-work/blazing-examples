#!/usr/bin/env python3
"""
Google Sheets ↔ MongoDB Bidirectional Sync Example

Syncs data between Google Sheets and MongoDB with last-write-wins conflict resolution.
Demonstrates: Bidirectional sync, timestamp-based conflict resolution, idempotent upserts.
"""
import logging
import os
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

from blazing import Blazing, BaseService

app = Blazing(
    api_url=os.getenv("BLAZING_API_URL", "http://localhost:8000"),
    api_token=os.getenv("BLAZING_API_TOKEN", "demo-token-placeholder")
)

logger = logging.getLogger(__name__)


@app.service(egress=["sheets.googleapis.com", "oauth2.googleapis.com"])
class BidirectionalSyncService(BaseService):
    """Service for bidirectional Google Sheets ↔ MongoDB synchronization."""

    def __init__(self, connector_instances=None):
        super().__init__(connector_instances)
        self.sheets = connector_instances.get('google_sheets') if connector_instances else None
        self.mongo = connector_instances.get('mongodb') if connector_instances else None

        if not self.sheets:
            raise ValueError("GoogleSheetsConnector required in connector_instances")
        if not self.mongo:
            raise ValueError("MongoDBConnector required in connector_instances")

    def _is_newer(self, timestamp_a: Optional[str], timestamp_b: Optional[str]) -> bool:
        """
        Compare timestamps for last-write-wins conflict resolution.

        Returns True if A is newer than B (or B is None), False otherwise.
        """
        if not timestamp_b:
            return True
        if not timestamp_a:
            return False

        try:
            dt_a = datetime.fromisoformat(timestamp_a.replace('Z', '+00:00'))
            dt_b = datetime.fromisoformat(timestamp_b.replace('Z', '+00:00'))
            return dt_a > dt_b
        except (ValueError, AttributeError) as e:
            logger.warning(f"Failed to parse timestamps: {e}")
            return False

    def _now_iso(self) -> str:
        """Get current UTC timestamp as ISO 8601 string."""
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    async def sync_sheets_to_mongo(
        self,
        spreadsheet_id: str,
        sheet_name: str,
        collection: str,
        key_field: str = "_id",
        database: Optional[str] = None
    ) -> Dict[str, int]:
        """
        Sync Google Sheets data to MongoDB with last-write-wins.

        Reads all rows from Google Sheets, compares timestamps with MongoDB,
        and upserts records that are newer.

        Sheet must have headers in first row, including key_field and _synced_at columns.

        Returns:
            Dict with inserted, updated, unchanged counts
        """
        rows = await self.sheets.read_rows(spreadsheet_id, worksheet=sheet_name)

        if not rows or len(rows) < 2:
            logger.info("No data in Google Sheets")
            return {"inserted": 0, "updated": 0, "unchanged": 0}

        headers = rows[0]
        data_rows = rows[1:]

        if key_field not in headers:
            raise ValueError(f"Key field '{key_field}' not found in sheet headers: {headers}")
        if "_synced_at" not in headers:
            raise ValueError("Sheet must have '_synced_at' column for timestamp-based conflict resolution")

        key_idx = headers.index(key_field)

        inserted = 0
        updated = 0
        unchanged = 0

        for row in data_rows:
            if len(row) <= key_idx or not row[key_idx]:
                continue

            doc = {}
            for i, header in enumerate(headers):
                doc[header] = row[i] if i < len(row) else ""

            key_value = doc[key_field]
            sheet_timestamp = doc.get("_synced_at", "")
            doc["_source"] = "google_sheets"

            existing = await self.mongo.find(
                collection,
                filter={key_field: key_value},
                limit=1,
                database=database
            )

            if not existing:
                doc["_synced_at"] = self._now_iso()
                await self.mongo.insert(collection, doc, database=database)
                inserted += 1
                logger.info(f"Inserted new record: {key_field}={key_value}")
            else:
                mongo_timestamp = existing[0].get("_synced_at", "")

                if self._is_newer(sheet_timestamp, mongo_timestamp):
                    doc["_synced_at"] = self._now_iso()
                    await self.mongo.update(
                        collection,
                        filter={key_field: key_value},
                        update={"$set": doc},
                        upsert=True,
                        database=database
                    )
                    updated += 1
                    logger.info(f"Updated record (sheet newer): {key_field}={key_value}")
                else:
                    unchanged += 1
                    logger.debug(f"Skipped record (mongo newer): {key_field}={key_value}")

        return {"inserted": inserted, "updated": updated, "unchanged": unchanged}

    async def sync_mongo_to_sheets(
        self,
        spreadsheet_id: str,
        sheet_name: str,
        collection: str,
        key_field: str = "_id",
        database: Optional[str] = None,
        limit: int = 10000  # Google Sheets 10M cell limit
    ) -> Dict[str, int]:
        """
        Sync MongoDB data to Google Sheets with last-write-wins.

        Returns:
            Dict with inserted, updated, unchanged counts
        """
        docs = await self.mongo.find(collection, filter={}, limit=limit, database=database)

        if not docs:
            logger.info("No data in MongoDB")
            return {"inserted": 0, "updated": 0, "unchanged": 0}

        rows = await self.sheets.read_rows(spreadsheet_id, worksheet=sheet_name)

        all_keys = set()
        for doc in docs:
            all_keys.update(doc.keys())
        all_keys.add(key_field)
        all_keys.add("_synced_at")

        headers = [key_field] + sorted([k for k in all_keys if k != key_field])

        # Build index of existing sheet rows by key_field
        sheet_index = {}
        if rows and len(rows) > 1:
            existing_headers = rows[0]
            if key_field in existing_headers:
                key_idx = existing_headers.index(key_field)
                synced_at_idx = existing_headers.index("_synced_at") if "_synced_at" in existing_headers else None

                for row_num, row in enumerate(rows[1:], start=2):
                    if len(row) > key_idx and row[key_idx]:
                        key_value = row[key_idx]
                        sheet_timestamp = row[synced_at_idx] if synced_at_idx and len(row) > synced_at_idx else ""
                        sheet_index[key_value] = {
                            "row_num": row_num,
                            "timestamp": sheet_timestamp
                        }

        rows_to_write = [headers]
        inserted = 0
        updated = 0
        unchanged = 0

        for doc in docs:
            key_value = str(doc.get(key_field, ""))
            mongo_timestamp = doc.get("_synced_at", "")

            row = [str(doc.get(header, "") or "") for header in headers]

            if key_value in sheet_index:
                sheet_info = sheet_index[key_value]
                sheet_timestamp = sheet_info["timestamp"]

                if self._is_newer(mongo_timestamp, sheet_timestamp):
                    rows_to_write.append(row)
                    updated += 1
                else:
                    unchanged += 1
            else:
                rows_to_write.append(row)
                inserted += 1

        if len(rows_to_write) > 1:
            await self.sheets.write_cells(
                spreadsheet_id,
                worksheet=sheet_name,
                range="A1",
                values=rows_to_write
            )

        return {"inserted": inserted, "updated": updated, "unchanged": unchanged}

    async def sync_bidirectional(
        self,
        spreadsheet_id: str,
        sheet_name: str,
        collection: str,
        key_field: str = "_id",
        database: Optional[str] = None
    ) -> Dict[str, Dict[str, int]]:
        """
        Perform bidirectional sync: Sheets→MongoDB then MongoDB→Sheets.

        Returns:
            Dict with sheets_to_mongo and mongo_to_sheets result dicts
        """
        sheets_to_mongo = await self.sync_sheets_to_mongo(
            spreadsheet_id, sheet_name, collection, key_field, database
        )

        mongo_to_sheets = await self.sync_mongo_to_sheets(
            spreadsheet_id, sheet_name, collection, key_field, database
        )

        return {
            "sheets_to_mongo": sheets_to_mongo,
            "mongo_to_sheets": mongo_to_sheets
        }


@app.endpoint.post("/sync")
async def sync_bidirectional_endpoint(request, services=None):
    """
    Perform bidirectional sync between Google Sheets and MongoDB.

    Request body:
    {
        "spreadsheet_id": "1abc...",
        "sheet_name": "Sheet1",
        "collection": "users",
        "key_field": "_id",
        "database": "mydb"  // optional
    }

    Note: Sheet must have headers in first row, including key_field and _synced_at columns.
    """
    body = await request.json()

    spreadsheet_id = body.get("spreadsheet_id")
    sheet_name = body.get("sheet_name")
    collection = body.get("collection")
    key_field = body.get("key_field", "_id")
    database = body.get("database")

    if not spreadsheet_id:
        return {"error": "Missing 'spreadsheet_id' field"}, 400
    if not sheet_name:
        return {"error": "Missing 'sheet_name' field"}, 400
    if not collection:
        return {"error": "Missing 'collection' field"}, 400

    sync_service = services['BidirectionalSyncService']

    result = await sync_service.sync_bidirectional(
        spreadsheet_id=spreadsheet_id,
        sheet_name=sheet_name,
        collection=collection,
        key_field=key_field,
        database=database
    )

    return result


@app.endpoint.post("/sync/sheets-to-mongo")
async def sync_sheets_to_mongo_endpoint(request, services=None):
    """One-way sync: Google Sheets → MongoDB."""
    body = await request.json()

    spreadsheet_id = body.get("spreadsheet_id")
    sheet_name = body.get("sheet_name")
    collection = body.get("collection")

    if not spreadsheet_id or not sheet_name or not collection:
        return {"error": "Missing required fields: spreadsheet_id, sheet_name, collection"}, 400

    sync_service = services['BidirectionalSyncService']
    result = await sync_service.sync_sheets_to_mongo(
        spreadsheet_id=spreadsheet_id,
        sheet_name=sheet_name,
        collection=collection,
        key_field=body.get("key_field", "_id"),
        database=body.get("database")
    )
    return result


@app.endpoint.post("/sync/mongo-to-sheets")
async def sync_mongo_to_sheets_endpoint(request, services=None):
    """One-way sync: MongoDB → Google Sheets."""
    body = await request.json()

    spreadsheet_id = body.get("spreadsheet_id")
    sheet_name = body.get("sheet_name")
    collection = body.get("collection")

    if not spreadsheet_id or not sheet_name or not collection:
        return {"error": "Missing required fields: spreadsheet_id, sheet_name, collection"}, 400

    sync_service = services['BidirectionalSyncService']
    result = await sync_service.sync_mongo_to_sheets(
        spreadsheet_id=spreadsheet_id,
        sheet_name=sheet_name,
        collection=collection,
        key_field=body.get("key_field", "_id"),
        database=body.get("database")
    )
    return result


if __name__ == "__main__":
    import asyncio
    asyncio.run(app.publish())
