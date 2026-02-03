# Expected Output

## Running

```bash
python flow.py
```

## Output

```
First lookup for 'user_123'...
[Computing] Expensive computation for key: user_123
Result: {'source': 'computed', 'value': 'computed_value_for_user_123'}

Second lookup for 'user_123'...
Result: {'source': 'cache', 'value': 'computed_value_for_user_123'}

Lookup for 'user_456'...
[Computing] Expensive computation for key: user_456
Result: {'source': 'computed', 'value': 'computed_value_for_user_456'}
```

## Notes

- First lookup for 'user_123' results in cache miss and triggers expensive computation
- Second lookup for 'user_123' returns cached value (no computation message)
- Third lookup for 'user_456' is a different key, so cache miss occurs again
- Demonstrates the cache-aside pattern where cache is checked before expensive operations
- Uses simulated in-memory cache for demonstration
