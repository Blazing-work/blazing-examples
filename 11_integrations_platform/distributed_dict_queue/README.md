# Distributed Dict & Queue

Shared state and message passing between service workers via `DictConnector` and `QueueConnector`.

## Connectors

| Connector | Model | Backed by |
|-----------|-------|-----------|
| `DictConnector` | Shared key-value store | Redis hash |
| `QueueConnector` | Async FIFO queue | Redis list |

Both connectors are injected into services by Blazing. All instances of the same service share the same underlying data.

## DictConnector API

```python
@app.service
class StateService(BaseService):
    def __init__(self, connector_instances=None):
        super().__init__(connector_instances)
        self.state = connector_instances.get("my-dict")

    async def example(self):
        await self.state.put("key", {"value": 42})    # write
        data = await self.state.get("key")            # read
        all_data = await self.state.get_all()         # dump all keys
        await self.state.delete("key")                # remove
```

## QueueConnector API

```python
@app.service
class WorkerService(BaseService):
    def __init__(self, connector_instances=None):
        super().__init__(connector_instances)
        self.queue = connector_instances.get("my-queue")

    async def produce(self, item: dict):
        await self.queue.put(item)          # enqueue

    async def consume(self) -> dict:
        return await self.queue.get()       # dequeue (blocking)

    async def try_consume(self) -> dict:
        return await self.queue.get_nowait() # non-blocking (returns None if empty)

    async def depth(self) -> int:
        return await self.queue.size()
```

## Use Cases

- **DictConnector**: shared counters, feature flags, job state, cache
- **QueueConnector**: task queues, event streams, work stealing, fan-out

## Running

```bash
docker-compose up -d
python flow.py
```
