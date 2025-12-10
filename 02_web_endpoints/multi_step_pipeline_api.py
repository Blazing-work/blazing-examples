"""
# Multi-Step Data Pipeline API

Expose a multi-step workflow that processes data through several stages.

## Metadata
- **Product**: Blazing Flow Endpoints
- **Difficulty**: Intermediate
- **Time**: 15 min
- **Tags**: endpoint, pipeline, multi-step, statistics

## Description

Expose a multi-step workflow that processes data through several stages.

## What you'll learn

- How to expose multi-step workflows as endpoints
- How to organize internal steps vs public endpoints
- Data validation and transformation via REST API
"""

from blazing import Blazing
from blazing.web import create_asgi_app


async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    # Internal steps (not exposed directly)
    @app.step
    async def validate_data(data: dict, services=None):
        """Validate input data."""
        if not data.get("values"):
            raise ValueError("Missing 'values' field")
        return data

    @app.step
    async def compute_statistics(data: dict, services=None):
        """Compute basic statistics."""
        values = data["values"]
        return {
            "count": len(values),
            "sum": sum(values),
            "average": sum(values) / len(values) if values else 0,
            "min": min(values) if values else 0,
            "max": max(values) if values else 0,
        }

    @app.step
    async def format_report(stats: dict, services=None):
        """Format statistics as a report."""
        return {
            "summary": f"Analyzed {stats['count']} values",
            "statistics": stats,
            "status": "completed",
        }

    # Public endpoint (exposes the workflow)
    @app.endpoint(path="/analyze")
    @app.workflow
    async def analyze_data(data: dict, services=None):
        """
        Public API: Analyze data and return statistics.
        POST /analyze
        Body: {"data": {"values": [1, 2, 3, 4, 5]}}
        """
        validated = await validate_data(data, services=services)
        stats = await compute_statistics(validated, services=services)
        report = await format_report(stats, services=services)
        return report

    await app.publish()
    await create_asgi_app(app, title="Data Analysis API")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
