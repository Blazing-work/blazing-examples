"""
Custom Exception Handler

Demonstrates registering a FastAPI exception handler to convert ValueError raised
inside a Blazing workflow into a structured 400 JSON response.  The Blazing ASGI app
is mounted on a parent FastAPI router that owns the exception handler.

Patterns shown:
  1. @app.endpoint with a workflow that raises ValueError for invalid input
  2. @api.exception_handler(ValueError) to catch domain errors and return 400
  3. api.mount('/blazing', blazing_asgi) to compose Blazing under a FastAPI router
"""
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from blazing import Blazing
from blazing.web import create_asgi_app


async def main():
    app = Blazing()

    @app.endpoint(path='/divide', method='POST')
    @app.workflow
    async def divide(x: int, y: int, services=None):
        if y == 0:
            raise ValueError('y must be non-zero')
        return {'result': x / y}

    await app.publish()
    blazing_asgi = await create_asgi_app(app)

    api = FastAPI()

    @api.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        return JSONResponse({'detail': str(exc)}, status_code=400)

    api.mount('/blazing', blazing_asgi)
    uvicorn.run(api, host='0.0.0.0', port=8080)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
