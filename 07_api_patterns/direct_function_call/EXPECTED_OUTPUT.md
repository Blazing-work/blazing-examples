# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'result': '92.5%'}
```

## Notes

- Runs locally without Docker — steps are called directly in-process, no `app.publish()` needed
- `normalize(92.5) = 0.925`, `format_result(0.925) = '92.5%'`
- The `__main__` block runs assertions then prints the workflow result
- No Blazing infrastructure required — this is the "direct function call" pattern for local testing
