# Expected Output

## Running

```bash
python flow.py
```

## Output

```
[0.0, 0.2857142857142857, 0.6428571428571429, 1.0]
```

## Notes

- Result of `prepare_dataset(raw_data=[1, None, 5, 10, None, 15])` workflow
- First step removes None values: [1, 5, 10, 15]
- Second step normalizes to 0-1 range using formula: (x - min) / (max - min)
- Normalized values: [0.0, 0.29, 0.64, 1.0] (approximate)
- Exact float representation may vary slightly
- Sync version produces identical results
