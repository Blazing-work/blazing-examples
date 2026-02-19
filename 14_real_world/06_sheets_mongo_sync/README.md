# Google Sheets ↔ MongoDB Bidirectional Sync

Syncs data between Google Sheets and MongoDB with last-write-wins conflict resolution.

## Patterns

- Bidirectional sync: Sheets→MongoDB then MongoDB→Sheets
- `_synced_at` timestamp-based conflict resolution
- Idempotent upserts with `$set` operator
- Sequential two-phase sync (Sheets first, then Mongo)

## Setup

Requires:
- `google_sheets` connector (OAuth2 or service account)
- `mongodb` connector

Sheet must have headers in row 1, including the key field and `_synced_at` column.

## Endpoints

- `POST /sync` — bidirectional sync
- `POST /sync/sheets-to-mongo` — one-way
- `POST /sync/mongo-to-sheets` — one-way
