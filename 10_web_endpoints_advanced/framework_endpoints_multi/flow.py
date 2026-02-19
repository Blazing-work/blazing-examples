"""
Framework Endpoints Multi

Demonstrates exposing a Blazing workflow as an HTTP endpoint through create_asgi_app()
and serving it with uvicorn.  This is the simplest example of a single-endpoint Blazing
ASGI application using the default POST method.

Patterns shown:
  1. @app.endpoint(path='/add') with @app.workflow stacked on the same function
  2. create_asgi_app(app) to produce the ASGI application object
  3. uvicorn.run(asgi_app) to serve on localhost:8080
"""
import uvicorn
from blazing import Blazing
from blazing.web import create_asgi_app


async def main():
    app = Blazing()

    @app.endpoint(path='/add')
    @app.workflow
    async def add(x: int, y: int, services=None):
        return x + y

    await app.publish()
    asgi_app = await create_asgi_app(app)
    uvicorn.run(asgi_app, host='0.0.0.0', port=8080)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
