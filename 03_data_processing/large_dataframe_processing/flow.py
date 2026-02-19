"""
Large DataFrame Processing

Demonstrates processing large pandas DataFrames across multiple steps with automatic
Arrow Flight transport for datasets over 1 MB.  A 100K-row DataFrame is generated,
statistics are computed, and filtered/aggregated results are returned.

Patterns shown:
  1. Generating a large DataFrame in a step (triggers Arrow Flight >1 MB)
  2. Computing statistics on a DataFrame passed between steps
  3. Filter + groupby aggregation in a downstream step
  4. Blazing's automatic small/large data transport selection (Redis vs Arrow Flight)

Requires: pip install numpy pandas
"""
import numpy as np
import pandas as pd

from blazing import Blazing


async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    @app.step
    async def generate_large_dataset(num_rows: int, services=None):
        """
        Generate a large DataFrame for processing.

        For DataFrames >1MB, Blazing automatically uses Arrow Flight
        for faster transfer between steps.
        """
        df = pd.DataFrame(
            {
                "id": range(num_rows),
                "value": np.random.randn(num_rows),
                "category": np.random.choice(["A", "B", "C", "D"], num_rows),
                "timestamp": pd.date_range("2024-01-01", periods=num_rows, freq="1min"),
            }
        )

        # Check size
        size_mb = df.memory_usage(deep=True).sum() / 1024 / 1024
        print(f"Generated DataFrame: {size_mb:.2f}MB")

        return df

    @app.step
    async def compute_statistics(df: pd.DataFrame, services=None):
        """
        Compute statistics on the large DataFrame.

        The DataFrame is automatically transferred via Arrow Flight
        if it's large enough (>1MB).
        """
        stats = {
            "row_count": len(df),
            "mean_value": float(df["value"].mean()),
            "std_value": float(df["value"].std()),
            "category_counts": df["category"].value_counts().to_dict(),
            "date_range": {
                "start": str(df["timestamp"].min()),
                "end": str(df["timestamp"].max()),
            },
        }
        return stats

    @app.step
    async def filter_and_aggregate(df: pd.DataFrame, services=None):
        """Apply filtering and aggregation on large DataFrame."""
        # Filter for positive values
        filtered = df[df["value"] > 0]

        # Aggregate by category
        agg_result = (
            filtered.groupby("category")
            .agg({"value": ["mean", "sum", "count"], "id": "count"})
            .reset_index()
        )

        return agg_result

    @app.workflow
    async def process_large_dataset(num_rows: int, services=None):
        """
        Complete workflow for processing large DataFrames.

        Key performance optimization:
        - Small data (<1MB): Uses Redis/pickle (fast enough)
        - Large data (>1MB): Automatically uses Arrow Flight (3-5x faster)

        You don't need to configure anything - Blazing chooses
        the best transfer method automatically!
        """
        # Step 1: Generate large dataset
        df = await generate_large_dataset(num_rows, services=services)

        # Step 2: Compute statistics
        stats = await compute_statistics(df, services=services)

        # Step 3: Filter and aggregate
        aggregated = await filter_and_aggregate(df, services=services)

        return {
            "statistics": stats,
            "aggregated_shape": aggregated.shape,
            "aggregated_data": aggregated.to_dict(),
        }

    await app.publish()

    # Process 100K rows (DataFrame will be ~40MB - uses Arrow Flight automatically)
    print("\n Processing 100K row DataFrame...")
    result = await app.process_large_dataset(num_rows=100000).wait_result()

    print("\n Processing complete!")
    print(f"   Rows processed: {result['statistics']['row_count']:,}")
    print(f"   Mean value: {result['statistics']['mean_value']:.4f}")
    print(f"   Categories: {result['statistics']['category_counts']}")
    print(f"   Aggregated shape: {result['aggregated_shape']}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
