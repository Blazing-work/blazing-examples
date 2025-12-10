"""
# Data Transformation Workflow

Multi-stage data pipeline with cleaning and normalization.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Beginner
- **Time**: 10 min
- **Tags**: workflow, data, transformation, pipeline

## Description

Multi-stage data pipeline with cleaning and normalization.

## What you'll learn

- How to build data processing pipelines
- How to handle data cleaning steps
- Data normalization techniques
"""

from blazing import Blazing


async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    @app.step
    async def clean_data(data: list, services=None):
        """Remove null values."""
        return [x for x in data if x is not None]

    @app.step
    async def normalize(data: list, services=None):
        """Normalize to 0-1 range."""
        min_val, max_val = min(data), max(data)
        return [(x - min_val) / (max_val - min_val) for x in data]

    @app.workflow
    async def prepare_dataset(raw_data: list, services=None):
        """Clean and normalize dataset."""
        cleaned = await clean_data(raw_data, services=services)
        normalized = await normalize(cleaned, services=services)
        return normalized

    await app.publish()
    result = await app.prepare_dataset([1, None, 5, 10, None, 15])
    print(result)  # [0.0, 0.29, 0.64, 1.0]


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
