"""
# Cleanup Expired Records

Batch delete expired database records on a schedule.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Intermediate
- **Time**: 20 min
- **Tags**: cleanup, scheduled, batch, database

## Description

Batch delete expired database records on a schedule.

## What you'll learn

- Batch cleanup patterns
- Scheduled maintenance jobs
- Database cleanup strategies
"""

    from sqlalchemy import text
    from sqlalchemy import text
    from datetime import datetime, timedelta

from blazing import Blazing

async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    @app.step
    async def find_expired_sessions(cutoff_date: str, services=None):
        """Find sessions older than cutoff date."""

        query = text("""
            SELECT session_id FROM sessions
            WHERE last_activity < :cutoff
            LIMIT 1000
        """)

        result = await services['Database'].execute(query, {"cutoff": cutoff_date})
        return [row[0] for row in result.fetchall()]

    @app.step
    async def delete_sessions(session_ids: list, services=None):
        """Delete expired sessions."""

        query = text("DELETE FROM sessions WHERE session_id = ANY(:ids)")
        await services['Database'].execute(query, {"ids": session_ids})

        return {"deleted": len(session_ids)}

    @app.workflow
    async def cleanup_expired_sessions(days_old: int = 30, services=None):
        """Clean up sessions older than N days."""

        cutoff_date = (datetime.now() - timedelta(days=days_old)).isoformat()

        # Find expired sessions
        session_ids = await find_expired_sessions(cutoff_date, services=services)

        if not session_ids:
            return {"deleted": 0, "message": "No expired sessions"}

        # Delete sessions
        result = await delete_sessions(session_ids, services=services)

        return {
            "cutoff_date": cutoff_date,
            "deleted": result['deleted']
        }

    await app.publish()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
