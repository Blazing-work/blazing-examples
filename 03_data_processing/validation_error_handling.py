"""
# Validation & Error Handling

Validate input data and handle errors gracefully in workflows.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Intermediate
- **Time**: 20 min
- **Tags**: validation, error-handling, data-quality

## Description

Validate input data and handle errors gracefully in workflows.

## What you'll learn

- Input validation patterns
- Graceful error handling in workflows
- Error propagation strategies
"""

import re

from blazing import Blazing


async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    @app.step
    async def validate_email(email: str, services=None):
        """Validate email format."""
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, email):
            raise ValueError(f"Invalid email: {email}")
        return {"valid": True, "email": email}

    @app.workflow
    async def process_user_registration(email: str, name: str, services=None):
        """Register user with validation."""
        try:
            # Validate email
            await validate_email(email, services=services)

            # Create user
            user_id = await services["UserDatabase"].create_user(name, email)

            # Send welcome email
            await services["EmailService"].send(email, "Welcome!", f"Hello {name}")

            return {"success": True, "user_id": user_id}
        except ValueError as e:
            return {"success": False, "error": str(e)}

    await app.publish()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
