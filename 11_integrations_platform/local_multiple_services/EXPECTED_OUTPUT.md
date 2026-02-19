# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'doubled': 42.0, 'label': 'ANSWER'}
```

## Notes

- `MathService.multiply(21.0, 2.0) = 42.0`, `StringService.uppercase('answer') = 'ANSWER'`
- Requires a running Blazing infrastructure: `docker-compose up -d`
- Demonstrates injecting and using two services in a single step
