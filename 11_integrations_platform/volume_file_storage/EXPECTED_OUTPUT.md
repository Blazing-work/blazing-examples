# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Volume File Storage Patterns:

  Volume.persisted('name')  — durable storage
  Volume.ephemeral('name')  — temporary, cleared on restart

  @app.service(volumes=[vol]) — declares which volumes a service uses
  connector_instances['vol-name'] — VolumeConnector injected at runtime

  volume.put_file(path, bytes)  — write file
  volume.get_file(path)         — read file
  volume.listdir(path)          — list directory
  volume.commit()               — flush writes to durable storage

Training result: {'epochs_saved': 3, 'total_checkpoints': 3, 'details': [{'path': '/checkpoints/epoch_0000.bin', 'size': 17, 'epoch': 0}, {'path': '/checkpoints/epoch_0001.bin', 'size': 17, 'epoch': 1}, {'path': '/checkpoints/epoch_0002.bin', 'size': 17, 'epoch': 2}]}
```

## Notes

- Requires a running Blazing infrastructure: `docker-compose up -d`
- The `main()` block prints API patterns then calls `app.publish()` and runs `training_loop(3)`
- `epochs_saved=3` — epochs 0, 1, 2 are saved as checkpoints
- File sizes (17 bytes) reflect the fake weight strings `b'weights_epoch_N'`
