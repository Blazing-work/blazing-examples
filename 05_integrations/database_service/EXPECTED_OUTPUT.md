# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Creating new user...
[DB] Created user: id=1, name=Alice Smith, email=alice@example.com

User created successfully:
  ID: 1
  Name: Alice Smith
  Email: alice@example.com
```

## Notes

- Uses simulated in-memory database for demonstration
- In production, would use actual database connector with SQL queries
- User ID is auto-incremented starting from 1
- Demonstrates service pattern with @app.service decorator and BaseService
- Shows how steps can access services via services parameter
