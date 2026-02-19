"""
Cron & Periodic Job Scheduling Example for Blazing

Services can register scheduled jobs using SchedulerConnector.
Jobs fire on a cron expression or a fixed interval.

Schedule types:
  Cron("0 9 * * *")         — standard cron expression
  Period(hours=1)            — fixed interval (seconds/minutes/hours/days)

Key operations:
  scheduler.register_job(job_id, schedule, callback, callback_kwargs)
  scheduler.trigger_job(job_id)          — immediate manual trigger
  scheduler.list_jobs()                  — inspect registered jobs
  scheduler.get_job(job_id)              — get a specific job
  scheduler.cancel_job(job_id)           — remove a job

Requires: docker-compose up -d
"""

import os
from datetime import datetime, timezone
from typing import Any, Dict, List

from blazing import Blazing, BaseService
from blazing.local import (
    LocalStack,
    LocalSchedulerService,
    SchedulerConnector,
    Cron,
    Period,
)

app = Blazing(
    api_url=os.getenv("BLAZING_API_URL", "http://localhost:8000"),
    api_token=os.getenv("BLAZING_API_TOKEN", "demo-token-placeholder"),
)


# ── Pattern 1: Report Service (cron expressions) ──────────────────────────────

@app.service
class ReportService(BaseService):
    """Service that generates reports on a schedule."""

    def __init__(self, connector_instances=None):
        super().__init__(connector_instances)
        self.scheduler = (connector_instances or {}).get("scheduler")
        self.reports: List[Dict] = []

    async def setup_schedules(self):
        """Register all report schedules at startup."""
        # Daily at 9am
        await self.scheduler.register_job(
            job_id="daily-sales-report",
            schedule=Cron("0 9 * * *"),
            callback=self._generate_report,
            callback_kwargs={"report_type": "sales"},
        )

        # Every Monday at 8am
        await self.scheduler.register_job(
            job_id="weekly-summary",
            schedule=Cron("0 8 * * 1"),
            callback=self._generate_report,
            callback_kwargs={"report_type": "weekly_summary"},
        )

        # First day of each month at midnight
        await self.scheduler.register_job(
            job_id="monthly-invoice",
            schedule=Cron("0 0 1 * *"),
            callback=self._generate_report,
            callback_kwargs={"report_type": "monthly_invoice"},
        )

    async def _generate_report(self, report_type: str) -> Dict:
        report = {
            "type": report_type,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        self.reports.append(report)
        return report

    async def trigger_report(self, report_type: str):
        """Manually trigger a specific report."""
        return await self.scheduler.trigger_job(f"daily-{report_type}")

    async def scheduled_jobs(self):
        return await self.scheduler.list_jobs()


# ── Pattern 2: Data Sync Service (fixed intervals) ────────────────────────────

@app.service
class DataSyncService(BaseService):
    """Service that syncs data sources on fixed intervals."""

    def __init__(self, connector_instances=None):
        super().__init__(connector_instances)
        self.scheduler = (connector_instances or {}).get("scheduler")

    async def register_sync(self, source: str, interval_minutes: int = 30):
        """Register a periodic sync for a data source."""
        await self.scheduler.register_job(
            job_id=f"sync-{source}",
            schedule=Period(minutes=interval_minutes),
            callback=self._sync,
            callback_kwargs={"source": source},
        )

    async def _sync(self, source: str) -> Dict:
        return {
            "source": source,
            "synced_at": datetime.now(timezone.utc).isoformat(),
            "records_synced": 100,  # In production: actual sync count
        }

    async def force_sync(self, source: str):
        """Immediately trigger a sync outside the regular schedule."""
        return await self.scheduler.trigger_job(f"sync-{source}")


# ── Pattern 3: Maintenance Service (multiple intervals) ───────────────────────

@app.service
class MaintenanceService(BaseService):
    """Service that runs cleanup and health checks on a schedule."""

    def __init__(self, connector_instances=None):
        super().__init__(connector_instances)
        self.scheduler = (connector_instances or {}).get("scheduler")

    async def setup_maintenance(self):
        """Register all maintenance jobs."""
        await self.scheduler.register_job(
            job_id="cleanup-logs",
            schedule=Cron("0 0 * * *"),       # daily at midnight
            callback=self._cleanup_logs,
        )
        await self.scheduler.register_job(
            job_id="cleanup-temp",
            schedule=Cron("0 3 * * 0"),       # weekly Sunday 3am
            callback=self._cleanup_temp,
        )
        await self.scheduler.register_job(
            job_id="health-check",
            schedule=Period(minutes=5),        # every 5 minutes
            callback=self._health_check,
        )
        await self.scheduler.register_job(
            job_id="cache-refresh",
            schedule=Period(hours=6),          # every 6 hours
            callback=self._refresh_cache,
        )

    async def _cleanup_logs(self):
        return {"action": "cleanup_logs", "freed_mb": 42}

    async def _cleanup_temp(self):
        return {"action": "cleanup_temp", "files_removed": 137}

    async def _health_check(self):
        return {"status": "healthy", "checked_at": datetime.now(timezone.utc).isoformat()}

    async def _refresh_cache(self):
        return {"action": "cache_refresh", "keys_refreshed": 256}


# ── Standalone demo (no Docker needed for structure, Docker needed for execution) ──

async def demo_scheduler():
    """Demonstrate scheduler API locally with LocalStack."""
    print("=== Cron & Periodic Scheduler Demo ===")
    print()

    svc_backend = LocalSchedulerService(tick_interval=0.05)
    await svc_backend.start()

    connector = SchedulerConnector(service=svc_backend)
    await connector.connect()

    # Register a report service
    report_svc = ReportService(connector_instances={"scheduler": connector})
    await report_svc.setup_schedules()

    jobs = await report_svc.scheduled_jobs()
    print(f"Registered {len(jobs)} scheduled jobs:")
    for job in jobs:
        print(f"  {job.job_id:<30} {job.schedule}")
    print()

    # Manual trigger
    await connector.trigger_job("daily-sales-report")
    print(f"Reports generated after trigger: {len(report_svc.reports)}")

    # Register data syncs
    sync_svc = DataSyncService(connector_instances={"scheduler": connector})
    await sync_svc.register_sync("postgres", interval_minutes=15)
    await sync_svc.register_sync("s3",       interval_minutes=60)

    result = await sync_svc.force_sync("postgres")
    print(f"Forced sync result: {result}")
    print()

    print("Schedule expressions:")
    print("  Cron('0 9 * * *')      → daily at 9am")
    print("  Cron('0 8 * * 1')      → every Monday 8am")
    print("  Cron('0 0 1 * *')      → first of month midnight")
    print("  Period(minutes=5)      → every 5 minutes")
    print("  Period(hours=6)        → every 6 hours")

    await connector.disconnect()
    await svc_backend.stop()


if __name__ == "__main__":
    import asyncio
    asyncio.run(demo_scheduler())
