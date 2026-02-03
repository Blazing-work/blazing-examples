# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Fetching 10 endpoints with rate limit of 3 concurrent...

Fetched 10 endpoints:
  endpoint_0: {'value': [random 1-100]}
  endpoint_1: {'value': [random 1-100]}
  endpoint_2: {'value': [random 1-100]}
  ...
```

## Notes

- Fetches 10 endpoints but limits concurrent requests to 3 using asyncio.Semaphore
- Random values will differ on each run (range 1-100)
- Without rate limiting, all 10 requests would fire simultaneously
- With semaphore, only 3 requests run at a time, demonstrating backpressure control
- The example shows how to implement client-side rate limiting for API calls
