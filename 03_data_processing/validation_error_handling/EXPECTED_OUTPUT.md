# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Testing with valid email...
[Simulated] Sending welcome email to john@example.com
Result: {'success': True, 'user_id': XXXX}

Testing with invalid email...
Result: {'success': False, 'error': 'Invalid email: invalid-email'}
```

## Notes

- User ID (XXXX) is randomly generated between 1000-9999 and will vary each run
- First test with valid email succeeds: creates user and sends welcome email
- Second test with invalid email fails validation and returns error
- Demonstrates error handling with try/except returning structured results
- In production, would use actual user database and email service
- Email validation uses regex pattern matching
- Validation errors are caught and returned in workflow result (not propagated as exceptions)
