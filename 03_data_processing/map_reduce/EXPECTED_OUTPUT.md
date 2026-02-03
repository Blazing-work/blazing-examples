# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Computing sum of squares for 1000 numbers...
Result: 333833500
Chunks processed: 10
Total numbers: 1000
```

## Notes

- Computes sum of squares for numbers 1 to 1000
- Result is deterministic: 1² + 2² + 3² + ... + 1000² = 333,833,500
- Numbers are split into 10 chunks of 100 each
- Each chunk is processed in parallel using asyncio.gather
- Demonstrates classic map-reduce pattern:
  - Map phase: Compute sum of squares for each chunk
  - Reduce phase: Sum all chunk results
- Chunk size is configurable (default: 100)
