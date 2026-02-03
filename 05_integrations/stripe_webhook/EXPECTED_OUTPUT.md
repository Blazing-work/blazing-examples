# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Processing Stripe webhook...
[STRIPE] Signature verified successfully
[ORDER] Marked order ORD-12345 as paid
[EMAIL] Sent receipt to customer@example.com

Webhook processed:
  Order ID: ORD-12345
  Status: paid
  Processed: True
```

## Notes

- Processes a Stripe payment_intent.succeeded webhook event
- Uses HMAC SHA256 for signature verification (simulated with test secret)
- In production, would use stripe library's construct_event() method
- Demonstrates webhook signature verification and event handling
- Simulated responses use pre-defined test payload with valid signature
