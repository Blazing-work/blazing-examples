"""
Serialize Loading Strategy Example for Blazing

Blazing supports three loading strategies that control how step code reaches
the executor worker:

  loading_strategy="wheel"       (default) — build a Python wheel, upload it
  loading_strategy="serialize"   — serialize step functions with dill
  loading_strategy="dockerfile"  — bundle code inside a custom Docker image

The "serialize" strategy is the fastest way to iterate:
- No wheel build step
- Functions are serialized at runtime and sent to workers
- Great for rapid local development and prototyping

Requires: docker-compose up -d
"""

import os

from blazing import Blazing

app = Blazing(
    api_url=os.getenv("BLAZING_API_URL", "http://localhost:8000"),
    api_token=os.getenv("BLAZING_API_TOKEN", "demo-token-placeholder"),
    loading_strategy="serialize",   # serialize functions at runtime
)


# ── Steps: identical to any other workflow ────────────────────────────────────

@app.step
async def fetch_data(query: str, services=None) -> dict:
    """Simulate fetching data for a query."""
    return {"query": query, "rows": [1, 2, 3, 4, 5], "count": 5}


@app.step
async def aggregate(data: dict, services=None) -> dict:
    """Aggregate fetched data."""
    rows = data["rows"]
    return {
        "query": data["query"],
        "sum": sum(rows),
        "mean": sum(rows) / len(rows),
        "count": data["count"],
    }


@app.step
async def format_report(aggregated: dict, services=None) -> str:
    """Format aggregation result as a report string."""
    return (
        f"Report for '{aggregated['query']}': "
        f"sum={aggregated['sum']}, mean={aggregated['mean']:.1f}, "
        f"n={aggregated['count']}"
    )


@app.workflow
async def analysis_pipeline(query: str, services=None) -> str:
    """Full analysis pipeline: fetch → aggregate → format."""
    data = await fetch_data(query)
    agg = await aggregate(data)
    report = await format_report(agg)
    return report


# ── Main ──────────────────────────────────────────────────────────────────────

async def main():
    print("Loading Strategy: serialize")
    print()
    print("Strategies comparison:")
    print("  'wheel'      — build & upload wheel (default, best for production)")
    print("  'serialize'  — serialize functions at runtime (fastest to iterate)")
    print("  'dockerfile' — bundle code in custom image (full control)")
    print()

    await app.publish()
    print("Published with loading_strategy='serialize'")
    print()

    result = await app.run(analysis_pipeline, args=("monthly sales",))
    print(f"Result: {result}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
