# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Running optimized mixed workload...
   - I/O work: NON_BLOCKING workers (concurrent)
   - CPU work: BLOCKING workers (doesn't block I/O)

Workflow complete!

Results:
   API calls: 3 concurrent requests
   API duration: [varies, ~1.0-1.5s]
   Fibonacci(30): 832040
   Fibonacci duration: [varies, ~0.1-0.5s]
   Matrix size: 100x100
   Matrix duration: [varies, ~0.05-0.2s]
```

## Notes

- Timing values vary based on system performance and network latency
- API duration depends on external httpbin.org service (typically ~1 second for 3 concurrent delay/1 requests)
- CPU-bound operations (Fibonacci, matrix) use BLOCKING workers and don't block I/O operations
- The example demonstrates optimal worker type selection for mixed workloads
