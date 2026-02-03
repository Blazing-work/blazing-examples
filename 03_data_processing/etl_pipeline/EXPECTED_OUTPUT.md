# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Running ETL pipeline...
[Simulated] Loading 3 records to analytics_warehouse

ETL Pipeline completed!
  Source: products_db
  Destination: analytics_warehouse
  Rows processed: 3
```

## Notes

- Demonstrates classic Extract-Transform-Load pattern
- Extracts 4 sample product records (simulated)
- Transforms by filtering invalid records (removes 1 invalid product)
- Loads 3 valid records to destination
- Each record is enriched with processed_at timestamp during transformation
- In production, would use actual database services for extraction and loading
- Timestamp values in transformed data will vary per run
