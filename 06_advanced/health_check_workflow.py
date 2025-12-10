"""
# Health Check Workflow

Monitor system health across database, cache, and external APIs.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Intermediate
- **Time**: 20 min
- **Tags**: monitoring, health-check, observability

## Description

Monitor system health across database, cache, and external APIs.

## What you'll learn

- Health check implementation patterns
- Parallel service monitoring
- System observability strategies
"""

        from sqlalchemy import text
        import httpx
    import asyncio

from blazing import Blazing

async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    @app.step
    async def check_database_health(services=None):
        """Check database connectivity."""
        try:
            await services['Database'].execute(text("SELECT 1"))
            return {"service": "database", "status": "healthy"}
        except Exception as e:
            return {"service": "database", "status": "unhealthy", "error": str(e)}

    @app.step
    async def check_cache_health(services=None):
        """Check cache connectivity."""
        try:
            await services['CacheService'].set('health_check', 'ok', ttl=10)
            value = await services['CacheService'].get('health_check')
            if value == 'ok':
                return {"service": "cache", "status": "healthy"}
            return {"service": "cache", "status": "unhealthy", "error": "Value mismatch"}
        except Exception as e:
            return {"service": "cache", "status": "unhealthy", "error": str(e)}

    @app.step
    async def check_external_api_health(services=None):
        """Check external API connectivity."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://api.example.com/health", timeout=5.0)
                if response.status_code == 200:
                    return {"service": "external_api", "status": "healthy"}
                return {"service": "external_api", "status": "unhealthy", "error": f"Status {response.status_code}"}
        except Exception as e:
            return {"service": "external_api", "status": "unhealthy", "error": str(e)}

    @app.workflow
    async def health_check(services=None):
        """Run health checks for all services."""

        checks = await asyncio.gather(
            check_database_health(services=services),
            check_cache_health(services=services),
            check_external_api_health(services=services)
        )

        healthy = all(c['status'] == 'healthy' for c in checks)

        return {
            "overall_status": "healthy" if healthy else "degraded",
            "checks": checks,
            "timestamp": datetime.now().isoformat()
        }

    await app.publish()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
