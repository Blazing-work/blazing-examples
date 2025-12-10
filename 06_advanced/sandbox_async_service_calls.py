"""
# Sandbox: Async Service Calls

User code making concurrent service calls for performance.

## Metadata
- **Product**: Blazing Flow Sandbox
- **Difficulty**: Expert
- **Time**: 30 min
- **Tags**: sandbox, async, concurrent, service-bridge

## Description

User code making concurrent service calls for performance.

## What you'll learn

- Concurrent service calls from sandbox
- Performance optimization in WASM
- Async patterns in sandboxed code
"""

from blazing import Blazing
from blazing.base import BaseService
import asyncio

async def main():
    app = Blazing()  # Uses Blazing SaaS by default
    # YOUR CODE (trusted - provides data access)
    @app.service
    class DataService(BaseService):
        def __init__(self, connectors):
            self._db = connectors.get('postgres')
        async def fetch_user(self, user_id: int) -> dict:
            """Fetch single user."""
            query = text("SELECT * FROM users WHERE id = :id")
            result = await self._db.execute(query, {"id": user_id})
            return dict(result.fetchone())
        async def fetch_orders(self, user_id: int) -> list:
            """Fetch user's orders."""
            query = text("SELECT * FROM orders WHERE user_id = :user_id")
            result = await self._db.execute(query, {"user_id": user_id})
            return [dict(row) for row in result]
        async def fetch_recommendations(self, user_id: int) -> list:
            """Fetch user's recommendations."""
            query = text("SELECT * FROM recommendations WHERE user_id = :user_id")
            result = await self._db.execute(query, {"user_id": user_id})
            return [dict(row) for row in result]
    # USER CODE (untrusted - makes concurrent service calls)
    @app.step
    async def analyze_user(user_id: int, services=None):
        """
        User-provided analysis with concurrent service calls.
        Runs in WASM sandbox but can call services concurrently.
        """
        # Fetch all data concurrently (service calls execute on trusted workers)
        user, orders, recommendations = await asyncio.gather(
            services['DataService'].fetch_user(user_id),
            services['DataService'].fetch_orders(user_id),
            services['DataService'].fetch_recommendations(user_id)
        )
        # Process in sandbox
        total_spent = sum(order['amount'] for order in orders)
        avg_order = total_spent / len(orders) if orders else 0
        return {
            "user_id": user_id,
            "name": user['name'],
            "total_orders": len(orders),
            "total_spent": total_spent,
            "avg_order": avg_order,
            "recommendations_count": len(recommendations)
        }
    # YOUR CODE (trusted - orchestrates)
    @app.workflow
    async def user_report(user_id: int, services=None):
        """Generate user report using user's analysis logic."""
        return await analyze_user(user_id, services=services)
    await app.publish()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
