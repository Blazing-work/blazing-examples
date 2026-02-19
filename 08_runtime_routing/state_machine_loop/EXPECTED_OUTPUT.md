# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'final_state': 5}
```

## Notes

- The workflow loops: state starts at 0, calls next_state repeatedly until state >= 5
- Requires a running Blazing infrastructure: `docker-compose up -d`
- Demonstrates a while-loop state machine pattern inside a Blazing workflow
