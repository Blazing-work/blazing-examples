# Volume File Storage

Persistent file storage for services via `VolumeConnector`.

## Key Concepts

- **Volumes are only accessible through Services** — sandboxed step code cannot directly access storage (same security model as databases)
- `Volume.persisted("name")` — durable storage, survives service restarts
- `Volume.ephemeral("name")` — temporary storage, cleared on restart
- `VolumeConnector` is injected by Blazing at runtime, no manual setup needed

## API

```python
from blazing.volumes import Volume

# Declare at module level
model_storage = Volume.persisted("model-checkpoints")
scratch = Volume.ephemeral("pipeline-scratch")

@app.service(volumes=[model_storage])
class CheckpointService(BaseService):
    def __init__(self, connector_instances=None):
        super().__init__(connector_instances)
        self.volume = connector_instances.get("model-checkpoints")

    async def save(self, path: str, data: bytes):
        await self.volume.put_file(path, data)
        await self.volume.commit()           # flush to durable storage

    async def load(self, path: str) -> bytes:
        return await self.volume.get_file(path)

    async def ls(self, path: str) -> list:
        return await self.volume.listdir(path)
```

## File Operations

| Method | Description |
|--------|-------------|
| `put_file(path, bytes)` | Write file |
| `get_file(path)` | Read file → `bytes` |
| `listdir(path)` | List directory → `list[str]` |
| `stat(path)` | Get file metadata (size, etc.) |
| `delete_file(path)` | Delete a file |
| `commit()` | Flush pending writes |
| `reload()` | Sync with latest committed state |

## Use Cases

- ML model checkpoints between training epochs
- Staged files for multi-step data pipelines
- Cached computation results shared across workers

## Running

```bash
docker-compose up -d
python flow.py
```
