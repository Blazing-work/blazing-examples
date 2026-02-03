# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Queueing 5 emails...

Queue has 5 emails

Processing email queue (batch of 10)...
[Simulated] Sending email to user0@example.com: Test Email 0
[Simulated] Sending email to user1@example.com: Test Email 1
[Simulated] Sending email to user2@example.com: Test Email 2
[Simulated] Sending email to user3@example.com: Test Email 3
[Simulated] Sending email to user4@example.com: Test Email 4

Results:
  Processed: 10
  Sent: 5
```

## Notes

- Queues 5 emails first, then processes them in a batch of 10
- Since only 5 emails are queued, only 5 are sent (the other 5 batch slots are empty)
- Uses simulated in-memory queue for demonstration
- Email sending is simulated with asyncio.sleep() and print statements
- Demonstrates batch processing pattern with asyncio.gather()
- Output order of email sending may vary due to parallel processing
