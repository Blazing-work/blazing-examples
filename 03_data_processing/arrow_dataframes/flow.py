"""
PyArrow DataFrames as Step Inputs/Outputs

Blazing steps can accept and return PyArrow Tables natively.
Arrow's columnar format makes large dataset transfers between steps
efficient — serialization is zero-copy and type-preserving.

Patterns shown:
  1. Passing an Arrow Table through a multi-step pipeline
  2. Filtering and projecting columns with Arrow compute
  3. Aggregating with pyarrow.compute
  4. Converting between Arrow and pandas mid-pipeline

Requires: pip install pyarrow pandas
The demo_local() function runs without Docker.
"""

import asyncio
import os

import pyarrow as pa
import pyarrow.compute as pc

from blazing import Blazing

app = Blazing(
    api_url=os.getenv("BLAZING_API_URL", "http://localhost:8000"),
    api_token=os.getenv("BLAZING_API_TOKEN", "demo-token-placeholder"),
)


# ── Step 1: Produce an Arrow Table ────────────────────────────────────────────

@app.step
async def load_sales_data(start_date: str, services=None) -> pa.Table:
    """
    Load raw sales records as a PyArrow Table.

    Returns a strongly-typed columnar table ready for efficient
    downstream processing.
    """
    data = {
        "order_id": [1001, 1002, 1003, 1004, 1005, 1006],
        "product":  ["A", "B", "A", "C", "B", "A"],
        "region":   ["US", "EU", "US", "EU", "US", "EU"],
        "amount":   [120.0, 85.5, 200.0, 45.0, 310.0, 95.0],
        "quantity": [2, 1, 4, 1, 5, 2],
    }
    schema = pa.schema([
        pa.field("order_id", pa.int64()),
        pa.field("product",  pa.string()),
        pa.field("region",   pa.string()),
        pa.field("amount",   pa.float64()),
        pa.field("quantity", pa.int32()),
    ])
    return pa.table(data, schema=schema)


# ── Step 2: Filter with Arrow compute ─────────────────────────────────────────

@app.step
async def filter_high_value(table: pa.Table, min_amount: float = 100.0, services=None) -> pa.Table:
    """
    Keep only orders above a threshold using Arrow compute.

    All filtering happens columnar — no Python loops, no pandas round-trip.
    """
    mask = pc.greater_equal(table.column("amount"), min_amount)
    return table.filter(mask)


# ── Step 3: Aggregate with Arrow compute ──────────────────────────────────────

@app.step
async def summarize_by_product(table: pa.Table, services=None) -> pa.Table:
    """
    Group by product and compute total revenue and order count.

    Converts to pandas for group-by, then back to Arrow.
    Returns a summary table with one row per product.
    """
    df = table.to_pandas()
    summary = (
        df.groupby("product")
        .agg(total_revenue=("amount", "sum"), order_count=("order_id", "count"))
        .reset_index()
        .sort_values("total_revenue", ascending=False)
    )
    return pa.Table.from_pandas(summary, preserve_index=False)


# ── Step 4: Format for output ─────────────────────────────────────────────────

@app.step
async def format_summary(summary: pa.Table, services=None) -> dict:
    """
    Convert Arrow summary table to a plain dict for the final result.
    """
    rows = summary.to_pydict()
    products = rows["product"]
    revenues = rows["total_revenue"]
    counts = rows["order_count"]
    return {
        "rankings": [
            {"product": p, "revenue": r, "orders": c}
            for p, r, c in zip(products, revenues, counts)
        ],
        "total_products": len(products),
        "grand_total": round(sum(revenues), 2),
    }


# ── Workflow ───────────────────────────────────────────────────────────────────

@app.workflow
async def sales_analysis(start_date: str, min_amount: float = 100.0, services=None) -> dict:
    """
    Full Arrow pipeline: load → filter → aggregate → format.

    PyArrow Tables flow between steps as first-class values.
    Blazing serializes them using Arrow IPC format.
    """
    raw = await load_sales_data(start_date)
    filtered = await filter_high_value(raw, min_amount)
    summary = await summarize_by_product(filtered)
    return await format_summary(summary)


# ── Main: demo locally without Docker ─────────────────────────────────────────

async def demo_local():
    """Run the Arrow pipeline locally without Docker."""
    print("=== PyArrow Step I/O Demo ===")
    print()

    raw = await load_sales_data("2024-01-01")
    print(f"Raw table: {raw.num_rows} rows, columns: {raw.column_names}")
    print(raw.to_pandas().to_string(index=False))
    print()

    filtered = await filter_high_value(raw, min_amount=100.0)
    print(f"Filtered (amount >= 100): {filtered.num_rows} rows")
    print(filtered.to_pandas().to_string(index=False))
    print()

    summary = await summarize_by_product(filtered)
    print("Summary by product:")
    print(summary.to_pandas().to_string(index=False))
    print()

    result = await format_summary(summary)
    print(f"Final result: {result}")


if __name__ == "__main__":
    asyncio.run(demo_local())
