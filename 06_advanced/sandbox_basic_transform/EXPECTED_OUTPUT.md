# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'transformed': [2, 6, 10], 'count': 3}
```

## Notes

- This is NOT a run_sandboxed() example despite the name
- Uses @app.step decorator which automatically sandboxes the user_transform function
- Transforms input list [1, -2, 3, -4, 5] by filtering positive numbers and doubling them
- Result: [1, 3, 5] → [2, 6, 10]
- Demonstrates basic sandboxed data transformation with no external access
- User code runs in WASM sandbox with no network or filesystem access
- Simplest sandbox pattern - pure Python computation
