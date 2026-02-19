# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'result': 'value=35'}
```

## Notes

- `MathService.multiply(7, 5) = 35`, `StringService.label(35) = 'value=35'`
- Requires a running Blazing infrastructure: `docker-compose up -d`
- Demonstrates chaining two services in one step: multiplication then string formatting
