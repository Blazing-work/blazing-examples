"""
# Basic Task Execution

Create and execute distributed tasks with automatic retry.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Beginner
- **Time**: 10 min
- **Tags**: tasks, async, distributed

## Description

This example demonstrates how to create and execute distributed tasks using Blazing Flow.
You'll learn how to:
- Initialize a Blazing Flow application
- Create tasks with `create_route_task()`
- Retrieve results with `gather()`
- Proper resource cleanup

## What you'll learn

- Task lifecycle management
- Async/await patterns in Python
- Distributed task execution
- Error handling basics
"""

import asyncio

from blazing import Blazing


async def main():
    # Initialize Blazing app
    app = Blazing()

    try:
        # Create a simple task
        print("Creating task...")
        task = await app.create_route_task(
            "process_data", data={"id": 1, "value": "Hello from Blazing Flow"}
        )

        # Wait for the task to complete and get result
        print("Waiting for task to complete...")
        results = await app.gather([task])

        print(f"Task completed! Result: {results[0]}")

    finally:
        # Always clean up resources
        await app.close()


if __name__ == "__main__":
    asyncio.run(main())
