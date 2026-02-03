# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'mean': 3.0, 'median': 3, 'count': 5}
```

## Notes

- Result of `get_statistics(numbers=[1, 2, 3, 4, 5])` workflow
- Demonstrates parallel execution using asyncio.gather
- Mean calculation: (1+2+3+4+5)/5 = 3.0
- Median calculation: sorted middle value = 3
- Count is the length of input list
- Sync version produces identical results
