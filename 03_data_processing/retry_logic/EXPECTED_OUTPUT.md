# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Running workflow with retry logic (30% failure rate)...
Result: {'success': True, 'result': 'processed: test data', 'attempts': 1}
Attempts made: 1
```

OR (if retries needed):

```
Running workflow with retry logic (30% failure rate)...
Result: {'success': True, 'result': 'processed: test data', 'attempts': 2}
Attempts made: 2
```

OR (if all retries fail):

```
Running workflow with retry logic (30% failure rate)...
Result: {'success': False, 'error': 'Transient error', 'attempts': 3}
Attempts made: 3
```

## Notes

- Operation has 30% random failure rate, so output varies between runs
- May succeed on first attempt (70% chance)
- May require 2-3 attempts with exponential backoff (2^attempt seconds between retries)
- Maximum 3 attempts before final failure
- Demonstrates retry pattern with error handling and backoff strategy
