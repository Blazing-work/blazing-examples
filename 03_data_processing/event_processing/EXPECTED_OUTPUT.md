# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Processing event: {'id': 'evt_001', 'event_type': 'page_view', 'user_id': 123, 'timestamp': '2025-12-10T10:00:00Z', 'page': '/products'}
Result: {'stored': True, 'event_id': 'evt_001'}
```

## Notes

- Event is validated, enriched with user data, and stored
- Sample event demonstrates page view tracking
- Enrichment adds user_name and user_email based on user_id
- In production, would query actual user database and store to analytics database
- Successfully processed events return stored: True
- Invalid events (missing required fields) would raise ValueError
