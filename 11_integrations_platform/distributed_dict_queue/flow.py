"""
Distributed Dict & Queue Example for Blazing

DictConnector and QueueConnector provide shared state and message passing
between service instances and workflow steps — across workers, deployments,
and tenants.

  DictConnector  — shared key-value store (like Redis hash, survives restarts)
  QueueConnector — async FIFO queue for producer-consumer patterns

Both connectors are injected into services by Blazing. Multiple service
instances share the same underlying data, enabling coordination.

Patterns shown:
  1. Shared counter with DictConnector (idempotent counter across workers)
  2. Producer-consumer pipeline with QueueConnector
  3. Job coordination: workers write results to shared dict

Requires: docker-compose up -d
"""

import asyncio
import os

from blazing import Blazing, BaseService

app = Blazing(
    api_url=os.getenv("BLAZING_API_URL", "http://localhost:8000"),
    api_token=os.getenv("BLAZING_API_TOKEN", "demo-token-placeholder"),
)


# ── Pattern 1: Shared State with DictConnector ────────────────────────────────

@app.service
class MetricsService(BaseService):
    """
    Service that tracks metrics in a shared dict.

    Multiple worker instances all write to the same dict — no Redis
    client required in user code.
    """

    def __init__(self, connector_instances=None):
        super().__init__(connector_instances)
        self.state = (connector_instances or {}).get("metrics-dict")

    async def increment(self, metric: str, by: int = 1) -> int:
        """Atomically increment a metric counter."""
        current = await self.state.get(metric) or 0
        new_value = current + by
        await self.state.put(metric, new_value)
        return new_value

    async def record(self, metric: str, value: float):
        """Record a metric value."""
        await self.state.put(metric, value)

    async def snapshot(self) -> dict:
        """Return all current metric values."""
        return await self.state.get_all()


# ── Pattern 2: Job Queue with QueueConnector ──────────────────────────────────

@app.service
class JobQueueService(BaseService):
    """
    Producer-consumer job queue.

    Producers submit jobs; consumer workers pick them up.
    """

    def __init__(self, connector_instances=None):
        super().__init__(connector_instances)
        self.queue = (connector_instances or {}).get("job-queue")

    async def submit(self, job: dict) -> int:
        """Submit a job to the queue. Returns current queue depth."""
        await self.queue.put(job)
        return await self.queue.size()

    async def claim_next(self) -> dict:
        """Claim the next available job (blocks until one arrives)."""
        return await self.queue.get()

    async def try_claim(self) -> dict:
        """Non-blocking: claim a job if one is available, else None."""
        return await self.queue.get_nowait()

    async def depth(self) -> int:
        """Return number of pending jobs."""
        return await self.queue.size()


# ── Pattern 3: Result Aggregation ─────────────────────────────────────────────

@app.service
class ResultsService(BaseService):
    """
    Aggregates results written by parallel workers into a shared dict.
    """

    def __init__(self, connector_instances=None):
        super().__init__(connector_instances)
        self.results = (connector_instances or {}).get("results-dict")

    async def write_result(self, worker_id: str, result: dict):
        """Write a worker's result to the shared dict."""
        await self.results.put(f"worker:{worker_id}", result)

    async def all_results(self) -> dict:
        """Read all worker results."""
        return await self.results.get_all()

    async def is_complete(self, expected_workers: int) -> bool:
        """Check if all expected workers have written their results."""
        all_res = await self.all_results()
        return len([k for k in all_res if k.startswith("worker:")]) >= expected_workers


# ── Workflows ─────────────────────────────────────────────────────────────────

@app.step
async def process_job(job: dict, services=None) -> dict:
    """Process a single job and record timing metrics."""
    metrics = services.get("MetricsService")
    await metrics.increment("jobs_processed")
    return {"job_id": job["id"], "result": job["payload"].upper(), "status": "done"}


@app.workflow
async def batch_processing_pipeline(jobs: list, services=None) -> dict:
    """
    Submit jobs to queue, process them, collect results.

    Demonstrates Dict + Queue coordination in a real workflow.
    """
    job_queue = services.get("JobQueueService")
    metrics = services.get("MetricsService")

    # Submit all jobs
    for job in jobs:
        await job_queue.submit(job)

    await metrics.record("batch_size", len(jobs))

    # Process all jobs
    results = []
    for _ in jobs:
        job = await job_queue.claim_next()
        result = await process_job(job)
        results.append(result)

    stats = await metrics.snapshot()
    return {"results": results, "metrics": stats}


# ── Main ──────────────────────────────────────────────────────────────────────

async def main():
    print("Distributed Dict & Queue Patterns:")
    print()
    print("  DictConnector  → shared key-value store across all workers")
    print("  QueueConnector → async FIFO queue for producer-consumer")
    print()
    print("  dict.put(key, value)    — write")
    print("  dict.get(key)           — read")
    print("  dict.get_all()          — dump all keys")
    print()
    print("  queue.put(item)         — enqueue")
    print("  queue.get()             — dequeue (blocking)")
    print("  queue.get_nowait()      — dequeue (non-blocking, returns None)")
    print("  queue.size()            — current depth")
    print()

    await app.publish()

    jobs = [{"id": i, "payload": f"task_{i}"} for i in range(5)]
    result = await app.run(batch_processing_pipeline, args=(jobs,))
    print(f"Processed {len(result['results'])} jobs")
    print(f"Metrics: {result['metrics']}")


if __name__ == "__main__":
    asyncio.run(main())
