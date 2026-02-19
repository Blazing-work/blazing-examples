# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Distributed Dict & Queue Patterns:

  DictConnector  → shared key-value store across all workers
  QueueConnector → async FIFO queue for producer-consumer

  dict.put(key, value)    — write
  dict.get(key)           — read
  dict.get_all()          — dump all keys

  queue.put(item)         — enqueue
  queue.get()             — dequeue (blocking)
  queue.get_nowait()      — dequeue (non-blocking, returns None)
  queue.size()            — current depth

Processed 5 jobs
Metrics: {'batch_size': 5, 'jobs_processed': 5}
```

## Notes

- Requires a running Blazing infrastructure: `docker-compose up -d`
- The `main()` block prints API patterns then calls `app.publish()` and runs `batch_processing_pipeline`
- Jobs are `task_0` through `task_4` — results are uppercased: `TASK_0`, `TASK_1`, etc.
- `jobs_processed` metric is incremented once per job via `MetricsService.increment()`
