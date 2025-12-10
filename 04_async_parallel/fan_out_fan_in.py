"""
# Fan-Out / Fan-In Pattern

Fetch data from multiple sources in parallel, then combine results.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Advanced
- **Time**: 25 min
- **Tags**: parallel, fan-out, fan-in, aggregation

## Description

Fetch data from multiple sources in parallel, then combine results.

## What you'll learn

- Fan-out/fan-in orchestration pattern
- Parallel data fetching strategies
- Result aggregation techniques
"""

import asyncio

from blazing import Blazing


async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    @app.step
    async def fetch_user_data(user_id: int, services=None):
        """Fetch user data."""
        user = await services["UserDatabase"].get_user(user_id)
        return user

    @app.step
    async def fetch_user_orders(user_id: int, services=None):
        """Fetch user orders."""
        orders = await services["OrderDatabase"].get_orders(user_id)
        return orders

    @app.step
    async def fetch_user_preferences(user_id: int, services=None):
        """Fetch user preferences."""
        prefs = await services["PreferenceService"].get(user_id)
        return prefs

    @app.workflow
    async def get_user_profile(user_id: int, services=None):
        """Fetch all user data in parallel (fan-out), then combine (fan-in)."""
        user, orders, prefs = await asyncio.gather(
            fetch_user_data(user_id, services=services),
            fetch_user_orders(user_id, services=services),
            fetch_user_preferences(user_id, services=services),
        )
        return {"user": user, "orders": orders, "preferences": prefs}

    await app.publish()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
