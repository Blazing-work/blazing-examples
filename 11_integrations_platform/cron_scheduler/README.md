# Cron & Periodic Scheduler

Register scheduled jobs in services using `SchedulerConnector`.

## Schedule Types

```python
from blazing.local import Cron, Period

Cron("0 9 * * *")       # standard cron expression — daily at 9am
Cron("0 8 * * 1")       # every Monday 8am
Cron("0 0 1 * *")       # first of month midnight
Period(minutes=5)       # every 5 minutes
Period(hours=6)         # every 6 hours
Period(seconds=30)      # every 30 seconds
```

## API

```python
from blazing.local import SchedulerConnector, Cron, Period

@app.service
class ReportService(BaseService):
    def __init__(self, connector_instances=None):
        super().__init__(connector_instances)
        self.scheduler = connector_instances.get("scheduler")

    async def setup(self):
        await self.scheduler.register_job(
            job_id="daily-report",
            schedule=Cron("0 9 * * *"),
            callback=self._generate_report,
            callback_kwargs={"report_type": "sales"},
        )

    async def _generate_report(self, report_type: str) -> dict:
        ...
```

## Operations

| Method | Description |
|--------|-------------|
| `register_job(job_id, schedule, callback, callback_kwargs)` | Register a scheduled job |
| `trigger_job(job_id)` | Manually trigger a job immediately |
| `list_jobs()` | List all registered jobs |
| `get_job(job_id)` | Get a specific job |
| `cancel_job(job_id)` | Remove a job |

## Running

The local demo uses `LocalSchedulerService` and runs without Docker:

```bash
python flow.py
```

Full deployment requires `docker-compose up -d` and `app.publish()`.
