# Expected Output

## Running

```bash
python flow.py
```

## Output

```
 Processing 100K row DataFrame...
Generated DataFrame: XX.XX MB

 Processing complete!
   Rows processed: 100,000
   Mean value: X.XXXX
   Categories: {'A': ~25000, 'B': ~25000, 'C': ~25000, 'D': ~25000}
   Aggregated shape: (4, X)
```

## Notes

- DataFrame size (XX.XX MB) will be approximately 40MB for 100K rows
- Mean value (X.XXXX) is from standard normal distribution, expected near 0.0
- Categories are uniformly distributed, approximately 25,000 per category (A/B/C/D)
- Exact counts and statistics vary due to random data generation
- Demonstrates automatic Arrow Flight optimization for DataFrames >1MB
- Aggregation shape shows 4 rows (one per category) with multiple aggregation columns
- Requires pandas and numpy to run
- Processing includes statistics computation, filtering, and groupby aggregation
