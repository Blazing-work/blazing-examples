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
- Execute workflows with `app.run()` or direct invocation
- Wait for results with `.wait_result()`
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
        # Execute a workflow and wait for result
        print("Running workflow...")

        # Option 1: Direct invocation (if workflow is defined locally)
        # result = await app.process_data(data={"id": 1, "value": "Hello"}).wait_result()

        # Option 2: By name (useful for pre-registered workflows)
        result = await app.run("process_data", data={"id": 1, "value": "Hello from Blazing Flow"}).wait_result()

        print(f"Task completed! Result: {result}")

    finally:
        # Always clean up resources
        await app.close()


if __name__ == "__main__":
    asyncio.run(main())
