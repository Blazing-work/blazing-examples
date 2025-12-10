"""
# Sandbox: Service Bridge with Database

Let user code process data while keeping database credentials safe.

## Metadata
- **Product**: Blazing Flow Sandbox
- **Difficulty**: Advanced
- **Time**: 25 min
- **Tags**: sandbox, service-bridge, database, security

## Description

Let user code process data while keeping database credentials safe.

## What you'll learn

- How the Service Bridge pattern works
- Allowing database access from sandboxed code
- Protecting credentials in multi-tenant systems
"""

from blazing import Blazing
from blazing.base import BaseService
from sqlalchemy import create_engine, text

async def main():
    app = Blazing(api_url="http://localhost:8000", api_token="your-token")
    # YOUR CODE (trusted - has real database access)
    @app.service
    class DatabaseService(BaseService):
        def __init__(self, connectors):
            # Real database connection (user code NEVER sees this)
            self._db = connectors.get('postgres')
        async def fetch_users(self, min_age: int) -> list:
            """Fetch users from database."""
            # ✅ Parameterized query (safe from SQL injection)
            query = text("SELECT id, name, age FROM users WHERE age >= :min_age")
            result = await self._db.execute(query, {"min_age": min_age})
            return [dict(row) for row in result]
        async def save_scores(self, user_scores: list):
            """Batch update user scores."""
            for item in user_scores:
                query = text("UPDATE users SET score = :score WHERE id = :id")
                await self._db.execute(query, {
                    "id": item["user_id"],
                    "score": item["score"]
                })
            await self._db.commit()
    # USER CODE (untrusted - runs in WASM sandbox)
    @app.step
    async def calculate_scores(min_age: int, services=None):
        """
        User-provided scoring logic.
        Can call database methods but CANNOT access database directly.
        """
        # Fetch data via service (executes on trusted worker)
        users = await services['DatabaseService'].fetch_users(min_age)
        # Process in sandbox (NO database access)
        user_scores = []
        for user in users:
            score = len(user['name']) * user['age']  # User's scoring logic
            user_scores.append({"user_id": user['id'], "score": score})
        # Save via service (executes on trusted worker)
        await services['DatabaseService'].save_scores(user_scores)
        return {"processed": len(user_scores)}
    # YOUR CODE (trusted - orchestrates)
    @app.workflow
    async def score_users(min_age: int, services=None):
        """Run user's scoring algorithm safely."""
        return await calculate_scores(min_age, services=services)
    await app.publish()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
