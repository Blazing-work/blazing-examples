"""
# Parallel Execution

Execute multiple tasks concurrently for 10x speedup.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Intermediate
- **Time**: 15 min
- **Tags**: concurrency, performance, parallel

## Recommendation

We recommend using the **async `Blazing` class** for the best performance and production readiness.
A sync version (`SyncBlazing`) is provided at the bottom for learning purposes only.

## Description

Learn how to execute multiple tasks in parallel to dramatically improve throughput.
This example shows you how to:
- Create batch tasks efficiently
- Achieve 4-10x speedup with parallelization
- Optimize for different workload sizes
- Monitor concurrency levels

## What you'll learn

- Parallel task execution patterns
- Performance optimization techniques
- Batch task creation
- Throughput monitoring
"""

import asyncio
import time

from blazing import Blazing


async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    # Define a step that processes individual items
    @app.step
    async def process_item(item_id: int, services=None):
        """Process a single item - simulates work."""
        # Simulate some processing time
        await asyncio.sleep(0.01)  # 10ms per item
        return {
            "item_id": item_id,
            "result": item_id * 2,
            "status": "processed"
        }

    # Publish to the execution engine
    await app.publish()

    # Number of tasks to run in parallel
    num_tasks = 100

    print(f"Creating {num_tasks} tasks...")
    start_time = time.time()

    # Launch all tasks in parallel (returns RemoteRun handles)
    runs = [
        await app.process_item(item_id=i)
        for i in range(num_tasks)
    ]

    print(f"Tasks launched in {time.time() - start_time:.2f}s")
    print("Waiting for all tasks to complete...")

    # Wait for all results in parallel
    exec_start = time.time()
    results = await asyncio.gather(*[run.result() for run in runs])
    exec_time = time.time() - exec_start

    print(f"\nCompleted {num_tasks} tasks in {exec_time:.2f}s")
    print(f"Throughput: {num_tasks / exec_time:.2f} tasks/second")
    print(f"First result: {results[0]}")
    print(f"Last result: {results[-1]}")


# ==============================================================================
# SYNC API - For learning and prototyping only
# NOTE: For production, we strongly recommend using the async Blazing class above
# ==============================================================================


def main_sync():
    """Synchronous version using SyncBlazing - for learning/prototyping only."""
    from blazing import SyncBlazing

    app = SyncBlazing()

    @app.step
    async def process_item(item_id: int, services=None):
        """Process a single item - simulates work."""
        import asyncio
        await asyncio.sleep(0.01)  # 10ms per item
        return {
            "item_id": item_id,
            "result": item_id * 2,
            "status": "processed"
        }

    # No await needed!
    app.publish()

    num_tasks = 100
    print(f"Creating {num_tasks} tasks...")
    start_time = time.time()

    # Launch all tasks (SyncBlazing handles the async internally)
    runs = [app.process_item(item_id=i) for i in range(num_tasks)]

    print(f"Tasks launched in {time.time() - start_time:.2f}s")
    print(f"First result: {runs[0]}")
    print(f"Last result: {runs[-1]}")


if __name__ == "__main__":
    # Choose your preferred style:
    asyncio.run(main())  # Async version (recommended)

    # Or use SyncBlazing (cleanest sync experience):
    # main_sync()
