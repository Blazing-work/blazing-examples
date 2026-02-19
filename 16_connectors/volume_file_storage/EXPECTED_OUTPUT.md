# Expected Output

## Running

```bash
python flow.py
```

## Requirements

- `pip install blazing`
- No docker-compose needed — uses LocalVolumeService (in-process emulator)

## Output

```
=== Volume File Storage with VolumeConnector ===

--- Pattern 1: FileProcessorService with VolumeConnector ---
  Written: /hello.txt (15 bytes)
  Read back: 'Hello, Blazing!'

--- Pattern 2: Transform pipeline (uppercase) ---
  Input:  /input/data.txt (24 bytes)
  Output: /output/result.txt (24 bytes)
  Transformed: 'HELLO WORLD FROM BLAZING'

--- Pattern 3: LocalStack-managed volume with multi-worker reload ---
  Worker 2 read Worker 1 data: {"status": "done", "items": 42}
  Root dirs after reload: ['worker1', 'worker2']
  Stack volume count: 1

=== Done ===
```

## Multi-Worker Semantics

| Step | Worker | Operation | Notes |
|------|--------|-----------|-------|
| 1 | Worker 1 | `put_file` + `commit()` | Writes flushed to durable storage |
| 2 | Worker 2 | `reload()` + `get_file` | Sees Worker 1's data after reload |
| 3 | Worker 2 | `put_file` + `commit()` | Worker 2 also writes |
| 4 | Worker 1 | `reload()` + `listdir("/")` | Both worker dirs visible |

## Notes

- `commit()` must be called after writes to make them visible to other workers — without it writes remain in the local buffer
- `reload()` syncs the local cache with durable storage — call it before reading from a volume that another worker may have written to
- `LocalVolumeService` provides the same `VolumeConnector` interface as the production backend (SeaweedFS)
- The higher-level `Volume.persisted("name")` / `Volume.ephemeral("name")` API (used in `11_integrations_platform/volume_file_storage/`) wraps the same connector underneath
- For production, replace `LocalVolumeService` with the cloud-backed volume service
