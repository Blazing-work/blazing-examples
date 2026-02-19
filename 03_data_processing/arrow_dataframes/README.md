# PyArrow DataFrames as Step I/O

Pass Apache Arrow Tables between workflow steps as first-class values.

## Why Arrow?

- **Columnar format** — fast filtering and aggregation without Python loops
- **Type-preserving** — schema is carried with the table, no type inference
- **Pandas interop** — zero-copy conversion for group-by and joins
- **Blazing IPC** — tables are transferred between steps using Arrow IPC format

## API

```python
import pyarrow as pa
import pyarrow.compute as pc

@app.step
async def filter_data(table: pa.Table, threshold: float, services=None) -> pa.Table:
    mask = pc.greater_equal(table.column("amount"), threshold)
    return table.filter(mask)

@app.step
async def summarize(table: pa.Table, services=None) -> dict:
    df = table.to_pandas()
    summary = df.groupby("product").agg(total=("amount", "sum"))
    return summary.to_dict(orient="records")
```

## Example Pipeline

```
load_sales_data(date)          → pa.Table (raw)
  → filter_high_value(≥100)    → pa.Table (filtered)
  → summarize_by_product()     → pa.Table (aggregated)
  → format_summary()           → dict (JSON-safe output)
```

## Running Locally

```bash
pip install pyarrow pandas
python flow.py
```

No Docker needed for the local demo. Use `app.publish()` / `app.run()` to execute on Blazing workers.
