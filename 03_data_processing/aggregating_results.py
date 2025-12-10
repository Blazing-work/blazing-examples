"""
# Aggregating Results

Fetch data from multiple sources and aggregate into summary statistics.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Intermediate
- **Time**: 20 min
- **Tags**: aggregation, data, statistics, parallel

## Description

Fetch data from multiple sources and aggregate into summary statistics.

## What you'll learn

- Parallel data fetching patterns
- Result aggregation techniques
- Computing summary statistics
"""

import asyncio

from blazing import Blazing


async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    @app.step
    async def fetch_sales_data(region: str, services=None):
        """Fetch sales data for region."""
        data = await services["SalesDatabase"].get_by_region(region)
        return {"region": region, "total": sum(d["amount"] for d in data)}

    @app.workflow
    async def aggregate_sales(regions: list, services=None):
        """Aggregate sales across all regions."""
        results = await asyncio.gather(
            *[fetch_sales_data(region, services=services) for region in regions]
        )

        total_sales = sum(r["total"] for r in results)
        return {
            "by_region": results,
            "grand_total": total_sales,
            "regions_count": len(regions),
        }

    await app.publish()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
