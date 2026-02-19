# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Batched Step Patterns:

  @batched(max_batch_size=32, wait_ms=100)
    → GPU classification: collect up to 32 calls or wait 100ms

  @batched(max_batch_size=100, wait_ms=50)
    → Bulk inserts: up to 100 rows per SQL statement

  @batched(max_batch_size=10, wait_ms=200)
    → API rate optimization: 200ms accumulation window

  @batched(max_batch_size=64, wait_ms=25, pad_to_max=True)
    → Fixed-shape batches for static-graph GPU kernels

Individual callers always pass a single item.
Blazing handles accumulation and dispatch transparently.

Deploy: app.publish()
```

## Notes

- This example runs standalone — no Docker required (the `__main__` block only prints pattern descriptions)
- The `@batched` steps are registered but not executed — this is a structural/API demonstration
- Batching only takes effect when `app.publish()` is called and steps are invoked concurrently from multiple callers
