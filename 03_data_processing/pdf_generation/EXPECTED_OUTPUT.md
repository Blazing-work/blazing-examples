# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Creating invoice for order ORD-12345...
[Simulated] Uploading XXX bytes to invoices/ORD-12345.pdf

Invoice created!
  Order ID: ORD-12345
  Invoice URL: https://storage.example.com/invoices/ORD-12345.pdf
  Total: $109.97
```

## Notes

- PDF byte size (XXX) will be approximately 300-400 bytes for simulated content
- In production, would use WeasyPrint or similar library to generate actual PDF
- In production, would fetch order data from database and upload to real file storage
- Simulated invoice includes:
  - Order ID: ORD-12345
  - Customer: John Doe
  - Items: Widget A ($29.99 x 2), Widget B ($49.99 x 1)
  - Total: $109.97
- Demonstrates pipeline: generate data → render PDF → upload to storage
