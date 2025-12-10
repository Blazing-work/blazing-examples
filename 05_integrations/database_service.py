"""
# Database Service

Connect to PostgreSQL and perform database operations with SQLAlchemy.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Intermediate
- **Time**: 20 min
- **Tags**: service, database, sqlalchemy, postgres

## Description

Connect to PostgreSQL and perform database operations with SQLAlchemy.

## What you'll learn

- How to create services with @app.service
- How to use SQLAlchemy connectors
- Database query patterns in services
"""

from sqlalchemy import text

from blazing import Blazing
from blazing.base import BaseService


async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    @app.service
    class UserDatabase(BaseService):
        def __init__(self, connectors):
            self._db = connectors.get("postgres")

        async def get_user(self, user_id: int) -> dict:
            """Fetch user from database."""
            query = text("SELECT id, name, email FROM users WHERE id = :id")
            result = await self._db.execute(query, {"id": user_id})
            row = result.fetchone()
            return {"id": row[0], "name": row[1], "email": row[2]}

        async def create_user(self, name: str, email: str) -> int:
            """Create new user."""
            query = text(
                "INSERT INTO users (name, email) VALUES (:name, :email) RETURNING id"
            )
            result = await self._db.execute(query, {"name": name, "email": email})
            return result.fetchone()[0]

    @app.step
    async def register_user(name: str, email: str, services=None):
        """Register new user (uses database service)."""
        user_id = await services["UserDatabase"].create_user(name, email)
        return {"user_id": user_id, "name": name, "email": email}

    await app.publish()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
