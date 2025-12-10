"""
# REST API Service

Call external REST APIs with httpx and handle responses.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Intermediate
- **Time**: 20 min
- **Tags**: service, api, httpx, rest

## Description

Call external REST APIs with httpx and handle responses.

## What you'll learn

- How to make HTTP requests from services
- How to manage API credentials with connectors
- Error handling for external API calls
"""

import httpx
from blazing.base import BaseService

from blazing import Blazing

async def main():
    app = Blazing(api_url="http://localhost:8000", api_token="your-token")

    @app.service
    class WeatherAPI(BaseService):
        def __init__(self, connectors):
            self._api_key = connectors.get('weather_api_key')
        async def get_weather(self, city: str) -> dict:
            """Fetch weather for city."""
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://api.weather.com/v1/{city}",
                    headers={"Authorization": f"Bearer {self._api_key}"}
                )
                return response.json()
    @app.step
    async def check_weather(city: str, services=None):
        """Check weather for city."""
        weather = await services['WeatherAPI'].get_weather(city)
        return {
            "city": city,
            "temperature": weather['temp'],
            "conditions": weather['conditions']
        }
    await app.publish()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
