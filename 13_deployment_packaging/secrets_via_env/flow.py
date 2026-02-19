"""
Secrets via Environment Variables

Demonstrates the simplest approach for consuming secrets in a Blazing step: reading
them from environment variables injected at container start.  The step uses os.getenv()
to retrieve MY_SECRET, with a fallback value if the variable is not set.

Patterns shown:
  1. os.getenv('MY_SECRET', 'unset') to read a secret with a safe default
  2. @app.step that accesses environment-level secrets without any special connector
  3. A workflow that delegates entirely to the secret-reading step
"""
import os
from blazing import Blazing


async def main():
    app = Blazing()

    @app.step
    async def read_secret(services=None):
        return os.getenv('MY_SECRET', 'unset')

    @app.workflow
    async def show_secret(services=None):
        return await read_secret(services=services)

    await app.publish()
    result = await app.show_secret().wait_result()
    print({'secret': result})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
