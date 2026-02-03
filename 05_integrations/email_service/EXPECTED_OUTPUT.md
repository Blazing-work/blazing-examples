# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Sending welcome email...
[EMAIL] To: john@example.com
[EMAIL] Subject: Welcome, John!
[EMAIL] Body: Hello John,

Welcome to our platform!

Best regard...

Email sent successfully to john@example.com
```

## Notes

- Sends a welcome email to john@example.com
- Email body is truncated in the simulated output (first 50 characters)
- In production, would use actual SMTP connector to send real emails
- Demonstrates basic email service integration pattern
