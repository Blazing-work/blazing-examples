# Expected Output

## Running

```bash
python flow.py
```

## Output

```
============================================================
Batch Stock Processing Demo
============================================================

Processing 13 stocks with rate limit: 5 req/0.5s
------------------------------------------------------------
  Processing batch 1/4: ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
  Processing batch 2/4: ['META', 'NVDA', 'TSLA', 'JPM']
  Processing batch 3/4: ['V', 'JNJ', 'WMT', 'PG']
  Processing batch 4/4: ['INVALID']

============================================================
Results Summary
============================================================
Total symbols:     13
Successful:        12
Failed:            1
Batches processed: 4
Total API calls:   13
Elapsed time:      [varies, ~1.5-2.5s]

Errors:
  - INVALID: Not found

============================================================
Throttling Configurations Available:
============================================================
  conservative: 10 req / 1.0s (fixed)
  standard    : 100 req / 60.0s (rolling)
  aggressive  : 1000 req / 60.0s (rolling)
```

## Notes

- Updated example from plan 04-04 to use current SDK patterns
- Processes 13 stocks in 4 batches with rate limiting (5 requests per 0.5 seconds)
- Elapsed time varies based on rate limiting and simulated API delays
- One stock symbol (INVALID) intentionally fails to demonstrate error handling
- Demonstrates batch processing pattern with throttling configuration from tradegrid
- Total API calls matches total symbols (each symbol requires one API call)
