# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Processed 5 items
  Item 1: 2
  Item 2: 4
  Item 3: 6
  Item 4: 8
  Item 5: 10
```

## Notes

- Processes 5 items in parallel using asyncio.gather()
- Each item value is doubled (item_id * 2)
- Output order is deterministic (items are returned in the order they were submitted)
- The example demonstrates basic parallel processing of multiple items
