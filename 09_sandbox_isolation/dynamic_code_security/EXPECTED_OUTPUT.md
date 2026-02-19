# Expected Output

## Running

```bash
python flow.py
```

## Output

```
=== Dynamic Code Security: 5-Layer Model ===

Happy path — all 5 layers:
calculate_total([10, 20, 30]) = 66.0

Layer 1 — AST validation:
Layer 1 blocked 'import os': <SecurityError message>
process_numbers([1,4,9,16,25]) = [1.0, 2.0, 3.0, 4.0, 5.0]

Layer 3 — Signature verification:
Layer 3 blocked tampered blob: <ValueError message>
Layer 3 blocked forged signature: <ValueError message>

Async functions and closures:
async_sum([1..5]) = 15

Development mode (signing disabled):
Dev mode (unsigned): simple(21) = 42

All security layers verified.
```

## Notes

- Runs locally without Docker — all security layers execute in-process
- `calculate_total([10, 20, 30]) = (10 + 20 + 30) * 1.1 = 66.0`
- The error messages for SecurityError and ValueError will include specific details about the violation
- `process_numbers([1,4,9,16,25])` returns square roots: `[1.0, 2.0, 3.0, 4.0, 5.0]`
