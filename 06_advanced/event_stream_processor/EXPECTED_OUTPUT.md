# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Processing event stream batch from 'user-events' topic...
[KAFKA] Produced to user-events: page_view
[KAFKA] Produced to user-events: click
[KAFKA] Produced to user-events: page_view
[KAFKA] Produced to user-events: purchase
[KAFKA] Produced to user-events: page_view
[KAFKA] Produced to user-events: click
[KAFKA] Produced to user-events: purchase

Stream Processing Results:
  Topic: user-events
  Events Processed: 7
  Event Type Breakdown:
    - page_view: 3
    - click: 2
    - purchase: 2

Total events stored in database: 7
```

## Notes

- Consumes batch of 7 events from simulated Kafka topic 'user-events'
- Transforms each event (adds processed_at timestamp and enriched flag)
- Aggregates events by type using Counter
- Stores processed events in simulated database
- Kafka produce messages may appear in different order due to async operations
- In production, would use actual Kafka connector
- Demonstrates stream processing pattern with batch consumption, transformation, and storage
