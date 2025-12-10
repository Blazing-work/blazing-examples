"""
# Multi-Branch Workflow

Parallel execution with asyncio.gather for concurrent processing.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Intermediate
- **Time**: 15 min
- **Tags**: workflow, parallel, asyncio, branching

## Description

Parallel execution with asyncio.gather for concurrent processing.

## What you'll learn

- How to run steps in parallel with asyncio.gather
- How to combine results from parallel branches
- When to use parallel vs sequential execution
"""

import asyncio

from blazing import Blazing


async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    @app.step
    async def calculate_mean(numbers: list, services=None):
        """Calculate mean."""
        return sum(numbers) / len(numbers)

    @app.step
    async def calculate_median(numbers: list, services=None):
        """Calculate median."""
        sorted_nums = sorted(numbers)
        mid = len(sorted_nums) // 2
        return sorted_nums[mid]

    @app.workflow
    async def get_statistics(numbers: list, services=None):
        """Calculate multiple statistics in parallel."""
        mean, median = await asyncio.gather(
            calculate_mean(numbers, services=services),
            calculate_median(numbers, services=services),
        )
        return {"mean": mean, "median": median, "count": len(numbers)}

    await app.publish()
    result = await app.get_statistics([1, 2, 3, 4, 5])
    print(result)  # {"mean": 3.0, "median": 3, "count": 5}


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
