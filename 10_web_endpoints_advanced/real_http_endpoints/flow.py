"""
Real HTTP Endpoints

Demonstrates exposing a Blazing workflow as a real HTTP endpoint served by uvicorn.
The workflow is accessible over the network via a POST to /square, returning the squared
value, confirming that Blazing workflows can serve as production HTTP handlers.

Patterns shown:
  1. @app.endpoint(path='/square') with @app.workflow to define an HTTP-accessible workflow
  2. create_asgi_app(app) to wrap the Blazing app in a FastAPI ASGI application
  3. uvicorn.run(fastapi_app) to serve the endpoint at localhost:8080
"""
import uvicorn
from blazing import Blazing
from blazing.web import create_asgi_app


async def main():
    app = Blazing()

    @app.endpoint(path='/square')
    @app.workflow
    async def square(value: int, services=None):
        return value * value

    await app.publish()
    fastapi_app = await create_asgi_app(app)
    uvicorn.run(fastapi_app, host='0.0.0.0', port=8080)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
