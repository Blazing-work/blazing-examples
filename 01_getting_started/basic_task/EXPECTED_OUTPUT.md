# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Running workflow...
Task completed! Result: {'id': 1, 'value': 'HELLO FROM BLAZING FLOW', 'processed': True}
```

## Notes

- First line is printed before workflow execution
- Second line shows the result of the `process_data` workflow
- Input data `{"id": 1, "value": "Hello from Blazing Flow"}` is validated and transformed
- Transformation uppercases the value string
- Sync version produces identical results
