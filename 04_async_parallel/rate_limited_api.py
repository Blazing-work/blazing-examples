"""
# Rate-Limited API Calls

Control concurrency with asyncio.Semaphore for rate limiting.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Advanced
- **Time**: 25 min
- **Tags**: rate-limiting, semaphore, api, concurrency

## Description

Control concurrency with asyncio.Semaphore for rate limiting.

## What you'll learn

- How to implement rate limiting with Semaphore
- Controlling concurrent API calls
- Preventing API throttling errors
"""

import asyncio
from blazing.base import BaseService
    import asyncio

from blazing import Blazing

async def main():
    app = Blazing(api_url="http://localhost:8000", api_token="your-token")

    @app.service
    class RateLimitedAPI(BaseService):
        def __init__(self, connectors):
            self._api_key = connectors.get('api_key')
            self._semaphore = asyncio.Semaphore(5)  # Max 5 concurrent
        async def call_api(self, endpoint: str) -> dict:
            """Call API with rate limiting."""
            async with self._semaphore:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        f"https://api.example.com/{endpoint}",
                        headers={"Authorization": f"Bearer {self._api_key}"}
                    )
                    return response.json()
    @app.workflow
    async def fetch_multiple_endpoints(endpoints: list, services=None):
        """Fetch multiple API endpoints with rate limiting."""
        tasks = [
            services['RateLimitedAPI'].call_api(endpoint)
            for endpoint in endpoints
        ]
        results = await asyncio.gather(*tasks)
        return results
    await app.publish()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
