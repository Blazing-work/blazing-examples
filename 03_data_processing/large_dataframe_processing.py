"""
# Large DataFrame Processing with Arrow Flight

Process large pandas DataFrames efficiently with automatic Arrow Flight optimization.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Intermediate
- **Time**: 15 min
- **Tags**: dataframe, arrow-flight, big-data, performance

## Description

When processing DataFrames larger than 1MB, Blazing automatically uses Apache Arrow Flight for 3-5x faster data transfer. This example shows how to work with large datasets without any special configuration - the optimization happens automatically.

## What you'll learn

- How to process large pandas DataFrames in workflows
- Automatic Arrow Flight optimization for DataFrames >1MB
- Performance benefits of columnar data transfer
- Working with real data science workloads
"""

from blazing import Blazing
import pandas as pd
import numpy as np

async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    @app.step
    async def generate_large_dataset(num_rows: int, services=None):
        """
        Generate a large DataFrame for processing.

        For DataFrames >1MB, Blazing automatically uses Arrow Flight
        for faster transfer between steps.
        """
        df = pd.DataFrame({
            'id': range(num_rows),
            'value': np.random.randn(num_rows),
            'category': np.random.choice(['A', 'B', 'C', 'D'], num_rows),
            'timestamp': pd.date_range('2024-01-01', periods=num_rows, freq='1min')
        })

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
            'row_count': len(df),
            'mean_value': float(df['value'].mean()),
            'std_value': float(df['value'].std()),
            'category_counts': df['category'].value_counts().to_dict(),
            'date_range': {
                'start': str(df['timestamp'].min()),
                'end': str(df['timestamp'].max())
            }
        }
        return stats

    @app.step
    async def filter_and_aggregate(df: pd.DataFrame, services=None):
        """Apply filtering and aggregation on large DataFrame."""
        # Filter for positive values
        filtered = df[df['value'] > 0]

        # Aggregate by category
        agg_result = filtered.groupby('category').agg({
            'value': ['mean', 'sum', 'count'],
            'id': 'count'
        }).reset_index()

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
            'statistics': stats,
            'aggregated_shape': aggregated.shape,
            'aggregated_data': aggregated.to_dict()
        }

    await app.publish()

    # Process 100K rows (DataFrame will be ~40MB - uses Arrow Flight automatically)
    print("\n🚀 Processing 100K row DataFrame...")
    result = await app.process_large_dataset(100000)

    print(f"\n✅ Processing complete!")
    print(f"   Rows processed: {result['statistics']['row_count']:,}")
    print(f"   Mean value: {result['statistics']['mean_value']:.4f}")
    print(f"   Categories: {result['statistics']['category_counts']}")
    print(f"   Aggregated shape: {result['aggregated_shape']}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
