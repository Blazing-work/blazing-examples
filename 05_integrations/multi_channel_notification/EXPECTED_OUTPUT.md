# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Sending multi-channel notification to user 123...
[PUSH] Sending to user 123: Your order has shipped!
[EMAIL] Sending to user 123: Your order has shipped!
[SMS] Sending to user 123: Your order has shipped!

Notification sent to user 123:
  email: Sent
  sms: Sent
  push: Sent
```

## Notes

- Sends notifications through 3 channels in parallel: email, SMS, and push
- All channels execute concurrently using asyncio.gather()
- Output order of channel messages may vary due to parallel execution and different simulated latencies
- All notifications are simulated with asyncio.sleep() and print statements
- Demonstrates multi-channel notification pattern for user messaging
