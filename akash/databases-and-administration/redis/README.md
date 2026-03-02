# redis

Redis is an open-source, in-memory data structure store used as a database, cache, message broker, and streaming engine.

## Use Cases

- Application caching layer
- Session management
- Real-time leaderboards and counters
- Pub/sub messaging
- Rate limiting

## Getting Started

1. The service is ready as soon as it reaches "Running" status
2. Connect with `redis-cli` or any Redis client library
3. Start setting and getting keys: `SET mykey "Hello"` / `GET mykey`

## Accessing the Service

Connect using the Redis CLI:
```bash
redis-cli -h {SERVICE_URI} -p 6379
```


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `REDIS_AOF_ENABLED` | `no` |

### Secrets

The following values are configured as secrets and should be set securely:

- `ALLOW_EMPTY_PASSWORD`
- `REDIS_PASSWORD`

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `redis:8.2.2` |
| CPU | 1.0 |
| Memory | 1Gi |
| Storage | 1Gi |
| Exposed Ports | 6379 |

## Documentation

For full documentation, visit: [https://redis.io/docs/](https://redis.io/docs/)
