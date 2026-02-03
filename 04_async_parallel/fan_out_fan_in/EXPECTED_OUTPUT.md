# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Fetching user profile (fan-out / fan-in pattern)...
  - fetch_user_data (0.3s)
  - fetch_user_orders (0.5s)
  - fetch_user_preferences (0.2s)
  Total sequential time: 1.0s
  Expected parallel time: ~0.5s (longest task)

User Profile fetched in [varies, ~0.5-0.7s]:
  User: User 123 (user123@example.com)
  Orders: 2 orders
  Preferences: {'theme': 'dark', 'notifications': True, 'language': 'en'}
```

## Notes

- Duration is approximately 0.5s due to parallel execution (limited by the slowest task)
- Sequential execution would take ~1.0s
- The example demonstrates the fan-out/fan-in pattern where multiple operations run in parallel and results are combined
- All data is simulated with asyncio.sleep() delays
