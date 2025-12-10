"""
# Sandbox: Service Bridge with REST APIs

Let users integrate with external APIs while keeping API keys safe.

## Metadata
- **Product**: Blazing Flow Sandbox
- **Difficulty**: Advanced
- **Time**: 25 min
- **Tags**: sandbox, service-bridge, api, security

## Description

Let users integrate with external APIs while keeping API keys safe.

## What you'll learn

- How to call external APIs from sandboxed code
- API key protection patterns
- Rate limiting at service level
"""

import httpx

from blazing import Blazing
from blazing.base import BaseService


async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    # YOUR CODE (trusted - has real API credentials)
    @app.service
    class ExternalAPIService(BaseService):
        def __init__(self, connectors):
            # Real API key (user code NEVER sees this)
            self._api_key = connectors.get("api_key")
            self._base_url = "https://api.example.com"

        async def fetch_weather(self, city: str) -> dict:
            """Fetch weather from external API."""
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self._base_url}/weather/{city}",
                    headers={"Authorization": f"Bearer {self._api_key}"},
                )
                return response.json()

        async def fetch_exchange_rate(
            self, from_currency: str, to_currency: str
        ) -> float:
            """Fetch exchange rate."""
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self._base_url}/exchange",
                    params={"from": from_currency, "to": to_currency},
                    headers={"Authorization": f"Bearer {self._api_key}"},
                )
                data = response.json()
                return data["rate"]

    # USER CODE (untrusted - runs in WASM sandbox)
    @app.step
    async def analyze_travel_cost(city: str, budget_usd: float, services=None):
        """
        User-provided travel analysis.
        Can call APIs via service but NO direct network access.
        """
        # Fetch data via services (execute on trusted workers)
        weather = await services["ExternalAPIService"].fetch_weather(city)
        exchange_rate = await services["ExternalAPIService"].fetch_exchange_rate(
            "USD", "EUR"
        )
        # Process in sandbox
        budget_eur = budget_usd * exchange_rate
        temp = weather.get("temperature", 20)
        # User's logic
        recommendation = "Go!" if 15 <= temp <= 25 else "Too hot/cold"
        return {
            "city": city,
            "temperature": temp,
            "budget_usd": budget_usd,
            "budget_eur": budget_eur,
            "recommendation": recommendation,
        }

    # YOUR CODE (trusted - orchestrates)
    @app.workflow
    async def plan_trip(city: str, budget_usd: float, services=None):
        """Run user's travel analysis safely."""
        return await analyze_travel_cost(city, budget_usd, services=services)

    await app.publish()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
