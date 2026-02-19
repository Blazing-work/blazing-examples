# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'sum': 15.0, 'scaled': 150.0}
```

## Notes

- `sum([1,2,3,4,5]) = 15.0`, `15.0 * 10.0 = 150.0`
- Requires a running Blazing infrastructure: `docker-compose up -d`
- Demonstrates a multi-step workflow where one step computes a sum and a second scales the result using a service
