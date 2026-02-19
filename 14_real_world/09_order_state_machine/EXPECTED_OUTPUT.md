# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'ORD-001': 'COMPLETED', 'ORD-002': 'FAILED', 'ORD-003': 'FAILED'}
```

## Notes

- Requires a running Blazing infrastructure: `docker-compose up -d`
- ORD-001: payment valid + inventory in stock → COMPLETED
- ORD-002: payment valid + inventory out of stock → FAILED
- ORD-003: payment declined → FAILED (inventory check is skipped)
- State transitions: PENDING → PAYMENT_CHECK → INVENTORY_CHECK → APPROVED → COMPLETED (or REJECTED → FAILED)
