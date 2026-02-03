# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Creating 100 tasks...
Tasks launched in 0.XX s
Waiting for all tasks to complete...

Completed 100 tasks in X.XX s
Throughput: XX.XX tasks/second
First result: {'item_id': 0, 'result': 0, 'status': 'processed'}
Last result: {'item_id': 99, 'result': 198, 'status': 'processed'}
```

## Notes

- Timing values (0.XX s, X.XX s, XX.XX tasks/second) will vary based on system performance and network latency
- Demonstrates launching 100 parallel workflows
- Each workflow doubles the item_id: result = item_id * 2
- First result: 0 * 2 = 0
- Last result: 99 * 2 = 198
- Throughput depends on Blazing SaaS backend performance
- Sync version produces similar results with different timing characteristics
