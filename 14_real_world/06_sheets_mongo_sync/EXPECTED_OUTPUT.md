# Expected Output

## Running

```bash
python flow.py
```

## Requirements

This example requires external services configured:
- Google Sheets API credentials (service account JSON)
- MongoDB connection string
- `GOOGLE_CREDENTIALS_JSON` and `MONGODB_URI` environment variables
- Running Blazing infrastructure: `docker-compose up -d`

Start infrastructure: `docker-compose up -d`

## Output

```
INFO - BidirectionalSyncService - Sheets → MongoDB: syncing 25 rows
INFO - BidirectionalSyncService - MongoDB → Sheets: 3 records updated
INFO - BidirectionalSyncService - Conflict resolution: 2 records kept from Sheets (newer timestamp)
{"synced_to_mongo": 25, "synced_to_sheets": 3, "conflicts_resolved": 2}
```

## Notes

- Row count and sync direction depend on what has changed since the last sync run
- Last-write-wins conflict resolution uses the `updated_at` timestamp from each side
- Output values (counts, conflicts) will vary with live data
- Requires OAuth2 service account credentials for Google Sheets API access
