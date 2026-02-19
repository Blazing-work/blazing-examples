"""
Remote Control Plane Connection

Demonstrates configuring a Blazing instance to connect to a remote control plane
using API URL and token from environment variables.  The app is published and a
simple echo workflow is invoked to confirm the remote connection is working.

Patterns shown:
  1. Blazing(api_url=..., api_token=...) for remote control plane configuration
  2. Reading BLAZING_API_URL and BLAZING_API_TOKEN from environment with fallback defaults
  3. Verifying connectivity by running a minimal echo workflow via wait_result()
"""
import os
from blazing import Blazing


async def main():
    api_url = os.getenv('BLAZING_API_URL', 'http://localhost:8000')
    api_token = os.getenv('BLAZING_API_TOKEN', 'test-token')
    app = Blazing(api_url=api_url, api_token=api_token)

    @app.step
    async def echo(message: str, services=None):
        return message

    @app.workflow
    async def ping(message: str, services=None):
        return await echo(message, services=services)

    await app.publish()
    result = await app.ping(message='hello').wait_result()
    print({'result': result})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
