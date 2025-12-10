"""
# Map-Reduce Pattern

Distributed map-reduce for processing large datasets in chunks.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Advanced
- **Time**: 30 min
- **Tags**: map-reduce, distributed, big-data, parallel

## Description

Distributed map-reduce for processing large datasets in chunks.

## What you'll learn

- Map-reduce pattern implementation
- Data chunking strategies
- Distributed computing fundamentals
"""

import asyncio

from blazing import Blazing


async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    @app.step
    async def map_operation(chunk: list, services=None):
        """Map operation: process chunk."""
        return sum(x**2 for x in chunk)

    @app.step
    async def reduce_operation(results: list, services=None):
        """Reduce operation: combine results."""
        return sum(results)

    @app.workflow
    async def map_reduce_sum_of_squares(
        numbers: list, chunk_size: int = 100, services=None
    ):
        """Map-reduce pattern for sum of squares."""

        # Split into chunks (map phase)
        chunks = [
            numbers[i : i + chunk_size] for i in range(0, len(numbers), chunk_size)
        ]

        # Process chunks in parallel
        mapped_results = await asyncio.gather(
            *[map_operation(chunk, services=services) for chunk in chunks]
        )

        # Combine results (reduce phase)
        final_result = await reduce_operation(mapped_results, services=services)

        return {
            "result": final_result,
            "chunks_processed": len(chunks),
            "total_numbers": len(numbers),
        }

    await app.publish()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
