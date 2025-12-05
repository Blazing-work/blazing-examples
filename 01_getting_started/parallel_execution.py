"""
# Parallel Execution

Execute multiple tasks concurrently for 10x speedup.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Intermediate
- **Time**: 15 min
- **Tags**: concurrency, performance, parallel

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
    app = Blazing()

    try:
        # Number of tasks to run in parallel
        num_tasks = 100

        print(f"Creating {num_tasks} tasks...")
        start_time = time.time()

        # Create all tasks first (this is fast)
        tasks = [
            await app.create_route_task("process_item", item_id=i)
            for i in range(num_tasks)
        ]

        print(f"Tasks created in {time.time() - start_time:.2f}s")
        print("Executing tasks in parallel...")

        # Execute all tasks in parallel
        exec_start = time.time()
        results = await app.gather(tasks)
        exec_time = time.time() - exec_start

        print(f"\nCompleted {num_tasks} tasks in {exec_time:.2f}s")
        print(f"Throughput: {num_tasks / exec_time:.2f} tasks/second")
        print(f"First result: {results[0]}")

    finally:
        await app.close()


if __name__ == "__main__":
    asyncio.run(main())
