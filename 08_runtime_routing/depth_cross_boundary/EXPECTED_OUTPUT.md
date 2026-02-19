# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'result': 115}
```

## Notes

- `5 * 3 = 15, 15 + 100 = 115` — sandboxed_processor calls CalculationService.multiply(5, 3) then adds 100
- Requires a running Blazing infrastructure: `docker-compose up -d`
- Demonstrates a sandboxed step crossing the sandbox boundary to call a trusted service
