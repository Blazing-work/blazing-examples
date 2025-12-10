"""
# Cache Service

Implement caching with Redis for faster lookups.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Intermediate
- **Time**: 20 min
- **Tags**: service, cache, redis, performance

## Description

Implement caching with Redis for faster lookups.

## What you'll learn

- How to use Redis for caching
- Setting TTL (time-to-live) on cached values
- Cache-aside pattern implementation
"""

from blazing import Blazing
from blazing.base import BaseService


async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    @app.service
    class CacheService(BaseService):
        def __init__(self, connectors):
            self._redis = connectors.get("redis")

        async def get(self, key: str) -> str:
            """Get value from cache."""
            value = await self._redis.get(key)
            return value.decode() if value else None

        async def set(self, key: str, value: str, ttl: int = 3600):
            """Set value in cache with TTL."""
            await self._redis.set(key, value, ex=ttl)

    @app.step
    async def cached_lookup(key: str, services=None):
        """Lookup value with caching."""
        cached = await services["CacheService"].get(key)
        if cached:
            return {"source": "cache", "value": cached}
        # Simulate expensive operation
        value = f"computed_value_for_{key}"
        await services["CacheService"].set(key, value)
        return {"source": "computed", "value": value}

    await app.publish()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
