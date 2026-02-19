"""
ASGI Server Integration

Demonstrates serving a Blazing workflow as a real HTTP endpoint via uvicorn.
create_asgi_app() wraps the Blazing app in an ASGI-compatible FastAPI app that
uvicorn serves directly, enabling standard HTTP clients to call Blazing workflows.

Patterns shown:
  1. @app.endpoint(path='/hello') to expose a workflow as an HTTP route
  2. create_asgi_app(app) to produce an ASGI app from the Blazing instance
  3. uvicorn.run(asgi_app) to serve the endpoint on localhost:8080
"""
import uvicorn
from blazing import Blazing
from blazing.web import create_asgi_app


async def main():
    app = Blazing()

    @app.endpoint(path='/hello')
    @app.workflow
    async def hello(name: str, services=None):
        return {'message': f'Hello, {name}!'}

    await app.publish()
    asgi_app = await create_asgi_app(app)
    uvicorn.run(asgi_app, host='0.0.0.0', port=8080)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
