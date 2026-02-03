# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Aggregating sales for regions: ['North America', 'Europe', 'Asia Pacific', 'Latin America']

Results by region:
  North America: $XX,XXX
  Europe: $XX,XXX
  Asia Pacific: $XX,XXX
  Latin America: $XX,XXX

Grand Total: $XXX,XXX
Regions processed: 4
```

## Notes

- Sales values (XX,XXX) are randomly generated between 10,000-100,000 per region and will vary each run
- Grand total is the sum of all regional totals
- All 4 regions are fetched concurrently using asyncio.gather
- Each fetch simulates 0.1s network latency
- In production, would query actual sales database
- Currency formatting includes comma separators
