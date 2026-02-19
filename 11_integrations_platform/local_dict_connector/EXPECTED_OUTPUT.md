# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'value': 3, 'history': [1, 2, 3]}
```

## Notes

- The loop increments state['value'] from 0 to 3, appending each value to history
- This example runs standalone — no docker-compose required (uses `LocalDictService`)
- `LocalDictService` provides an in-memory key-value store without external dependencies
