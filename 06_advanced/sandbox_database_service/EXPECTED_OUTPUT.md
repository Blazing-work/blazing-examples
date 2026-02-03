# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Generating report for user 1 (with concurrent data fetching)...

User Report:
  Name: Alice Smith
  Total Orders: 2
  Total Spent: $249.98
  Average Order: $124.99
  Recommendations: 3

Generating report for user 2...

User Report:
  Name: Bob Jones
  Total Orders: 1
  Total Spent: $49.99
  Average Order: $49.99
  Recommendations: 1
```

## Notes

- This is NOT a run_sandboxed() example despite being in sandbox_* directory
- Uses @app.step decorator for the analyze_user function
- Demonstrates concurrent service calls within sandboxed step (asyncio.gather)
- Fetches user data, orders, and recommendations in parallel
- User 1 (Alice) has 2 orders totaling $249.98
- User 2 (Bob) has 1 order totaling $49.99
- Uses simulated in-memory databases for demonstration
- Shows how sandboxed code can make concurrent calls to trusted services
