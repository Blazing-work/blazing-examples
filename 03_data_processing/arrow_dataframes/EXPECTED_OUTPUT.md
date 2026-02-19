# Expected Output

## Running

```bash
python flow.py
```

## Output

```
=== PyArrow Step I/O Demo ===

Raw table: 6 rows, columns: ['order_id', 'product', 'region', 'amount', 'quantity']
 order_id product region  amount  quantity
     1001       A     US  120.00         2
     1002       B     EU   85.50         1
     1003       A     US  200.00         4
     1004       C     EU   45.00         1
     1005       B     US  310.00         5
     1006       A     EU   95.00         2

Filtered (amount >= 100): 3 rows
 order_id product region  amount  quantity
     1001       A     US  120.00         2
     1003       A     US  200.00         4
     1005       B     US  310.00         5

Summary by product:
  product  total_revenue  order_count
        B          310.0            1
        A          320.0            2

Final result: {'rankings': [{'product': 'B', 'revenue': 310.0, 'orders': 1}, {'product': 'A', 'revenue': 320.0, 'orders': 2}], 'total_products': 2, 'grand_total': 630.0}
```

## Notes

- Runs locally without Docker — `demo_local()` is called directly, no Blazing infrastructure needed
- Product B (310.0) is listed before A (320.0) due to pandas sort_values ascending; actual order may differ
- The `grand_total` is 120 + 200 + 310 = 630.0
- Requires: `pip install pyarrow pandas`
