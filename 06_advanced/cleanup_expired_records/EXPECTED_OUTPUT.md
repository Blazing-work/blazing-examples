# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Running session cleanup job (sessions older than 30 days)...
  [DB] Deleted session: sess_001
  [DB] Deleted session: sess_002
  [DB] Deleted session: sess_004

Cleanup Results:
  Cutoff Date: [current date - 30 days in ISO format]
  Sessions Deleted: 3
```

## Notes

- Cutoff date is calculated dynamically (30 days before current date)
- Simulated database contains 5 sessions, 3 of which are older than 30 days
- Sessions sess_001, sess_002, and sess_004 have timestamps from January 2024 (expired)
- Sessions sess_003 and sess_005 have timestamps from December 2024 (not expired)
- Uses simulated in-memory database for demonstration
- Demonstrates scheduled cleanup workflow pattern with date-based filtering
