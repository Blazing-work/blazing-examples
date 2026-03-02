# Bitcoin Node

## Environment Variables

| Variable | Description |
|:--------:|:-----------:|
| `LINK_BINARY` | Download URL for the Bitcoin binary archive |
| `SNAPSHOT` | URL to an `lz4` node snapshot (leave empty to sync the full blockchain) |
| `ARGS` | Startup flags for `bitcoind` |

## Resources

### Ephemeral Storage

> **Warning:** Data will be lost when the container restarts.

```yaml
profiles:
  compute:
    app:
      resources:
        cpu:
          units: 2.0
        memory:
          size: 2Gi
        storage:
          size: 600Gi
```

### Persistent Storage

1. Uncomment in the `app` section:

```yaml
    params:
      storage:
        data:
          mount: /root/
```

1. Uncomment in the `profiles` section:

```yaml
profiles:
  compute:
    app:
      resources:
        cpu:
          units: 2.0
        memory:
          size: 2Gi
        storage:
          size: 10Gi
          - name: data
            size: 600Gi
            attributes:
              persistent: true
              class: beta3
```
