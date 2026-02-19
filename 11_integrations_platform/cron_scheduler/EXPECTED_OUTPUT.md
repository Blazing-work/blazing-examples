# Expected Output

## Running

```bash
python flow.py
```

## Output

```
=== Cron & Periodic Scheduler Demo ===

Registered 3 scheduled jobs:
  daily-sales-report             Cron(0 9 * * *)
  weekly-summary                 Cron(0 8 * * 1)
  monthly-invoice                Cron(0 0 1 * *)

Reports generated after trigger: 1
Forced sync result: {'source': 'postgres', 'synced_at': '{timestamp}', 'records_synced': 100}

Schedule expressions:
  Cron('0 9 * * *')      → daily at 9am
  Cron('0 8 * * 1')      → every Monday 8am
  Cron('0 0 1 * *')      → first of month midnight
  Period(minutes=5)      → every 5 minutes
  Period(hours=6)        → every 6 hours
```

## Notes

- Runs locally without Docker — uses `LocalSchedulerService` (in-memory scheduler)
- `synced_at` timestamp will reflect the current UTC time when run
- The `Cron` and `Period` schedule expressions are printed using their string representations
- Full scheduler functionality (actual periodic firing) requires `docker-compose up -d`
